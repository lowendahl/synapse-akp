"""Immutable domain models for runtime operations — re-export facade.

What: Single import point for all domain model types.
Why: Backward compatibility for existing consumers that import from models.
Boundaries: No IO, no infrastructure imports.
"""

from akp_runtime.domain.pack_metadata import PackMetadata
from akp_runtime.domain.provenance_models import (
    MetadataFreezer,
    MetadataMap,
    MetadataValue,
    ProvenanceStep,
    SourceKind,
)
from akp_runtime.domain.search_results import (
    ChannelScore,
    GraphEdgeHit,
    SearchHit,
    SemanticUnitRecord,
)


class _DomainModelExports:
    """Marker class preserving class-based module shape for the facade."""


# Backward-compatible aliases
_EMPTY_METADATA = MetadataFreezer.freeze(None)
_freeze_metadata = MetadataFreezer.freeze

__all__ = [
    "ChannelScore",
    "GraphEdgeHit",
    "MetadataFreezer",
    "MetadataMap",
    "MetadataValue",
    "PackMetadata",
    "ProvenanceStep",
    "SearchHit",
    "SemanticUnitRecord",
    "SourceKind",
    "_EMPTY_METADATA",
    "_freeze_metadata",
]
