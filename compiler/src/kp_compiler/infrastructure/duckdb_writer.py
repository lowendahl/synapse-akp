"""DuckDB pack writer adapter — writes compiled projections to a .duckdb file.

What: Creates DuckDB tables for canonical objects, graph, lexical, vectors, and metadata.
Why: Isolates DuckDB dependency behind adapter (ES-03, ADR-003).
Contracts: Implements PackWriter protocol.
Boundaries: ONLY file that imports duckdb.
Test strategy: Integration tests creating temp .duckdb files.
"""

from __future__ import annotations

from pathlib import Path

import duckdb

from kp_compiler.contracts.protocols import GraphResult
from kp_compiler.domain.models import KnowledgeObject, SemanticUnit


class DuckDBPackWriter:
    """Writes Knowledge Pack projections to a DuckDB file."""

    def __init__(self, pack_path: Path) -> None:
        self._path = pack_path
        self._con = duckdb.connect(str(pack_path))
        self._create_schema()

    def _create_schema(self) -> None:
        """Create all pack tables (V1 + V2)."""
        self._con.execute("""
            CREATE TABLE IF NOT EXISTS objects (
                id VARCHAR PRIMARY KEY,
                type VARCHAR NOT NULL,
                title VARCHAR,
                description VARCHAR,
                domain VARCHAR,
                status VARCHAR,
                aliases JSON,
                tags JSON,
                source_path VARCHAR,
                properties JSON
            )
        """)
        self._con.execute("""
            CREATE TABLE IF NOT EXISTS nodes (
                id VARCHAR PRIMARY KEY,
                type VARCHAR NOT NULL,
                title VARCHAR,
                domain VARCHAR,
                source_path VARCHAR,
                pagerank FLOAT,
                in_degree INTEGER,
                out_degree INTEGER
            )
        """)
        self._con.execute("""
            CREATE TABLE IF NOT EXISTS edges (
                subject_id VARCHAR NOT NULL,
                predicate VARCHAR NOT NULL,
                object_id VARCHAR NOT NULL,
                origin VARCHAR NOT NULL,
                confidence FLOAT
            )
        """)
        self._con.execute("""
            CREATE TABLE IF NOT EXISTS semantic_units (
                id VARCHAR PRIMARY KEY,
                source_object_id VARCHAR NOT NULL,
                heading_path VARCHAR,
                content VARCHAR,
                context VARCHAR,
                object_type VARCHAR,
                domain VARCHAR
            )
        """)
        self._con.execute("""
            CREATE TABLE IF NOT EXISTS aliases (
                alias VARCHAR NOT NULL,
                canonical_id VARCHAR NOT NULL,
                alias_type VARCHAR DEFAULT 'exact'
            )
        """)
        self._con.execute("""
            CREATE TABLE IF NOT EXISTS manifest (
                key VARCHAR PRIMARY KEY,
                value VARCHAR
            )
        """)
        # V2 tables
        self._con.execute("""
            CREATE TABLE IF NOT EXISTS bm25_tokens (
                unit_id VARCHAR NOT NULL,
                tokens JSON NOT NULL
            )
        """)
        self._con.execute("""
            CREATE TABLE IF NOT EXISTS vector_metadata (
                unit_id VARCHAR PRIMARY KEY,
                model_name VARCHAR NOT NULL,
                model_version VARCHAR NOT NULL,
                dimensions INTEGER NOT NULL,
                input_hash VARCHAR NOT NULL
            )
        """)
        self._con.execute("""
            CREATE TABLE IF NOT EXISTS cross_pack_refs (
                source_id VARCHAR NOT NULL,
                target_qualified_id VARCHAR NOT NULL,
                target_pack VARCHAR NOT NULL,
                predicate VARCHAR NOT NULL DEFAULT 'references',
                resolved BOOLEAN DEFAULT FALSE
            )
        """)

    def write_objects(self, objects: list[KnowledgeObject]) -> None:
        """Write canonical object table."""
        import orjson

        for obj in objects:
            if not obj.id:
                continue
            self._con.execute(
                "INSERT OR REPLACE INTO objects VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                [
                    obj.id,
                    obj.type.value,
                    obj.title,
                    obj.description,
                    obj.domain,
                    obj.status,
                    orjson.dumps(obj.aliases).decode(),
                    orjson.dumps(obj.tags).decode(),
                    obj.source_path,
                    orjson.dumps(obj.properties).decode(),
                ],
            )

    def write_graph(self, result: GraphResult) -> None:
        """Write node and edge tables."""
        for node in result.nodes:
            self._con.execute(
                "INSERT OR REPLACE INTO nodes VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                [
                    node.id,
                    node.type,
                    node.title,
                    node.domain,
                    node.source_path,
                    node.pagerank,
                    node.in_degree,
                    node.out_degree,
                ],
            )
        for edge in result.edges:
            self._con.execute(
                "INSERT INTO edges VALUES (?, ?, ?, ?, ?)",
                [
                    edge.subject_id,
                    edge.predicate,
                    edge.object_id,
                    edge.origin,
                    edge.confidence,
                ],
            )

    def write_semantic_units(self, units: list[SemanticUnit]) -> None:
        """Write semantic unit table."""
        for unit in units:
            self._con.execute(
                "INSERT OR REPLACE INTO semantic_units VALUES (?, ?, ?, ?, ?, ?, ?)",
                [unit.id, unit.source_object_id, unit.heading_path,
                 unit.content, unit.context, unit.object_type, unit.domain],
            )

    def write_aliases(self, aliases: list[tuple[str, str, str]]) -> None:
        """Write alias registry. Each tuple: (alias, canonical_id, alias_type)."""
        for alias, canonical_id, alias_type in aliases:
            self._con.execute(
                "INSERT INTO aliases VALUES (?, ?, ?)",
                [alias.lower(), canonical_id, alias_type],
            )

    def write_bm25_tokens(self, unit_ids: list[str], corpus_tokens: list[list[str]]) -> None:
        """Write BM25 tokenized corpus for consumer-side retrieval."""
        import orjson

        for unit_id, tokens in zip(unit_ids, corpus_tokens):
            self._con.execute(
                "INSERT INTO bm25_tokens VALUES (?, ?)",
                [unit_id, orjson.dumps(tokens).decode()],
            )

    def write_vector_metadata(
        self,
        unit_ids: list[str],
        model_name: str,
        dimensions: int,
        input_hashes: list[str],
    ) -> None:
        """Write vector provenance metadata (vectors live in .usearch sidecar)."""
        model_version = "1.0"
        for unit_id, input_hash in zip(unit_ids, input_hashes):
            self._con.execute(
                "INSERT OR REPLACE INTO vector_metadata VALUES (?, ?, ?, ?, ?)",
                [unit_id, model_name, model_version, dimensions, input_hash],
            )

    def write_cross_pack_refs(
        self,
        refs: list[tuple[str, str, str, str]],
        resolved_ids: set[str] | None = None,
    ) -> None:
        """Write cross-pack reference table."""
        resolved_ids = resolved_ids or set()
        for source_id, target_id, target_pack, predicate in refs:
            self._con.execute(
                "INSERT INTO cross_pack_refs VALUES (?, ?, ?, ?, ?)",
                [source_id, target_id, target_pack,
                 predicate or "references", target_id in resolved_ids],
            )

    def write_manifest(self, manifest: dict) -> None:
        """Write build manifest as key-value pairs."""
        for key, value in manifest.items():
            self._con.execute(
                "INSERT OR REPLACE INTO manifest VALUES (?, ?)",
                [key, str(value)],
            )

    def close(self) -> None:
        """Finalize and close the pack file."""
        self._con.close()
