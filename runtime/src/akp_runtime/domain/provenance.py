"""Provenance chain assembly helpers.

Builds provenance step chains from manifest, object, unit, edge, and embedding data.
"""

from __future__ import annotations

from akp_runtime.domain.models import PackMetadata, ProvenanceStep, SourceKind


def package_provenance(meta: PackMetadata) -> ProvenanceStep:
    """Create a package-level provenance step from pack metadata."""
    return ProvenanceStep(
        layer="package",
        identifier=meta.pack_id,
        origin="authored",
        pack_id=meta.pack_id,
        pack_version=meta.pack_version,
        metadata={"content_hash": meta.content_hash},
    )


def object_provenance(
    object_id: str,
    source_path: str | None,
    source_kind: SourceKind,
    pack_id: str,
    pack_version: str,
) -> ProvenanceStep:
    """Create an object-level provenance step."""
    return ProvenanceStep(
        layer="object",
        identifier=object_id,
        origin=source_kind,
        source_path=source_path,
        pack_id=pack_id,
        pack_version=pack_version,
    )


def unit_provenance(
    unit_id: str,
    source_kind: SourceKind,
    pack_id: str,
) -> ProvenanceStep:
    """Create a semantic-unit-level provenance step."""
    return ProvenanceStep(
        layer="semantic_unit",
        identifier=unit_id,
        origin=source_kind,
        pack_id=pack_id,
    )


def embedding_provenance(
    unit_id: str,
    model_name: str,
    dimensions: int,
    input_hash: str,
) -> ProvenanceStep:
    """Create an embedding-level provenance step."""
    return ProvenanceStep(
        layer="embedding",
        identifier=unit_id,
        origin="generated",
        metadata={
            "model_name": model_name,
            "dimensions": dimensions,
            "input_hash": input_hash,
        },
    )


def retrieval_provenance(
    query: str,
    channels_used: list[str],
    final_score: float,
) -> ProvenanceStep:
    """Create a retrieval-level provenance step (terminal in chain)."""
    return ProvenanceStep(
        layer="retrieval",
        identifier=f"query:{query[:64]}",
        origin="generated",
        metadata={
            "channels": channels_used,
            "final_score": final_score,
        },
    )
