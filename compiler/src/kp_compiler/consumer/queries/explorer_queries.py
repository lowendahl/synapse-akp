"""Query objects for explorer extraction workflows."""

from __future__ import annotations

from dataclasses import dataclass

from kp_compiler.contracts.infrastructure_protocols import QueryProtocol


@dataclass(frozen=True)
class ObjectListQuery(QueryProtocol[list[tuple[object, ...]]]):
    """Load all objects for explorer nodes."""

    def execute(self, connection: object) -> list[tuple[object, ...]]:
        return connection.execute("SELECT id, title, type, domain, description FROM objects").fetchall()


@dataclass(frozen=True)
class EdgeListQuery(QueryProtocol[list[tuple[object, ...]]]):
    """Load all graph edges for explorer links."""

    def execute(self, connection: object) -> list[tuple[object, ...]]:
        return connection.execute("SELECT subject_id, object_id, predicate FROM edges").fetchall()


@dataclass(frozen=True)
class CrossPackReferenceQuery(QueryProtocol[list[tuple[object, ...]]]):
    """Load resolved cross-pack references for explorer links."""

    def execute(self, connection: object) -> list[tuple[object, ...]]:
        return connection.execute(
            """
            SELECT source_id, target_qualified_id, predicate
            FROM cross_pack_refs
            WHERE resolved = true
            """
        ).fetchall()


@dataclass(frozen=True)
class LegacyCrossPackReferenceQuery(QueryProtocol[list[tuple[object, ...]]]):
    """Load resolved cross-pack references from the legacy schema."""

    def execute(self, connection: object) -> list[tuple[object, ...]]:
        return connection.execute(
            """
            SELECT source_id, target_qualified_id, target_pack, resolved
            FROM cross_pack_refs
            WHERE resolved = true
            """
        ).fetchall()


@dataclass(frozen=True)
class SemanticUnitSectionsQuery(QueryProtocol[list[tuple[object, ...]]]):
    """Load semantic units for explorer detail drawers."""

    def execute(self, connection: object) -> list[tuple[object, ...]]:
        return connection.execute(
            """
            SELECT id, source_object_id, heading_path, content
            FROM semantic_units
            ORDER BY source_object_id, id
            """
        ).fetchall()


@dataclass(frozen=True)
class AliasRegistryQuery(QueryProtocol[list[tuple[object, ...]]]):
    """Load aliases for explorer detail drawers."""

    def execute(self, connection: object) -> list[tuple[object, ...]]:
        return connection.execute("SELECT alias, canonical_id, alias_type FROM aliases").fetchall()
