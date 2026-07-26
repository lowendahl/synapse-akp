"""Pydantic v2 domain models — the compiler's typed intermediate representation.

What: Defines all knowledge object types as Pydantic models.
Why: Provides typed validation, schema enforcement, and serialization (ADR-008).
Contracts: These ARE the IR that all stages consume and produce.
Boundaries: Must NOT import from infrastructure/ or perform IO.
Test strategy: Unit tests validate construction, serialization, and constraints.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ObjectType(str, Enum):
    """Allowed object types per ontology.yaml."""

    FRAMEWORK = "Framework"
    STAGE = "Stage"
    METHODOLOGY = "Methodology"
    STRATEGY = "Strategy"
    ORGANIZATION = "Organization"
    ROLE = "Role"
    PROCESS = "Process"
    METRIC = "Metric"
    KPI = "KPI"
    DOCTRINE = "Doctrine"
    PROGRAM = "Program"
    OUTCOME = "Outcome"
    EVIDENCE_SOURCE = "Evidence Source"
    EVIDENCE_MAP = "Evidence Map"
    RISK = "Risk"
    PRIORITY = "Priority"
    PLANNING = "Planning"
    TAXONOMY = "Taxonomy"
    PIPELINE = "Pipeline"
    GOVERNANCE = "Governance"
    GTM = "GTM"
    CONTRACT = "Contract"
    DELIVERY = "Delivery"
    MEASUREMENT = "Measurement"
    ADR = "ADR"
    INDEX = "Index"
    LOG = "Log"


class Origin(str, Enum):
    """How a relationship or object was created."""

    AUTHORED = "authored"
    DERIVED = "derived"
    INFERRED = "inferred"
    GENERATED = "generated"


class MeasurementParadigm(str, Enum):
    """How a metric is measured."""

    SNAPSHOT = "snapshot"
    REALTIME = "realtime"


class Classification(str, Enum):
    """KPI classification."""

    LEADING = "leading"
    LAGGING = "lagging"
    DIAGNOSTIC = "diagnostic"


# ─── Core Models ────────────────────────────────────────────────────────────


class Relationship(BaseModel):
    """A typed relationship between two knowledge objects."""

    model_config = ConfigDict(frozen=True)

    subject_id: str
    predicate: str
    object_id: str
    origin: Origin = Origin.AUTHORED
    confidence: Optional[float] = None
    source_file: Optional[str] = None


class Section(BaseModel):
    """A heading-delimited section within a document."""

    model_config = ConfigDict(frozen=True)

    heading: str
    level: int
    content: str
    source_line: Optional[int] = None


class Provenance(BaseModel):
    """Tracks where a compiled object came from (CP-09)."""

    model_config = ConfigDict(frozen=True)

    source_file: str
    source_revision: Optional[str] = None
    compiler_version: str = "0.1.0"
    stage: str = "parse"
    origin: Origin = Origin.AUTHORED
    timestamp: Optional[datetime] = None


class SemanticUnit(BaseModel):
    """A meaning-aligned chunk for embedding and retrieval."""

    model_config = ConfigDict(frozen=True)

    id: str
    source_object_id: str
    heading_path: str
    content: str
    context: str = ""
    object_type: str = ""
    domain: str = ""


# ─── Knowledge Object (Base) ───────────────────────────────────────────────


class KnowledgeObject(BaseModel):
    """Base model for all canonical knowledge objects in the IR."""

    model_config = ConfigDict(frozen=False)

    id: str
    type: ObjectType
    title: str
    description: str = ""
    aliases: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    domain: str = ""
    status: str = "stable"
    source_path: str = ""
    provenance: Optional[Provenance] = None
    relationships: list[Relationship] = Field(default_factory=list)
    sections: list[Section] = Field(default_factory=list)
    properties: dict = Field(default_factory=dict)
    raw_body: str = ""


# ─── Specialized Object Types ──────────────────────────────────────────────


class MetricObject(KnowledgeObject):
    """Extended model for Metric and KPI type objects."""

    formula: Optional[str] = None
    classification: Optional[Classification] = None
    thresholds: Optional[dict] = None
    measurement_paradigm: Optional[MeasurementParadigm] = None
    evidence_sources: list[str] = Field(default_factory=list)


class EvidenceSourceObject(KnowledgeObject):
    """Extended model for Evidence Source type objects."""

    platform: Optional[str] = None
    access_pattern: Optional[str] = None
    artifact_ids: list[str] = Field(default_factory=list)


class RoleObject(KnowledgeObject):
    """Extended model for Role type objects."""

    responsibilities: list[str] = Field(default_factory=list)


class ProcessObject(KnowledgeObject):
    """Extended model for Process type objects."""

    steps: list[str] = Field(default_factory=list)
