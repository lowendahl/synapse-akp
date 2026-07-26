"""Immutable domain models for runtime operations.

What: Frozen dataclasses for pack metadata, retrieval results, and provenance.
Why: Value semantics ensure deterministic, hashable, thread-safe domain objects.
Contracts: All models are deeply immutable — tuples for collections, MappingProxyType for metadata.
Boundaries: No IO, no infrastructure imports. MCP boundary models convert to/from these.
Test strategy: Unit tests verify immutability, equality, hashing, and construction.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Literal

SourceKind = Literal["authored", "derived", "inferred", "generated"]

# Type alias for deeply-immutable metadata values
MetadataValue = str | int | float | bool | tuple[str, ...]
MetadataMap = MappingProxyType[str, MetadataValue]

_EMPTY_METADATA: MetadataMap = MappingProxyType({})


def _freeze_metadata(
    raw: dict[str, str | int | float | bool | list[str] | tuple[str, ...]] | None,
) -> MetadataMap:
    """Convert a mutable metadata dict to a deeply-immutable MappingProxyType."""
    if not raw:
        return _EMPTY_METADATA
    frozen: dict[str, MetadataValue] = {}
    for k, v in raw.items():
        frozen[k] = tuple(v) if isinstance(v, list) else v
    return MappingProxyType(frozen)


@dataclass(frozen=True)
class PackMetadata:
    """Validated manifest data for a loaded Knowledge Pack."""

    pack_id: str
    pack_version: str
    schema_version: str
    compiler_version: str
    path: Path
    content_hash: str = ""
    ontology_version: str = ""
    build_timestamp: str = ""
    source_file_count: int = 0
    object_count: int = 0
    node_count: int = 0
    edge_count: int = 0
    semantic_unit_count: int = 0
    alias_count: int = 0
    bm25_vocab_size: int = 0
    embedding_model: str = ""
    embedding_dimensions: int = 0
    cross_pack_refs: int = 0
    error_count: int = 0
    warning_count: int = 0


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
    _metadata: MetadataMap = field(default=_EMPTY_METADATA, repr=False)

    def __init__(
        self,
        layer: str,
        identifier: str,
        origin: SourceKind,
        source_path: str | None = None,
        source_revision: str | None = None,
        pack_id: str | None = None,
        pack_version: str | None = None,
        metadata: dict[str, str | int | float | bool | list[str] | tuple[str, ...]] | None = None,
    ) -> None:
        object.__setattr__(self, "layer", layer)
        object.__setattr__(self, "identifier", identifier)
        object.__setattr__(self, "origin", origin)
        object.__setattr__(self, "source_path", source_path)
        object.__setattr__(self, "source_revision", source_revision)
        object.__setattr__(self, "pack_id", pack_id)
        object.__setattr__(self, "pack_version", pack_version)
        object.__setattr__(self, "_metadata", _freeze_metadata(metadata))

    @property
    def metadata(self) -> MetadataMap:
        """Deeply-immutable metadata mapping."""
        return self._metadata


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
