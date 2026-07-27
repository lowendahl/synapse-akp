"""Re-export facade — all MCP models available from their canonical locations.

Canonical sources:
- mcp_config.py: PackBindingModel, RuntimeConfigModel
- mcp_search.py: SearchToolInput, ChannelScoreModel, SearchResultModel, SearchToolOutput
- mcp_lookup.py: LookupConceptToolInput, ConceptUnitModel, LookupConceptToolOutput
- mcp_graph.py: ExpandGraphToolInput, GraphEdgeModel, ExpandGraphToolOutput
- mcp_provenance.py: ProvenanceStepModel, GetProvenanceToolInput, GetProvenanceToolOutput
"""

from akp_runtime.contracts.mcp_config import PackBindingModel, RuntimeConfigModel
from akp_runtime.contracts.mcp_graph import ExpandGraphToolInput, ExpandGraphToolOutput, GraphEdgeModel
from akp_runtime.contracts.mcp_lookup import ConceptUnitModel, LookupConceptToolInput, LookupConceptToolOutput
from akp_runtime.contracts.mcp_provenance import GetProvenanceToolInput, GetProvenanceToolOutput, ProvenanceStepModel
from akp_runtime.contracts.mcp_search import ChannelScoreModel, SearchResultModel, SearchToolInput, SearchToolOutput


class _McpModelExports:
    """Marker class preserving class-based module shape for the facade."""


__all__ = [
    "PackBindingModel",
    "RuntimeConfigModel",
    "SearchToolInput",
    "ChannelScoreModel",
    "SearchResultModel",
    "SearchToolOutput",
    "LookupConceptToolInput",
    "ConceptUnitModel",
    "LookupConceptToolOutput",
    "ExpandGraphToolInput",
    "GraphEdgeModel",
    "ExpandGraphToolOutput",
    "ProvenanceStepModel",
    "GetProvenanceToolInput",
    "GetProvenanceToolOutput",
]
