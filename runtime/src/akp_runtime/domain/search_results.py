"""Search result domain models.

What: Frozen dataclasses for search hits, channel scores, and graph edges.
Why: Value semantics ensure deterministic, hashable, thread-safe results.
Boundaries: No IO, no infrastructure imports.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from akp_runtime.domain.provenance_models import ProvenanceStep, SourceKind

ChannelName = Literal["lexical", "semantic", "exact_alias", "graph"]


@dataclass(frozen=True)
class ChannelScore:
    """Score contribution from a single retrieval channel."""

    channel: str
    rank: int | None
    raw_score: float
    contribution: float


@dataclass(frozen=True)
class SemanticUnitRecord:
    """A semantic unit extracted from a knowledge object."""

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
class SearchHit:
    """A scored search result with full provenance chain."""

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
    """A graph edge result with neighbor context."""

    pack_id: str
    subject_id: str
    predicate: str
    object_id: str
    origin: SourceKind
    confidence: float | None
    neighbor_title: str | None
    neighbor_type: str | None
    provenance: tuple[ProvenanceStep, ...]
