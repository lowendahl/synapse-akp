"""MCP lookup models — input and output contracts for the lookup-concept tool."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from akp_runtime.contracts.mcp_graph import GraphEdgeModel
from akp_runtime.contracts.mcp_provenance import ProvenanceStepModel


class LookupConceptToolInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    identifier: str = Field(min_length=1)
    pack_ids: list[str] = Field(default_factory=list)
    include_units: bool = True
    include_neighbors: bool = True
    neighbor_limit: int = Field(default=10, ge=1, le=50)


class ConceptUnitModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    unit_id: str
    heading_path: str
    snippet: str


class LookupConceptToolOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pack_id: str
    object_id: str
    title: str
    object_type: str
    domain: str
    description: str
    source_kind: Literal["authored", "derived", "inferred", "generated"]
    units: list[ConceptUnitModel]
    neighbors: list[GraphEdgeModel]
    provenance: list[ProvenanceStepModel]
