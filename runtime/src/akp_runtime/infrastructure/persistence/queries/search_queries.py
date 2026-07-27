"""Search queries for knowledge pack retrieval.

What: Query objects for alias match, lexical search, and object lookup.
Why: Confines all SQL to query files; each query is independently testable.
"""

from __future__ import annotations

from typing import Any

from akp_runtime.infrastructure.persistence.queries.base import PackQuery


class ExactAliasMatchQuery(PackQuery[list[tuple]]):
    """Find objects by exact alias match, ordered by resolution_role priority.

    Tie-breaking: role > explicit-over-tag > title contains alias as word boundary > alphabetical.
    """

    _ROLE_PRIORITY = (
        "CASE json_extract_string(o.properties, '$.resolution_role') "
        "WHEN 'concept' THEN 1 WHEN 'measurement' THEN 2 "
        "WHEN 'evidence' THEN 3 ELSE 4 END"
    )
    _ALIAS_TYPE_PRIORITY = (
        "CASE a.alias_type WHEN 'author' THEN 1 WHEN 'explicit' THEN 2 WHEN 'title' THEN 2 WHEN 'tag' THEN 3 ELSE 4 END"
    )

    def __init__(self, alias: str, limit: int) -> None:
        self._alias = alias
        self._limit = limit

    def sql(self) -> str:
        return f"""
            SELECT a.canonical_id, o.type, o.title, o.description, o.domain, o.source_path
            FROM aliases a
            JOIN objects o ON a.canonical_id = o.id
            WHERE LOWER(a.alias) = LOWER(?)
            ORDER BY
                {self._ROLE_PRIORITY},
                {self._ALIAS_TYPE_PRIORITY},
                CASE WHEN LOWER(o.title) = LOWER(?) THEN 0
                     WHEN o.title ILIKE ? OR o.title ILIKE ? THEN 1
                     ELSE 2 END,
                o.title
            LIMIT ?
        """

    def parameters(self) -> list[Any]:
        # Prefer title = alias, then title contains "(ALIAS)" or "ALIAS —", else deprioritize
        return [self._alias, self._alias, f"%({self._alias})%", f"{self._alias} %", self._limit]

    def map_results(self, rows: list[tuple]) -> list[tuple]:
        return rows


class ObjectFallbackQuery(PackQuery[list[tuple]]):
    """Fallback search by object title ILIKE match."""

    def __init__(self, pattern: str, limit: int) -> None:
        self._pattern = f"%{pattern}%"
        self._limit = limit

    def sql(self) -> str:
        return """
            SELECT id, type, title, description, domain, source_path
            FROM objects
            WHERE title ILIKE ?
            LIMIT ?
        """

    def parameters(self) -> list[Any]:
        return [self._pattern, self._limit]

    def map_results(self, rows: list[tuple]) -> list[tuple]:
        return rows


class LexicalSearchQuery(PackQuery[list[tuple]]):
    """BM25 lexical search via content ILIKE (placeholder until BM25 index)."""

    def __init__(self, pattern: str, top_k: int) -> None:
        self._pattern = f"%{pattern}%"
        self._top_k = top_k

    def sql(self) -> str:
        return """
            SELECT su.source_object_id, o.type, o.title, o.description, o.domain, o.source_path
            FROM semantic_units su
            JOIN objects o ON su.source_object_id = o.id
            WHERE su.content ILIKE ?
            LIMIT ?
        """

    def parameters(self) -> list[Any]:
        return [self._pattern, self._top_k]

    def map_results(self, rows: list[tuple]) -> list[tuple]:
        return rows


class LookupObjectQuery(PackQuery[list[tuple]]):
    """Look up an object by exact ID."""

    def __init__(self, object_id: str) -> None:
        self._object_id = object_id

    def sql(self) -> str:
        return "SELECT id, type, title, description, domain, source_path FROM objects WHERE id = ?"

    def parameters(self) -> list[Any]:
        return [self._object_id]

    def map_results(self, rows: list[tuple]) -> list[tuple]:
        return rows


class ConceptUnitsQuery(PackQuery[list[tuple]]):
    """Retrieve semantic units for an object."""

    def __init__(self, object_id: str, limit: int) -> None:
        self._object_id = object_id
        self._limit = limit

    def sql(self) -> str:
        return """
            SELECT su.id, su.source_object_id, su.heading_path, su.content, su.context,
                   su.object_type, su.domain, o.title, o.description, o.source_path
            FROM semantic_units su
            JOIN objects o ON su.source_object_id = o.id
            WHERE su.source_object_id = ?
            LIMIT ?
        """

    def parameters(self) -> list[Any]:
        return [self._object_id, self._limit]

    def map_results(self, rows: list[tuple]) -> list[tuple]:
        return rows
