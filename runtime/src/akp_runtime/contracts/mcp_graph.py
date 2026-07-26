"""MCP graph models — input and output contracts for the expand-graph tool."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from akp_runtime.contracts.mcp_provenance import ProvenanceStepModel


class ExpandGraphToolInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    object_id: str = Field(min_length=1)
    pack_ids: list[str] = Field(default_factory=list)
    hops: int = Field(default=1, ge=1, le=3)
    predicates: list[str] = Field(default_factory=list)
    limit: int = Field(default=20, ge=1, le=100)


class GraphEdgeModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pack_id: str
    subject_id: str
    predicate: str
    object_id: str
    origin: Literal["authored", "derived", "inferred", "generated"]
    confidence: float | None = None
    neighbor_title: str | None = None
    neighbor_type: str | None = None
    provenance: list[ProvenanceStepModel]


class ExpandGraphToolOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    seed_object_id: str
    hops: int
    edges: list[GraphEdgeModel]
