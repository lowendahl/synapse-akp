"""Immutable domain models for runtime operations.

Frozen dataclasses ensure value semantics and hashability.
These are the internal representation — MCP boundary models convert to/from these.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

SourceKind = Literal["authored", "derived", "inferred", "generated"]


@dataclass(frozen=True)
class PackMetadata:
    pack_id: str
    pack_version: str
    schema_version: str
    compiler_version: str
    path: Path
    content_hash: str = ""


@dataclass(frozen=True)
class SemanticUnitRecord:
    unit_id: str
    source_object_id: str
    heading_path: str
    content: str
    context: str
    object_type: str
    domain: str
    title: str
    description: str
    source_path: str
    source_kind: SourceKind


@dataclass(frozen=True)
class ChannelScore:
    channel: str
    rank: int | None
    raw_score: float
    contribution: float


@dataclass(frozen=True)
class ProvenanceStep:
    layer: str
    identifier: str
    origin: SourceKind
    source_path: str | None = None
    source_revision: str | None = None
    pack_id: str | None = None
    pack_version: str | None = None
    metadata: dict[str, str | int | float | bool | list[str]] = field(default_factory=dict)


@dataclass(frozen=True)
class SearchHit:
    pack_id: str
    pack_version: str
    object_id: str
    unit_id: str | None
    title: str
    object_type: str
    domain: str
    heading_path: str | None
    snippet: str
    score: float
    source_kind: SourceKind
    channels: tuple[ChannelScore, ...]
    provenance: tuple[ProvenanceStep, ...]


@dataclass(frozen=True)
class GraphEdgeHit:
    pack_id: str
    subject_id: str
    predicate: str
    object_id: str
    origin: SourceKind
    confidence: float | None
    neighbor_title: str | None
    neighbor_type: str | None
    provenance: tuple[ProvenanceStep, ...]
