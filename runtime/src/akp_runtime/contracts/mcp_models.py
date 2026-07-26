"""Pydantic boundary models for MCP tool inputs, outputs, and configuration.

These are the external contracts exposed through the MCP protocol.
All models use extra='forbid' for strict validation.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PackBindingModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pack_id: str = Field(min_length=1)
    path: Path
    required: bool = True


class RuntimeConfigModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    server_name: str = "akp-runtime"
    default_limit: int = Field(default=10, ge=1, le=50)
    lexical_k: int = Field(default=20, ge=1, le=100)
    semantic_k: int = Field(default=20, ge=1, le=100)
    graph_boost_top_n: int = Field(default=3, ge=1, le=10)
    graph_boost_value: float = Field(default=0.1, ge=0.0, le=1.0)
    rrf_k: int = Field(default=60, ge=1, le=200)
    max_hops: int = Field(default=3, ge=1, le=5)
    embeddings_enabled: bool = True
    config_path: Path | None = None
    packs: list[PackBindingModel] = Field(default_factory=list)


class SearchToolInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=1)
    pack_ids: list[str] = Field(default_factory=list)
    limit: int = Field(default=10, ge=1, le=50)
    include_semantic: bool = True
    include_graph_boost: bool = True
    object_types: list[str] = Field(default_factory=list)
    domains: list[str] = Field(default_factory=list)


class LookupConceptToolInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    identifier: str = Field(min_length=1)
    pack_ids: list[str] = Field(default_factory=list)
    include_units: bool = True
    include_neighbors: bool = True
    neighbor_limit: int = Field(default=10, ge=1, le=50)


class ExpandGraphToolInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    object_id: str = Field(min_length=1)
    pack_ids: list[str] = Field(default_factory=list)
    hops: int = Field(default=1, ge=1, le=3)
    predicates: list[str] = Field(default_factory=list)
    limit: int = Field(default=20, ge=1, le=100)


class GetProvenanceToolInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pack_id: str | None = None
    object_id: str | None = None
    unit_id: str | None = None
    edge_subject_id: str | None = None
    edge_predicate: str | None = None
    edge_object_id: str | None = None

    @model_validator(mode="after")
    def validate_target(self) -> "GetProvenanceToolInput":
        has_object = self.object_id is not None
        has_unit = self.unit_id is not None
        has_edge = all([self.edge_subject_id, self.edge_predicate, self.edge_object_id])
        if sum([has_object, has_unit, has_edge]) != 1:
            raise ValueError("Provide exactly one provenance target: object, unit, or edge")
        return self


# ─── Output Models ──────────────────────────────────────────────────────────


class ChannelScoreModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    channel: Literal["exact", "bm25", "semantic", "graph_boost", "object_fallback"]
    rank: int | None = Field(default=None, ge=1)
    raw_score: float
    contribution: float


class ProvenanceStepModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    layer: Literal["package", "object", "semantic_unit", "edge", "embedding", "retrieval"]
    identifier: str
    origin: Literal["authored", "derived", "inferred", "generated"]
    source_path: str | None = None
    source_revision: str | None = None
    pack_id: str | None = None
    pack_version: str | None = None
    metadata: dict[str, str | int | float | bool | list[str]] = Field(default_factory=dict)


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


class ConceptUnitModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    unit_id: str
    heading_path: str
    snippet: str


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


class ExpandGraphToolOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    seed_object_id: str
    hops: int
    edges: list[GraphEdgeModel]


class GetProvenanceToolOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    target_type: Literal["object", "semantic_unit", "edge"]
    target_id: str
    provenance: list[ProvenanceStepModel]
