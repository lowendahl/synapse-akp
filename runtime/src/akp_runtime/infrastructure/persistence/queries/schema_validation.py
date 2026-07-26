"""Schema validation queries for pack initialization.

What: Queries that validate pack schema during load.
Why: Fail fast if the DuckDB file is malformed or incompatible.
"""

from __future__ import annotations

from typing import Any

from akp_runtime.infrastructure.persistence.queries.base import PackQuery


class ListTablesQuery(PackQuery[set[str]]):
    """Retrieve all table names in the main schema."""

    def sql(self) -> str:
        return "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'"

    def parameters(self) -> list[Any]:
        return []

    def map_results(self, rows: list[tuple]) -> set[str]:
        return {row[0] for row in rows}


class LoadManifestQuery(PackQuery[dict[str, str]]):
    """Load all key-value pairs from the manifest table."""

    def sql(self) -> str:
        return "SELECT key, value FROM manifest"

    def parameters(self) -> list[Any]:
        return []

    def map_results(self, rows: list[tuple]) -> dict[str, str]:
        return {row[0]: row[1] for row in rows}
