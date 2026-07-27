"""Query objects for compiled-pack metadata reads."""

from __future__ import annotations

from dataclasses import dataclass

from kp_compiler.contracts.infrastructure_protocols import QueryProtocol


@dataclass(frozen=True)
class DependencyObjectIdentifiersQuery(QueryProtocol[list[tuple[object, ...]]]):
    """Load object identifiers from a dependency pack."""

    def execute(self, connection: object) -> list[tuple[object, ...]]:
        return connection.execute("SELECT id FROM objects").fetchall()


@dataclass(frozen=True)
class DependencyDomainQuery(QueryProtocol[tuple[object, ...] | None]):
    """Load a representative object identifier for domain inference."""

    def execute(self, connection: object) -> tuple[object, ...] | None:
        return connection.execute("SELECT id FROM objects LIMIT 1").fetchone()
