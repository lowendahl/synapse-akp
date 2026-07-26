"""MCP search models — input and output contracts for the search tool."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from akp_runtime.contracts.mcp_provenance import ProvenanceStepModel


class SearchToolInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=1)
    pack_ids: list[str] = Field(default_factory=list)
    limit: int = Field(default=10, ge=1, le=50)
    include_semantic: bool = True
    include_graph_boost: bool = True
    object_types: list[str] = Field(default_factory=list)
    domains: list[str] = Field(default_factory=list)


class ChannelScoreModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    channel: Literal["exact", "bm25", "semantic", "graph_boost", "object_fallback"]
    rank: int | None = Field(default=None, ge=1)
    raw_score: float
    contribution: float


class SearchResultModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pack_id: str
    pack_version: str
    object_id: str
    unit_id: str | None = None
    title: str
    object_type: str
    domain: str
    heading_path: str | None = None
    snippet: str
    score: float
    source_kind: Literal["authored", "derived", "inferred", "generated"]
    channels: list[ChannelScoreModel]
    provenance: list[ProvenanceStepModel]


class SearchToolOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    results: list[SearchResultModel]
