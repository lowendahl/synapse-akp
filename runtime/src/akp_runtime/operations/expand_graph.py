"""Graph expansion operation — N-hop BFS over preloaded adjacency."""

from __future__ import annotations

from akp_runtime.contracts.mcp_graph import (
    ExpandGraphToolInput,
    ExpandGraphToolOutput,
    GraphEdgeModel,
)
from akp_runtime.contracts.mcp_provenance import ProvenanceStepModel
from akp_runtime.contracts.protocols import LoadedPack


class GraphExpansionOperation:
    """Traverses the knowledge graph from a seed object."""

    def __init__(self, pack: LoadedPack) -> None:
        self._pack = pack

    def expand(self, request: ExpandGraphToolInput) -> ExpandGraphToolOutput:
        """Execute N-hop BFS from seed, optionally filtering by predicate."""
        predicates = tuple(request.predicates) if request.predicates else ()
        raw_edges = self._pack.graph_neighbors(
            request.object_id,
            hops=request.hops,
            predicates=predicates,
            limit=request.limit,
        )

        edges = [
            GraphEdgeModel(
                pack_id=e.pack_id,
                subject_id=e.subject_id,
                predicate=e.predicate,
                object_id=e.object_id,
                origin=e.origin or "authored",
                confidence=e.confidence,
                neighbor_title=e.neighbor_title,
                neighbor_type=e.neighbor_type,
                provenance=[
                    ProvenanceStepModel(
                        layer=s.layer,
                        identifier=s.identifier,
                        origin=s.origin,
                        source_path=s.source_path,
                        pack_id=s.pack_id,
                        pack_version=s.pack_version,
                    )
                    for s in (e.provenance or ())
                ],
            )
            for e in raw_edges
        ]

        return ExpandGraphToolOutput(
            seed_object_id=request.object_id,
            hops=request.hops,
            edges=edges,
        )
