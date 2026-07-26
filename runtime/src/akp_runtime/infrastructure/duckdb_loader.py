"""DuckDB pack adapter — reads compiled Knowledge Packs.

What: Opens .duckdb files read-only, validates schema, provides query methods.
Why: Isolates DuckDB dependency behind adapter boundary.
Contracts: Implements LoadedPack and PackLoader protocols.
Boundaries: ONLY runtime file that imports duckdb. SQL lives in persistence/queries/.
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
)
from akp_runtime.domain.models import (
    GraphEdgeHit,
    PackMetadata,
    ProvenanceStep,
    SearchHit,
)
from akp_runtime.domain.search_results import SemanticUnitRecord
from akp_runtime.infrastructure.persistence.manifest_parser import (
    REQUIRED_MANIFEST_KEYS,
    REQUIRED_TABLES,
    ManifestParser,
)
from akp_runtime.infrastructure.persistence.queries.base import QueryExecutor
from akp_runtime.infrastructure.persistence.queries.graph_queries import (
    EdgeProvenanceQuery,
    EdgesFromNodeQuery,
)
from akp_runtime.infrastructure.persistence.queries.provenance_queries import (
    ObjectProvenanceQuery,
    UnitProvenanceQuery,
)
from akp_runtime.infrastructure.persistence.queries.schema_validation import (
    ListTablesQuery,
    LoadManifestQuery,
)
from akp_runtime.infrastructure.persistence.queries.search_queries import (
    ConceptUnitsQuery,
    ExactAliasMatchQuery,
    LexicalSearchQuery,
    LookupObjectQuery,
    ObjectFallbackQuery,
)
from akp_runtime.infrastructure.persistence.result_mapper import SearchHitMapper, SemanticUnitMapper

logger = logging.getLogger(__name__)


class DuckDBLoadedPack:
    """A single opened Knowledge Pack backed by DuckDB.

    Implements the LoadedPack protocol. Connection is read-only.
    """

    def __init__(self, pack_path: Path) -> None:
        self._path = pack_path.resolve()
        self._closed = False

        try:
            self._connection = duckdb.connect(str(self._path), read_only=True)
        except Exception as error:
            raise PackOpenError(pack_path=self._path, detail=str(error)) from error

        self._executor = QueryExecutor(self._connection, pack_id="unknown")
        self._validate_schema()
        manifest = self._load_manifest()
        parser = ManifestParser()
        self._metadata = parser.build_metadata(manifest, self._path)
        self._executor = QueryExecutor(self._connection, pack_id=self._metadata.pack_id)
        self._mapper = SearchHitMapper(
            self._metadata.pack_id,
            self._metadata.pack_version,
            self._pack_provenance_step(),
        )

    def _validate_schema(self) -> None:
        """Check all required tables exist."""
        existing = self._executor.execute(ListTablesQuery())
        for table in REQUIRED_TABLES:
            if table not in existing:
                self._connection.close()
                raise MissingPackTable(pack_path=self._path, table_name=table)

    def _load_manifest(self) -> dict[str, str]:
        """Load and validate manifest key-value pairs."""
        manifest = self._executor.execute(LoadManifestQuery())
        missing = REQUIRED_MANIFEST_KEYS - manifest.keys()
        if missing:
            first_missing = sorted(missing)[0]
            self._connection.close()
            raise MissingManifestKey(pack_path=self._path, key=first_missing)
        return manifest

    @property
    def metadata(self) -> PackMetadata:
        return self._metadata

    def exact_matches(self, query: str, limit: int) -> list[SearchHit]:
        """Find objects by exact alias match."""
        effective_limit = max(1, limit) if limit > 0 else 0
        if effective_limit == 0:
            return []
        rows = self._executor.execute(ExactAliasMatchQuery(query, effective_limit))
        return [self._mapper.from_object_row(row) for row in rows]

    def object_fallback(self, query: str, limit: int) -> list[SearchHit]:
        """Fallback search by object title LIKE match."""
        rows = self._executor.execute(ObjectFallbackQuery(query, max(1, limit)))
        return [self._mapper.from_object_row(row) for row in rows]

    def lexical_matches(self, query: str, top_k: int) -> list[SearchHit]:
        """BM25 lexical search placeholder using LIKE."""
        rows = self._executor.execute(LexicalSearchQuery(query, max(1, top_k)))
        return [self._mapper.from_object_row(row) for row in rows]

    def semantic_matches(self, vector: list[float], top_k: int) -> list[SearchHit]:
        """Vector-based semantic search — requires external VectorIndex."""
        return []

    def lookup_concept(self, identifier: str) -> SearchHit | None:
        """Look up an object by its exact ID."""
        rows = self._executor.execute(LookupObjectQuery(identifier))
        if not rows:
            return None
        return self._mapper.from_object_row(rows[0])

    def concept_units(self, object_id: str, limit: int) -> list[SemanticUnitRecord]:
        """Retrieve semantic units for an object."""
        rows = self._executor.execute(ConceptUnitsQuery(object_id, max(1, limit)))
        return [SemanticUnitMapper.from_row(row) for row in rows]

    def graph_neighbors(
        self, object_id: str, hops: int, predicates: tuple[str, ...], limit: int,
    ) -> list[GraphEdgeHit]:
        """BFS graph traversal respecting depth and limit bounds."""
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
        """Fetch outgoing edges from a node."""
        rows = self._executor.execute(EdgesFromNodeQuery(node_id, predicates))
        return [
            GraphEdgeHit(
                pack_id=self._metadata.pack_id, subject_id=row[0],
                predicate=row[1], object_id=row[2], origin=row[3],
                confidence=row[4], neighbor_title=row[5], neighbor_type=row[6],
                provenance=(self._pack_provenance_step(),),
            )
            for row in rows
        ]

    def provenance_for_object(self, object_id: str) -> tuple[ProvenanceStep, ...]:
        """Assemble provenance chain for an object."""
        rows = self._executor.execute(ObjectProvenanceQuery(object_id))
        steps = [self._pack_provenance_step()]
        if rows:
            steps.append(ProvenanceStep(
                layer="object", identifier=rows[0][0], origin="authored",
                source_path=rows[0][1], pack_id=self._metadata.pack_id,
                pack_version=self._metadata.pack_version,
            ))
        return tuple(steps)

    def provenance_for_unit(self, unit_id: str) -> tuple[ProvenanceStep, ...]:
        """Assemble provenance chain for a semantic unit."""
        rows = self._executor.execute(UnitProvenanceQuery(unit_id))
        steps = [self._pack_provenance_step()]
        if rows:
            steps.append(ProvenanceStep(
                layer="unit", identifier=rows[0][0], origin="authored",
                source_path=rows[0][2], pack_id=self._metadata.pack_id,
                pack_version=self._metadata.pack_version,
            ))
        return tuple(steps)

    def provenance_for_edge(
        self, subject_id: str, predicate: str, object_id: str,
    ) -> tuple[ProvenanceStep, ...]:
        """Assemble provenance chain for a graph edge."""
        rows = self._executor.execute(EdgeProvenanceQuery(subject_id, predicate, object_id))
        steps = [self._pack_provenance_step()]
        if rows:
            steps.append(ProvenanceStep(
                layer="edge", identifier=f"{subject_id}--{predicate}-->{object_id}",
                origin=rows[0][0], pack_id=self._metadata.pack_id,
                pack_version=self._metadata.pack_version,
                metadata={"confidence": rows[0][1]} if rows[0][1] is not None else None,
            ))
        return tuple(steps)

    def _pack_provenance_step(self) -> ProvenanceStep:
        """Create the pack-layer provenance step."""
        return ProvenanceStep(
            layer="pack", identifier=self._metadata.pack_id, origin="authored",
            pack_id=self._metadata.pack_id, pack_version=self._metadata.pack_version,
        )

    def close(self) -> None:
        """Close the DuckDB connection. Idempotent."""
        if not self._closed:
            self._closed = True
            self._executor.mark_closed()
            with contextlib.suppress(Exception):
                self._connection.close()


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
