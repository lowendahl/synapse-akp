"""Core domain models — structural building blocks of the compiler IR."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from kp_compiler.domain.enumerations import Origin


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
    compiler_version: str = "0.2.0"
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
