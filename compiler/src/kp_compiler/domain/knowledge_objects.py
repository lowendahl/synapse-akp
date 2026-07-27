"""Knowledge object models — the typed IR produced by the parser stage."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from kp_compiler.domain.core_models import Provenance, Relationship, Section
from kp_compiler.domain.enumerations import Classification, MeasurementParadigm, ObjectType


class KnowledgeObject(BaseModel):
    """Base model for all canonical knowledge objects in the IR."""

    model_config = ConfigDict(extra="forbid")

    id: str
    type: ObjectType
    title: str
    description: str = ""
    aliases: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    domain: str = ""
    status: str = "stable"
    source_path: str = ""
    provenance: Provenance | None = None
    relationships: list[Relationship] = Field(default_factory=list)
    sections: list[Section] = Field(default_factory=list)
    properties: dict[str, str | int | float | bool | list[str]] = Field(default_factory=dict)
    raw_body: str = ""


class MetricObject(KnowledgeObject):
    """Extended model for Metric and KPI type objects."""

    formula: str | None = None
    classification: Classification | None = None
    thresholds: dict[str, float] | None = None
    measurement_paradigm: MeasurementParadigm | None = None
    evidence_sources: list[str] = Field(default_factory=list)


class EvidenceSourceObject(KnowledgeObject):
    """Extended model for Evidence Source type objects."""

    platform: str | None = None
    access_pattern: str | None = None
    artifact_ids: list[str] = Field(default_factory=list)


class RoleObject(KnowledgeObject):
    """Extended model for Role type objects."""

    responsibilities: list[str] = Field(default_factory=list)


class ProcessObject(KnowledgeObject):
    """Extended model for Process type objects."""

    steps: list[str] = Field(default_factory=list)
