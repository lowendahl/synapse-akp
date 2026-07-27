"""Graph and provenance helpers for loaded packs."""

from __future__ import annotations

from collections import deque
from collections.abc import Callable

from akp_runtime.contracts.protocols import GraphService
from akp_runtime.domain.models import GraphEdgeHit, PackMetadata, ProvenanceStep
from akp_runtime.infrastructure.persistence.queries.base import QueryExecutor
from akp_runtime.infrastructure.persistence.queries.graph_queries import EdgeProvenanceQuery, EdgesFromNodeQuery
from akp_runtime.infrastructure.persistence.queries.provenance_queries import ObjectProvenanceQuery, UnitProvenanceQuery


class DuckDBGraphService(GraphService):
    """Runs graph traversal and provenance queries. Implements GraphService protocol."""

    def __init__(
        self,
        executor: QueryExecutor,
        metadata: PackMetadata,
        provenance_factory: Callable[[], ProvenanceStep],
    ) -> None:
        self._executor = executor
        self._metadata = metadata
        self._provenance_factory = provenance_factory

    def graph_neighbors(
        self,
        object_id: str,
        hops: int,
        predicates: tuple[str, ...],
        limit: int,
    ) -> list[GraphEdgeHit]:
        effective_limit = max(1, limit)
        visited = {object_id}
        frontier: deque[str] = deque([object_id])
        results: list[GraphEdgeHit] = []
        current_hop = 0
        while frontier and current_hop < hops and len(results) < effective_limit:
            next_frontier: deque[str] = deque()
            while frontier and len(results) < effective_limit:
                node = frontier.popleft()
                for edge in self._fetch_edges_from(node, predicates):
                    if edge.object_id not in visited and len(results) < effective_limit:
                        visited.add(edge.object_id)
                        next_frontier.append(edge.object_id)
                        results.append(edge)
            frontier = next_frontier
            current_hop += 1
        return results

    def provenance_for_object(self, object_id: str) -> tuple[ProvenanceStep, ...]:
        rows = self._executor.execute(ObjectProvenanceQuery(object_id))
        steps = [self._provenance_factory()]
        if rows:
            steps.append(
                ProvenanceStep(
                    layer="object",
                    identifier=rows[0][0],
                    origin="authored",
                    source_path=rows[0][1],
                    pack_id=self._metadata.pack_id,
                    pack_version=self._metadata.pack_version,
                )
            )
        return tuple(steps)

    def provenance_for_unit(self, unit_id: str) -> tuple[ProvenanceStep, ...]:
        rows = self._executor.execute(UnitProvenanceQuery(unit_id))
        steps = [self._provenance_factory()]
        if rows:
            steps.append(
                ProvenanceStep(
                    layer="unit",
                    identifier=rows[0][0],
                    origin="authored",
                    source_path=rows[0][2],
                    pack_id=self._metadata.pack_id,
                    pack_version=self._metadata.pack_version,
                )
            )
        return tuple(steps)

    def provenance_for_edge(
        self,
        subject_id: str,
        predicate: str,
        object_id: str,
    ) -> tuple[ProvenanceStep, ...]:
        rows = self._executor.execute(EdgeProvenanceQuery(subject_id, predicate, object_id))
        steps = [self._provenance_factory()]
        if rows:
            steps.append(
                ProvenanceStep(
                    layer="edge",
                    identifier=f"{subject_id}--{predicate}-->{object_id}",
                    origin=rows[0][0],
                    pack_id=self._metadata.pack_id,
                    pack_version=self._metadata.pack_version,
                    metadata={"confidence": rows[0][1]} if rows[0][1] is not None else None,
                )
            )
        return tuple(steps)

    def _fetch_edges_from(self, node_id: str, predicates: tuple[str, ...]) -> list[GraphEdgeHit]:
        rows = self._executor.execute(EdgesFromNodeQuery(node_id, predicates))
        return [
            GraphEdgeHit(
                pack_id=self._metadata.pack_id,
                subject_id=row[0],
                predicate=row[1],
                object_id=row[2],
                origin=row[3],
                confidence=row[4],
                neighbor_title=row[5],
                neighbor_type=row[6],
                provenance=(self._provenance_factory(),),
            )
            for row in rows
        ]
