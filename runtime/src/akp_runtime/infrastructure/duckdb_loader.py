"""DuckDB pack adapter — reads compiled Knowledge Packs.

What: Opens .duckdb files read-only, validates schema, provides query methods.
Why: Isolates DuckDB dependency behind adapter boundary.
Contracts: Implements LoadedPack and PackLoader protocols.
Boundaries: ONLY runtime file that imports duckdb.
"""

from __future__ import annotations

import contextlib
import logging
from collections import deque
from pathlib import Path

import duckdb

from akp_runtime.contracts.errors import (
    MissingManifestKey,
    MissingPackTable,
    PackOpenError,
    PackQueryError,
    RuntimeStateError,
    UnsupportedSchemaVersion,
)
from akp_runtime.domain.models import (
    GraphEdgeHit,
    PackMetadata,
    ProvenanceStep,
    SearchHit,
    SemanticUnitRecord,
)

logger = logging.getLogger(__name__)

REQUIRED_TABLES = ("objects", "semantic_units", "aliases", "edges", "manifest")

REQUIRED_MANIFEST_KEYS = frozenset(
    {
        "pack_id",
        "pack_version",
        "schema_version",
        "ontology_version",
        "compiler_version",
        "build_timestamp",
        "source_file_count",
        "object_count",
        "node_count",
        "edge_count",
        "semantic_unit_count",
        "alias_count",
        "bm25_vocab_size",
        "embedding_model",
        "embedding_dimensions",
        "cross_pack_refs",
        "content_hash",
        "error_count",
        "warning_count",
    }
)

_INT_MANIFEST_KEYS = frozenset(
    {
        "source_file_count",
        "object_count",
        "node_count",
        "edge_count",
        "semantic_unit_count",
        "alias_count",
        "bm25_vocab_size",
        "embedding_dimensions",
        "cross_pack_refs",
        "error_count",
        "warning_count",
    }
)


def _parse_manifest_value(key: str, value: str) -> str | int:
    """Parse manifest string values to appropriate Python types."""
    if key in _INT_MANIFEST_KEYS:
        try:
            return int(value)
        except (ValueError, TypeError):
            return 0
    return value


class DuckDBLoadedPack:
    """A single opened Knowledge Pack backed by DuckDB.

    Implements the LoadedPack protocol. Connection is read-only.
    """

    def __init__(self, pack_path: Path) -> None:
        self._path = pack_path.resolve()
        self._closed = False

        try:
            self._con = duckdb.connect(str(self._path), read_only=True)
        except Exception as e:
            raise PackOpenError(pack_path=self._path, detail=str(e)) from e

        self._validate_tables()
        self._manifest = self._load_manifest()
        self._metadata = self._build_metadata()

    def _validate_tables(self) -> None:
        """Check all required tables exist."""
        result = self._con.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'")
        existing = {row[0] for row in result.fetchall()}
        for table in REQUIRED_TABLES:
            if table not in existing:
                self._con.close()
                raise MissingPackTable(pack_path=self._path, table_name=table)

    def _load_manifest(self) -> dict[str, str]:
        """Load and validate manifest key-value pairs."""
        result = self._con.execute("SELECT key, value FROM manifest")
        manifest = {row[0]: row[1] for row in result.fetchall()}
        missing = REQUIRED_MANIFEST_KEYS - manifest.keys()
        if missing:
            first_missing = sorted(missing)[0]
            self._con.close()
            raise MissingManifestKey(pack_path=self._path, key=first_missing)
        return manifest

    def _build_metadata(self) -> PackMetadata:
        """Construct PackMetadata from validated manifest."""
        schema_version = self._manifest["schema_version"]
        major = schema_version.split(".")[0]
        if major != "2":
            self._con.close()
            raise UnsupportedSchemaVersion(pack_path=self._path, found=schema_version)

        parsed = {k: _parse_manifest_value(k, v) for k, v in self._manifest.items()}
        return PackMetadata(
            pack_id=parsed["pack_id"],  # type: ignore[arg-type]
            pack_version=parsed["pack_version"],  # type: ignore[arg-type]
            schema_version=parsed["schema_version"],  # type: ignore[arg-type]
            compiler_version=parsed["compiler_version"],  # type: ignore[arg-type]
            path=self._path,
            content_hash=parsed["content_hash"],  # type: ignore[arg-type]
            ontology_version=parsed["ontology_version"],  # type: ignore[arg-type]
            build_timestamp=parsed["build_timestamp"],  # type: ignore[arg-type]
            source_file_count=parsed["source_file_count"],  # type: ignore[arg-type]
            object_count=parsed["object_count"],  # type: ignore[arg-type]
            node_count=parsed["node_count"],  # type: ignore[arg-type]
            edge_count=parsed["edge_count"],  # type: ignore[arg-type]
            semantic_unit_count=parsed["semantic_unit_count"],  # type: ignore[arg-type]
            alias_count=parsed["alias_count"],  # type: ignore[arg-type]
            bm25_vocab_size=parsed["bm25_vocab_size"],  # type: ignore[arg-type]
            embedding_model=parsed["embedding_model"],  # type: ignore[arg-type]
            embedding_dimensions=parsed["embedding_dimensions"],  # type: ignore[arg-type]
            cross_pack_refs=parsed["cross_pack_refs"],  # type: ignore[arg-type]
            error_count=parsed["error_count"],  # type: ignore[arg-type]
            warning_count=parsed["warning_count"],  # type: ignore[arg-type]
        )

    def _guard_open(self, operation: str) -> None:
        """Raise RuntimeStateError if connection is closed."""
        if self._closed:
            raise RuntimeStateError(operation=operation, reason="Pack connection is closed")

    def _query(self, sql: str, params: list | None = None, context: str = "") -> list[tuple]:
        """Execute a query with error handling."""
        self._guard_open(context or "query")
        try:
            result = self._con.execute(sql, params) if params else self._con.execute(sql)
            return result.fetchall()
        except Exception as e:
            if self._closed:
                raise RuntimeStateError(operation=context, reason="Pack connection is closed") from e
            raise PackQueryError(
                pack_id=self._metadata.pack_id,
                query_context=context,
                detail=str(e),
            ) from e

    @property
    def metadata(self) -> PackMetadata:
        return self._metadata

    def exact_matches(self, query: str, limit: int) -> list[SearchHit]:
        """Find objects by exact alias match."""
        self._guard_open("exact_matches")
        effective_limit = max(1, limit) if limit > 0 else 0
        if effective_limit == 0:
            return []
        rows = self._query(
            """
            SELECT a.canonical_id, o.type, o.title, o.description, o.domain, o.source_path
            FROM aliases a
            JOIN objects o ON a.canonical_id = o.id
            WHERE a.alias = ?
            LIMIT ?
            """,
            [query, effective_limit],
            "exact_matches",
        )
        return [self._row_to_search_hit(row) for row in rows]

    def object_fallback(self, query: str, limit: int) -> list[SearchHit]:
        """Fallback search by object title LIKE match."""
        self._guard_open("object_fallback")
        rows = self._query(
            """
            SELECT id, type, title, description, domain, source_path
            FROM objects
            WHERE title ILIKE ?
            LIMIT ?
            """,
            [f"%{query}%", max(1, limit)],
            "object_fallback",
        )
        return [self._row_to_search_hit(row) for row in rows]

    def lexical_matches(self, query: str, top_k: int) -> list[SearchHit]:
        """BM25 lexical search — placeholder using LIKE until BM25 index is warmed."""
        self._guard_open("lexical_matches")
        rows = self._query(
            """
            SELECT su.source_object_id, o.type, o.title, o.description, o.domain, o.source_path
            FROM semantic_units su
            JOIN objects o ON su.source_object_id = o.id
            WHERE su.content ILIKE ?
            LIMIT ?
            """,
            [f"%{query}%", max(1, top_k)],
            "lexical_matches",
        )
        return [self._row_to_search_hit(row) for row in rows]

    def semantic_matches(self, vector: list[float], top_k: int) -> list[SearchHit]:
        """Vector-based semantic search — requires external VectorIndex."""
        self._guard_open("semantic_matches")
        # Vector search is delegated to USearch sidecar via operations layer.
        # This method is called with pre-matched unit_ids from the vector index.
        return []

    def lookup_concept(self, identifier: str) -> SearchHit | None:
        """Look up an object by its exact ID."""
        self._guard_open("lookup_concept")
        rows = self._query(
            "SELECT id, type, title, description, domain, source_path FROM objects WHERE id = ?",
            [identifier],
            "lookup_concept",
        )
        if not rows:
            return None
        return self._row_to_search_hit(rows[0])

    def concept_units(self, object_id: str, limit: int) -> list[SemanticUnitRecord]:
        """Retrieve semantic units for an object."""
        self._guard_open("concept_units")
        rows = self._query(
            """
            SELECT su.id, su.source_object_id, su.heading_path, su.content, su.context,
                   su.object_type, su.domain, o.title, o.description, o.source_path
            FROM semantic_units su
            JOIN objects o ON su.source_object_id = o.id
            WHERE su.source_object_id = ?
            LIMIT ?
            """,
            [object_id, max(1, limit)],
            "concept_units",
        )
        return [
            SemanticUnitRecord(
                unit_id=row[0],
                source_object_id=row[1],
                heading_path=row[2] or "",
                content=row[3] or "",
                context=row[4] or "",
                object_type=row[5] or "",
                domain=row[6] or "",
                title=row[7] or "",
                description=row[8] or "",
                source_path=row[9] or "",
                source_kind="authored",
            )
            for row in rows
        ]

    def graph_neighbors(
        self,
        object_id: str,
        hops: int,
        predicates: tuple[str, ...],
        limit: int,
    ) -> list[GraphEdgeHit]:
        """BFS graph traversal respecting depth and limit bounds."""
        self._guard_open("graph_neighbors")
        effective_limit = max(1, limit)
        results: list[GraphEdgeHit] = []
        visited: set[str] = {object_id}
        frontier: deque[str] = deque([object_id])
        current_hop = 0

        while frontier and current_hop < hops and len(results) < effective_limit:
            next_frontier: deque[str] = deque()
            while frontier and len(results) < effective_limit:
                node = frontier.popleft()
                edges = self._fetch_edges_from(node, predicates)
                for edge in edges:
                    if edge.object_id not in visited and len(results) < effective_limit:
                        visited.add(edge.object_id)
                        next_frontier.append(edge.object_id)
                        results.append(edge)
            frontier = next_frontier
            current_hop += 1

        return results

    def _fetch_edges_from(self, node_id: str, predicates: tuple[str, ...]) -> list[GraphEdgeHit]:
        """Fetch outgoing edges from a node, optionally filtered by predicate."""
        if predicates:
            placeholders = ", ".join(["?"] * len(predicates))
            sql = f"""
                SELECT e.subject_id, e.predicate, e.object_id, e.origin, e.confidence,
                       o.title, o.type
                FROM edges e
                LEFT JOIN objects o ON e.object_id = o.id
                WHERE e.subject_id = ? AND e.predicate IN ({placeholders})
            """
            params = [node_id, *predicates]
        else:
            sql = """
                SELECT e.subject_id, e.predicate, e.object_id, e.origin, e.confidence,
                       o.title, o.type
                FROM edges e
                LEFT JOIN objects o ON e.object_id = o.id
                WHERE e.subject_id = ?
            """
            params = [node_id]

        rows = self._query(sql, params, "graph_neighbors")
        return [
            GraphEdgeHit(
                pack_id=self._metadata.pack_id,
                subject_id=row[0],
                predicate=row[1],
                object_id=row[2],
                origin=row[3],
                confidence=row[4],
                neighbor_title=row[5],
                neighbor_type=row[6],
                provenance=(self._pack_provenance_step(),),
            )
            for row in rows
        ]

    def provenance_for_object(self, object_id: str) -> tuple[ProvenanceStep, ...]:
        """Assemble provenance chain for an object."""
        self._guard_open("provenance_for_object")
        rows = self._query(
            "SELECT id, source_path FROM objects WHERE id = ?",
            [object_id],
            "provenance_for_object",
        )
        steps = [self._pack_provenance_step()]
        if rows:
            steps.append(
                ProvenanceStep(
                    layer="object",
                    identifier=rows[0][0],
                    origin="authored",
                    source_path=rows[0][1],
                    pack_id=self._metadata.pack_id,
                    pack_version=self._metadata.pack_version,
                )
            )
        return tuple(steps)

    def provenance_for_unit(self, unit_id: str) -> tuple[ProvenanceStep, ...]:
        """Assemble provenance chain for a semantic unit."""
        self._guard_open("provenance_for_unit")
        rows = self._query(
            """
            SELECT su.id, su.source_object_id, o.source_path
            FROM semantic_units su
            LEFT JOIN objects o ON su.source_object_id = o.id
            WHERE su.id = ?
            """,
            [unit_id],
            "provenance_for_unit",
        )
        steps = [self._pack_provenance_step()]
        if rows:
            steps.append(
                ProvenanceStep(
                    layer="unit",
                    identifier=rows[0][0],
                    origin="authored",
                    source_path=rows[0][2],
                    pack_id=self._metadata.pack_id,
                    pack_version=self._metadata.pack_version,
                )
            )
        return tuple(steps)

    def provenance_for_edge(
        self,
        subject_id: str,
        predicate: str,
        object_id: str,
    ) -> tuple[ProvenanceStep, ...]:
        """Assemble provenance chain for a graph edge."""
        self._guard_open("provenance_for_edge")
        rows = self._query(
            "SELECT origin, confidence FROM edges WHERE subject_id = ? AND predicate = ? AND object_id = ?",
            [subject_id, predicate, object_id],
            "provenance_for_edge",
        )
        steps = [self._pack_provenance_step()]
        if rows:
            steps.append(
                ProvenanceStep(
                    layer="edge",
                    identifier=f"{subject_id}--{predicate}-->{object_id}",
                    origin=rows[0][0],
                    pack_id=self._metadata.pack_id,
                    pack_version=self._metadata.pack_version,
                    metadata={"confidence": rows[0][1]} if rows[0][1] is not None else None,
                )
            )
        return tuple(steps)

    def _pack_provenance_step(self) -> ProvenanceStep:
        """Create the pack-layer provenance step (always present)."""
        return ProvenanceStep(
            layer="pack",
            identifier=self._metadata.pack_id,
            origin="authored",
            pack_id=self._metadata.pack_id,
            pack_version=self._metadata.pack_version,
        )

    def _row_to_search_hit(self, row: tuple) -> SearchHit:
        """Convert a query row (id, type, title, desc, domain, source_path) to SearchHit."""
        return SearchHit(
            pack_id=self._metadata.pack_id,
            pack_version=self._metadata.pack_version,
            object_id=row[0],
            unit_id=None,
            title=row[2] or "",
            object_type=row[1] or "",
            domain=row[4] or "",
            heading_path=None,
            snippet=row[3] or "",
            score=1.0,
            source_kind="authored",
            channels=(),
            provenance=(self._pack_provenance_step(),),
        )

    def close(self) -> None:
        """Close the DuckDB connection. Idempotent."""
        if not self._closed:
            self._closed = True
            with contextlib.suppress(Exception):
                self._con.close()


class DuckDBPackLoader:
    """Loads and manages multiple Knowledge Packs."""

    def __init__(self) -> None:
        self._packs: dict[str, DuckDBLoadedPack] = {}

    def load(self, pack_path: Path) -> DuckDBLoadedPack:
        """Load a single pack, validating schema and tables."""
        if not pack_path.exists():
            raise PackOpenError(pack_path=pack_path, detail="File not found")
        pack = DuckDBLoadedPack(pack_path)
        self._packs[pack.metadata.pack_id] = pack
        return pack

    def load_many(self, pack_paths: list[Path]) -> dict[str, DuckDBLoadedPack]:
        """Load multiple packs, returning dict keyed by pack_id."""
        result: dict[str, DuckDBLoadedPack] = {}
        for path in pack_paths:
            pack = self.load(path)
            result[pack.metadata.pack_id] = pack
        return result

    def close_all(self) -> None:
        """Close all loaded packs."""
        for pack in self._packs.values():
            pack.close()
        self._packs.clear()
