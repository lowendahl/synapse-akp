"""Pack metadata domain model.

What: Frozen dataclass representing a validated Knowledge Pack manifest.
Why: Value semantics for pack identity and build metadata.
Boundaries: No IO, no infrastructure imports.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


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
