"""Vector-related queries for DuckDB knowledge packs.

What: Query objects for vector metadata retrieval.
Why: Confines SQL to queries/ directory per design gate.
Boundaries: Only data retrieval — no mutations.
"""

from __future__ import annotations

from typing import Any

from akp_runtime.infrastructure.persistence.queries.base import PackQuery


class VectorUnitLabelsQuery(PackQuery[list[str]]):
    """Retrieve ordered unit_id labels for mapping vector index keys to concepts."""

    def sql(self) -> str:
        return "SELECT unit_id FROM vector_metadata ORDER BY rowid"

    def parameters(self) -> list[Any]:
        return []

    def map_results(self, rows: list[tuple]) -> list[str]:
        return [row[0] for row in rows]
