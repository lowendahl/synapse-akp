"""Query objects for pack search workflows."""

from __future__ import annotations

from dataclasses import dataclass

from kp_compiler.contracts.infrastructure_protocols import QueryProtocol


@dataclass(frozen=True)
class AliasSearchQuery(QueryProtocol[list[tuple[object, ...]]]):
    """Load alias hits for a search term."""

    query_text: str
    limit: int = 10

    def execute(self, connection: object) -> list[tuple[object, ...]]:
        return connection.execute(
            """
            SELECT a.canonical_id, a.alias, a.alias_type, o.title, o.type, o.description
            FROM aliases a
            JOIN objects o ON a.canonical_id = o.id
            WHERE LOWER(a.alias) = LOWER(?)
               OR LOWER(a.alias) LIKE LOWER(?)
            LIMIT ?
            """,
            [self.query_text, f"%{self.query_text}%", self.limit],
        ).fetchall()


@dataclass(frozen=True)
class SemanticUnitCorpusQuery(QueryProtocol[list[tuple[object, ...]]]):
    """Load semantic units for lexical retrieval."""

    def execute(self, connection: object) -> list[tuple[object, ...]]:
        return connection.execute(
            """
            SELECT su.id, su.heading_path, su.content, su.context, o.title, o.type
            FROM semantic_units su
            JOIN objects o ON su.source_object_id = o.id
            """
        ).fetchall()


@dataclass(frozen=True)
class VectorUnitIdentifiersQuery(QueryProtocol[list[tuple[object, ...]]]):
    """Load semantic-unit ordering for vector metadata."""

    def execute(self, connection: object) -> list[tuple[object, ...]]:
        return connection.execute("SELECT unit_id FROM vector_metadata ORDER BY rowid").fetchall()


@dataclass(frozen=True)
class VectorModelNameQuery(QueryProtocol[tuple[object, ...] | None]):
    """Load the embedding model name for a pack."""

    def execute(self, connection: object) -> tuple[object, ...] | None:
        return connection.execute("SELECT model_name FROM vector_metadata LIMIT 1").fetchone()


@dataclass(frozen=True)
class SemanticUnitByIdentifierQuery(QueryProtocol[tuple[object, ...] | None]):
    """Load a semantic unit and owning object by identifier."""

    unit_identifier: str

    def execute(self, connection: object) -> tuple[object, ...] | None:
        return connection.execute(
            """
            SELECT su.heading_path, su.content, o.title, o.type
            FROM semantic_units su
            JOIN objects o ON su.source_object_id = o.id
            WHERE su.id = ?
            """,
            [self.unit_identifier],
        ).fetchone()


@dataclass(frozen=True)
class ObjectSearchQuery(QueryProtocol[list[tuple[object, ...]]]):
    """Load object hits for fallback search."""

    query_text: str
    limit: int = 10

    def execute(self, connection: object) -> list[tuple[object, ...]]:
        query_value = f"%{self.query_text}%"
        return connection.execute(
            """
            SELECT id, type, title, description, domain
            FROM objects
            WHERE LOWER(title) LIKE LOWER(?)
               OR LOWER(description) LIKE LOWER(?)
            ORDER BY
                CASE WHEN LOWER(title) LIKE LOWER(?) THEN 0 ELSE 1 END,
                LENGTH(title)
            LIMIT ?
            """,
            [query_value, query_value, query_value, self.limit],
        ).fetchall()


@dataclass(frozen=True)
class GraphExpansionQuery(QueryProtocol[list[tuple[object, ...]]]):
    """Load direct graph neighbors for an object."""

    object_identifier: str
    limit: int = 30

    def execute(self, connection: object) -> list[tuple[object, ...]]:
        return connection.execute(
            """
            SELECT e.subject_id, e.predicate, e.object_id, o.title, o.type
            FROM edges e
            LEFT JOIN objects o ON (
                CASE WHEN e.subject_id = ? THEN e.object_id ELSE e.subject_id END
            ) = o.id
            WHERE e.subject_id = ? OR e.object_id = ?
            LIMIT ?
            """,
            [self.object_identifier, self.object_identifier, self.object_identifier, self.limit],
        ).fetchall()
