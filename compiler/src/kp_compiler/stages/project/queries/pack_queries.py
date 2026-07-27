"""Query objects for dependency-pack stage reads."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module

from kp_compiler.contracts.infrastructure_protocols import QueryProtocol


class InfrastructurePackQueryProvider:
    """Loads infrastructure query implementations for stage-safe delegation."""

    @staticmethod
    def resolve(query_name: str) -> type[QueryProtocol[object]]:
        module = import_module("kp_compiler.infrastructure.queries.pack_queries")
        return getattr(module, query_name)


@dataclass(frozen=True)
class DependencyObjectIdentifiersQuery(QueryProtocol[list[tuple[object, ...]]]):
    """Load object identifiers from a dependency pack."""

    def execute(self, connection: object) -> list[tuple[object, ...]]:
        return InfrastructurePackQueryProvider.resolve("DependencyObjectIdentifiersQuery")().execute(connection)


@dataclass(frozen=True)
class DependencyDomainQuery(QueryProtocol[tuple[object, ...] | None]):
    """Load a representative identifier for domain inference."""

    def execute(self, connection: object) -> tuple[object, ...] | None:
        return InfrastructurePackQueryProvider.resolve("DependencyDomainQuery")().execute(connection)
