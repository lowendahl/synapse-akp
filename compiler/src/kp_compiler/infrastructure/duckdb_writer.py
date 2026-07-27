"""DuckDB pack writer adapter."""

from __future__ import annotations

from pathlib import Path

import duckdb

from kp_compiler.contracts.protocols import GraphResult, PackWriter
from kp_compiler.domain.models import KnowledgeObject, SemanticUnit
from kp_compiler.infrastructure.duckdb_projection_writer import DuckDBProjectionWriter
from kp_compiler.infrastructure.duckdb_schema_builder import DuckDBSchemaBuilder


class DuckDBPackWriter(PackWriter):
    """Writes compiler outputs to a DuckDB file."""

    def __init__(self, pack_path: Path) -> None:
        self._connection = duckdb.connect(str(pack_path))
        self._schema_builder = DuckDBSchemaBuilder()
        self._projection_writer = DuckDBProjectionWriter(self._connection)
        self._schema_builder.create_schema(self._connection)

    def write_objects(self, objects: list[KnowledgeObject]) -> None:
        self._projection_writer.write_objects(objects)

    def write_graph(self, result: GraphResult) -> None:
        """Write node and edge tables."""
        self._projection_writer.write_graph(result)

    def write_semantic_units(self, units: list[SemanticUnit]) -> None:
        """Write semantic unit table."""
        self._projection_writer.write_semantic_units(units)

    def write_aliases(self, aliases: list[tuple[str, str, str]]) -> None:
        """Write alias registry. Each tuple: (alias, canonical_id, alias_type)."""
        self._projection_writer.write_aliases(aliases)

    def write_bm25_tokens(self, unit_ids: list[str], corpus_tokens: list[list[str]]) -> None:
        """Write BM25 tokenized corpus for consumer-side retrieval."""
        self._projection_writer.write_bm25_tokens(unit_ids, corpus_tokens)

    def write_vector_metadata(
        self,
        unit_ids: list[str],
        model_name: str,
        dimensions: int,
        input_hashes: list[str],
    ) -> None:
        """Write vector provenance metadata (vectors live in .usearch sidecar)."""
        self._projection_writer.write_vector_metadata(unit_ids, model_name, dimensions, input_hashes)

    def write_cross_pack_refs(
        self,
        refs: list[tuple[str, str, str, str]],
        resolved_ids: set[str] | None = None,
    ) -> None:
        """Write cross-pack reference table."""
        self._projection_writer.write_cross_pack_refs(refs, resolved_ids)

    def write_manifest(self, manifest: dict) -> None:
        """Write build manifest as key-value pairs."""
        self._projection_writer.write_manifest(manifest)

    def close(self) -> None:
        """Finalize and close the pack file."""
        self._connection.close()
