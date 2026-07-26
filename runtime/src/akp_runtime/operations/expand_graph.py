"""Graph expansion operation — N-hop BFS over preloaded adjacency."""

from __future__ import annotations

from akp_runtime.contracts.mcp_models import ExpandGraphToolInput
from akp_runtime.domain.models import GraphEdgeHit


class GraphExpansionOperation:
    """Traverses the knowledge graph from a seed object."""

    def expand(self, request: ExpandGraphToolInput) -> tuple[GraphEdgeHit, ...]:
        raise NotImplementedError("PBI #9")
