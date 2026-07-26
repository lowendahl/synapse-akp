"""Provenance chain assembly.

What: Domain class for building provenance step chains.
Why: Every result must trace back to its knowledge source for explainability.
Contracts: Each step records layer, identifier, origin, and optional metadata.
Boundaries: Imports only from domain/models.py. No IO, no side effects.
"""

from __future__ import annotations

from akp_runtime.domain.models import PackMetadata, ProvenanceStep, SourceKind


class ProvenanceChainBuilder:
    """Assembles provenance step chains from manifest, object, unit, and embedding data.

    Each method creates a single provenance step for one layer of the chain.
    Steps are designed to be composed into ordered lists by the caller.
    """

    def package_step(self, metadata: PackMetadata) -> ProvenanceStep:
        """Create a package-level provenance step from pack metadata."""
        return ProvenanceStep(
            layer="package",
            identifier=metadata.pack_id,
            origin="authored",
            pack_id=metadata.pack_id,
            pack_version=metadata.pack_version,
            metadata={"content_hash": metadata.content_hash},
        )

    def object_step(
        self,
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

    def unit_step(
        self,
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

    def embedding_step(
        self,
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

    def retrieval_step(
        self,
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


# ─── Backward-compatible module-level functions ─────────────────────────────

_builder = ProvenanceChainBuilder()


def package_provenance(meta: PackMetadata) -> ProvenanceStep:
    """Backward-compatible wrapper."""
    return _builder.package_step(meta)


def object_provenance(
    object_id: str,
    source_path: str | None,
    source_kind: SourceKind,
    pack_id: str,
    pack_version: str,
) -> ProvenanceStep:
    """Backward-compatible wrapper."""
    return _builder.object_step(object_id, source_path, source_kind, pack_id, pack_version)


def unit_provenance(unit_id: str, source_kind: SourceKind, pack_id: str) -> ProvenanceStep:
    """Backward-compatible wrapper."""
    return _builder.unit_step(unit_id, source_kind, pack_id)


def embedding_provenance(unit_id: str, model_name: str, dimensions: int, input_hash: str) -> ProvenanceStep:
    """Backward-compatible wrapper."""
    return _builder.embedding_step(unit_id, model_name, dimensions, input_hash)


def retrieval_provenance(query: str, channels_used: list[str], final_score: float) -> ProvenanceStep:
    """Backward-compatible wrapper."""
    return _builder.retrieval_step(query, channels_used, final_score)
