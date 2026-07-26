"""Provenance queries for tracing knowledge origin.

What: Query objects for assembling provenance chains.
Why: Every result must trace back to its source for explainability.
"""

from __future__ import annotations

from typing import Any

from akp_runtime.infrastructure.persistence.queries.base import PackQuery


class ObjectProvenanceQuery(PackQuery[list[tuple]]):
    """Retrieve object ID and source path for provenance assembly."""

    def __init__(self, object_id: str) -> None:
        self._object_id = object_id

    def sql(self) -> str:
        return "SELECT id, source_path FROM objects WHERE id = ?"

    def parameters(self) -> list[Any]:
        return [self._object_id]

    def map_results(self, rows: list[tuple]) -> list[tuple]:
        return rows


class UnitProvenanceQuery(PackQuery[list[tuple]]):
    """Retrieve unit ID, source object, and path for provenance assembly."""

    def __init__(self, unit_id: str) -> None:
        self._unit_id = unit_id

    def sql(self) -> str:
        return """
            SELECT su.id, su.source_object_id, o.source_path
            FROM semantic_units su
            LEFT JOIN objects o ON su.source_object_id = o.id
            WHERE su.id = ?
        """

    def parameters(self) -> list[Any]:
        return [self._unit_id]

    def map_results(self, rows: list[tuple]) -> list[tuple]:
        return rows
