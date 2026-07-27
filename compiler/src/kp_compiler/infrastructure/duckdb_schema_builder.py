"""DuckDB schema creation helpers for pack writing."""

from __future__ import annotations

import duckdb

from kp_compiler.contracts.infrastructure_protocols import SchemaBuilder


class DuckDBSchemaBuilder(SchemaBuilder):
    """Creates the compiled pack schema."""

    def create_schema(self, connection: duckdb.DuckDBPyConnection) -> None:
        for statement in self._statements():
            connection.execute(statement)

    def _statements(self) -> list[str]:
        return [
            "CREATE TABLE IF NOT EXISTS objects ("
            "id VARCHAR PRIMARY KEY, type VARCHAR NOT NULL, title VARCHAR, description VARCHAR, "
            "domain VARCHAR, status VARCHAR, aliases JSON, tags JSON, source_path VARCHAR, properties JSON)",
            "CREATE TABLE IF NOT EXISTS nodes ("
            "id VARCHAR PRIMARY KEY, type VARCHAR NOT NULL, title VARCHAR, domain VARCHAR, "
            "source_path VARCHAR, pagerank FLOAT, in_degree INTEGER, out_degree INTEGER)",
            "CREATE TABLE IF NOT EXISTS edges ("
            "subject_id VARCHAR NOT NULL, predicate VARCHAR NOT NULL, object_id VARCHAR NOT NULL, "
            "origin VARCHAR NOT NULL, confidence FLOAT)",
            "CREATE TABLE IF NOT EXISTS semantic_units ("
            "id VARCHAR PRIMARY KEY, source_object_id VARCHAR NOT NULL, heading_path VARCHAR, "
            "content VARCHAR, context VARCHAR, object_type VARCHAR, domain VARCHAR)",
            "CREATE TABLE IF NOT EXISTS aliases ("
            "alias VARCHAR NOT NULL, canonical_id VARCHAR NOT NULL, alias_type VARCHAR DEFAULT 'exact')",
            "CREATE TABLE IF NOT EXISTS manifest (key VARCHAR PRIMARY KEY, value VARCHAR)",
            "CREATE TABLE IF NOT EXISTS bm25_tokens (unit_id VARCHAR NOT NULL, tokens JSON NOT NULL)",
            "CREATE TABLE IF NOT EXISTS vector_metadata ("
            "unit_id VARCHAR PRIMARY KEY, model_name VARCHAR NOT NULL, model_version VARCHAR NOT NULL, "
            "dimensions INTEGER NOT NULL, input_hash VARCHAR NOT NULL)",
            "CREATE TABLE IF NOT EXISTS cross_pack_refs ("
            "source_id VARCHAR NOT NULL, target_qualified_id VARCHAR NOT NULL, target_pack VARCHAR NOT NULL, "
            "predicate VARCHAR NOT NULL DEFAULT 'references', resolved BOOLEAN DEFAULT FALSE)",
        ]
