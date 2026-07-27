"""Query objects for stage-level outcome validation."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module

from kp_compiler.contracts.infrastructure_protocols import QueryProtocol


class InfrastructureOutcomeQueryProvider:
    """Loads infrastructure query implementations for stage-safe delegation."""

    @staticmethod
    def resolve(query_name: str) -> type[QueryProtocol[object]]:
        module = import_module("kp_compiler.infrastructure.queries.outcome_queries")
        return getattr(module, query_name)


@dataclass(frozen=True)
class ExplicitAliasLookupQuery(QueryProtocol[list[tuple[object, ...]]]):
    """Load explicit aliases and their owners."""

    def execute(self, connection: object) -> list[tuple[object, ...]]:
        return InfrastructureOutcomeQueryProvider.resolve("ExplicitAliasLookupQuery")().execute(connection)


@dataclass(frozen=True)
class TopAliasLookupQuery(QueryProtocol[list[tuple[object, ...]]]):
    """Load top alias matches for a lookup value."""

    alias_text: str
    limit: int

    def execute(self, connection: object) -> list[tuple[object, ...]]:
        return InfrastructureOutcomeQueryProvider.resolve("TopAliasLookupQuery")(self.alias_text, self.limit).execute(
            connection
        )


@dataclass(frozen=True)
class ObjectCountQuery(QueryProtocol[tuple[object, ...] | None]):
    """Load the number of compiled objects."""

    def execute(self, connection: object) -> tuple[object, ...] | None:
        return InfrastructureOutcomeQueryProvider.resolve("ObjectCountQuery")().execute(connection)


@dataclass(frozen=True)
class TagCoverageQuery(QueryProtocol[list[tuple[object, ...]]]):
    """Load object counts grouped by tag alias."""

    def execute(self, connection: object) -> list[tuple[object, ...]]:
        return InfrastructureOutcomeQueryProvider.resolve("TagCoverageQuery")().execute(connection)


@dataclass(frozen=True)
class ExistingObjectTitlesQuery(QueryProtocol[list[tuple[object, ...]]]):
    """Load object identifiers and titles."""

    def execute(self, connection: object) -> list[tuple[object, ...]]:
        return InfrastructureOutcomeQueryProvider.resolve("ExistingObjectTitlesQuery")().execute(connection)


@dataclass(frozen=True)
class OrphanAliasQuery(QueryProtocol[list[tuple[object, ...]]]):
    """Load aliases that point to missing objects."""

    limit: int = 20

    def execute(self, connection: object) -> list[tuple[object, ...]]:
        return InfrastructureOutcomeQueryProvider.resolve("OrphanAliasQuery")(self.limit).execute(connection)
