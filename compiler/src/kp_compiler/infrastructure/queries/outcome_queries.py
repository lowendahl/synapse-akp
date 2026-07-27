"""Query objects for outcome validation reads."""

from __future__ import annotations

from dataclasses import dataclass

from kp_compiler.contracts.infrastructure_protocols import QueryProtocol


@dataclass(frozen=True)
class ExplicitAliasLookupQuery(QueryProtocol[list[tuple[object, ...]]]):
    """Load explicit aliases and their owners."""

    def execute(self, connection: object) -> list[tuple[object, ...]]:
        return connection.execute("SELECT alias, canonical_id FROM aliases WHERE alias_type = 'explicit'").fetchall()


@dataclass(frozen=True)
class TopAliasLookupQuery(QueryProtocol[list[tuple[object, ...]]]):
    """Load top alias hits for a lookup value."""

    alias_text: str
    limit: int

    def execute(self, connection: object) -> list[tuple[object, ...]]:
        return connection.execute(
            "SELECT canonical_id FROM aliases WHERE lower(alias) = lower(?) LIMIT ?",
            [self.alias_text, self.limit],
        ).fetchall()


@dataclass(frozen=True)
class ObjectCountQuery(QueryProtocol[tuple[object, ...] | None]):
    """Load the number of compiled objects."""

    def execute(self, connection: object) -> tuple[object, ...] | None:
        return connection.execute("SELECT count(*) FROM objects").fetchone()


@dataclass(frozen=True)
class TagCoverageQuery(QueryProtocol[list[tuple[object, ...]]]):
    """Load object counts grouped by tag alias."""

    def execute(self, connection: object) -> list[tuple[object, ...]]:
        return connection.execute(
            """
            SELECT alias, count(DISTINCT canonical_id) as cnt
            FROM aliases
            WHERE alias_type = 'tag'
            GROUP BY alias
            ORDER BY cnt DESC
            """
        ).fetchall()


@dataclass(frozen=True)
class ExistingObjectTitlesQuery(QueryProtocol[list[tuple[object, ...]]]):
    """Load object identifiers and titles."""

    def execute(self, connection: object) -> list[tuple[object, ...]]:
        return connection.execute("SELECT id, title FROM objects WHERE title IS NOT NULL").fetchall()


@dataclass(frozen=True)
class OrphanAliasQuery(QueryProtocol[list[tuple[object, ...]]]):
    """Load aliases that point to missing objects."""

    limit: int = 20

    def execute(self, connection: object) -> list[tuple[object, ...]]:
        return connection.execute(
            """
            SELECT a.alias, a.canonical_id
            FROM aliases a
            LEFT JOIN objects o ON a.canonical_id = o.id
            WHERE o.id IS NULL
            LIMIT ?
            """,
            [self.limit],
        ).fetchall()
