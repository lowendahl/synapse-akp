"""MCP provenance models — input and output contracts for the get-provenance tool."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ProvenanceStepModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    layer: Literal["pack", "package", "object", "semantic_unit", "edge", "embedding", "retrieval"]
    identifier: str
    origin: Literal["authored", "derived", "inferred", "generated"]
    source_path: str | None = None
    source_revision: str | None = None
    pack_id: str | None = None
    pack_version: str | None = None
    metadata: dict[str, str | int | float | bool | list[str]] = Field(default_factory=dict)


class GetProvenanceToolInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pack_id: str | None = None
    object_id: str | None = None
    unit_id: str | None = None
    edge_subject_id: str | None = None
    edge_predicate: str | None = None
    edge_object_id: str | None = None

    @model_validator(mode="after")
    def validate_target(self) -> GetProvenanceToolInput:
        has_object = self.object_id is not None
        has_unit = self.unit_id is not None
        has_edge = all(x is not None for x in [self.edge_subject_id, self.edge_predicate, self.edge_object_id])
        if sum([has_object, has_unit, has_edge]) != 1:
            raise ValueError("Provide exactly one provenance target: object, unit, or edge")
        return self


class GetProvenanceToolOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    target_type: Literal["object", "semantic_unit", "edge"]
    target_id: str
    provenance: list[ProvenanceStepModel]
