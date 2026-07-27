"""Projection writing helpers for DuckDB packs."""

from __future__ import annotations

import duckdb
import orjson

from kp_compiler.contracts.infrastructure_protocols import PackWriter
from kp_compiler.contracts.protocols import GraphResult
from kp_compiler.domain.models import KnowledgeObject, SemanticUnit


class DuckDBProjectionWriter(PackWriter):
    """Writes compiler projections to DuckDB tables. Implements PackWriter protocol."""

    def __init__(self, connection: duckdb.DuckDBPyConnection) -> None:
        self._connection = connection

    def write_objects(self, objects: list[KnowledgeObject]) -> None:
        for obj in objects:
            if obj.id:
                self._connection.execute(
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
        for node in result.nodes:
            self._connection.execute(
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
            self._connection.execute(
                "INSERT INTO edges VALUES (?, ?, ?, ?, ?)",
                [edge.subject_id, edge.predicate, edge.object_id, edge.origin, edge.confidence],
            )

    def write_semantic_units(self, units: list[SemanticUnit]) -> None:
        for unit in units:
            self._connection.execute(
                "INSERT OR REPLACE INTO semantic_units VALUES (?, ?, ?, ?, ?, ?, ?)",
                [
                    unit.id,
                    unit.source_object_id,
                    unit.heading_path,
                    unit.content,
                    unit.context,
                    unit.object_type,
                    unit.domain,
                ],
            )

    def write_aliases(self, aliases: list[tuple[str, str, str]]) -> None:
        for alias, canonical_id, alias_type in aliases:
            self._connection.execute("INSERT INTO aliases VALUES (?, ?, ?)", [alias.lower(), canonical_id, alias_type])

    def write_bm25_tokens(self, unit_ids: list[str], corpus_tokens: list[list[str]]) -> None:
        for unit_id, tokens in zip(unit_ids, corpus_tokens, strict=False):
            self._connection.execute("INSERT INTO bm25_tokens VALUES (?, ?)", [unit_id, orjson.dumps(tokens).decode()])

    def write_vector_metadata(
        self,
        unit_ids: list[str],
        model_name: str,
        dimensions: int,
        input_hashes: list[str],
    ) -> None:
        for unit_id, input_hash in zip(unit_ids, input_hashes, strict=False):
            self._connection.execute(
                "INSERT OR REPLACE INTO vector_metadata VALUES (?, ?, ?, ?, ?)",
                [unit_id, model_name, "1.0", dimensions, input_hash],
            )

    def write_cross_pack_refs(
        self,
        references: list[tuple[str, str, str, str]],
        resolved_ids: set[str] | None = None,
    ) -> None:
        resolved = resolved_ids or set()
        for source_id, target_id, target_pack, predicate in references:
            self._connection.execute(
                "INSERT INTO cross_pack_refs VALUES (?, ?, ?, ?, ?)",
                [source_id, target_id, target_pack, predicate or "references", target_id in resolved],
            )

    def write_manifest(self, manifest: dict) -> None:
        for key, value in manifest.items():
            self._connection.execute("INSERT OR REPLACE INTO manifest VALUES (?, ?)", [key, str(value)])
