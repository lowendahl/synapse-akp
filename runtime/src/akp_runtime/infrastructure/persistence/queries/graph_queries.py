"""Graph traversal queries for knowledge pack edges.

What: Query objects for edge retrieval and graph neighbor discovery.
Why: Confines graph SQL to query files; supports BFS traversal.
"""

from __future__ import annotations

from typing import Any

from akp_runtime.infrastructure.persistence.queries.base import PackQuery


class EdgesFromNodeQuery(PackQuery[list[tuple]]):
    """Fetch outgoing edges from a node, optionally filtered by predicate."""

    def __init__(self, node_id: str, predicates: tuple[str, ...] = ()) -> None:
        self._node_id = node_id
        self._predicates = predicates

    def sql(self) -> str:
        if self._predicates:
            placeholders = ", ".join(["?"] * len(self._predicates))
            return f"""
                SELECT e.subject_id, e.predicate, e.object_id, e.origin, e.confidence,
                       o.title, o.type
                FROM edges e
                LEFT JOIN objects o ON e.object_id = o.id
                WHERE e.subject_id = ? AND e.predicate IN ({placeholders})
            """
        return """
            SELECT e.subject_id, e.predicate, e.object_id, e.origin, e.confidence,
                   o.title, o.type
            FROM edges e
            LEFT JOIN objects o ON e.object_id = o.id
            WHERE e.subject_id = ?
        """

    def parameters(self) -> list[Any]:
        if self._predicates:
            return [self._node_id, *self._predicates]
        return [self._node_id]

    def map_results(self, rows: list[tuple]) -> list[tuple]:
        return rows


class EdgeProvenanceQuery(PackQuery[list[tuple]]):
    """Retrieve origin and confidence for a specific edge."""

    def __init__(self, subject_id: str, predicate: str, object_id: str) -> None:
        self._subject_id = subject_id
        self._predicate = predicate
        self._object_id = object_id

    def sql(self) -> str:
        return "SELECT origin, confidence FROM edges WHERE subject_id = ? AND predicate = ? AND object_id = ?"

    def parameters(self) -> list[Any]:
        return [self._subject_id, self._predicate, self._object_id]

    def map_results(self, rows: list[tuple]) -> list[tuple]:
        return rows
