"""Factories for runtime provenance chains."""

from __future__ import annotations

from akp_runtime.contracts.protocols import ProvenanceFactory
from akp_runtime.domain.models import PackMetadata, ProvenanceStep


class PackProvenanceFactory(ProvenanceFactory):
    """Build provenance steps for loaded-pack artifacts."""

    def pack_step(self, metadata: PackMetadata) -> ProvenanceStep:
        return ProvenanceStep(
            layer="pack",
            identifier=metadata.pack_id,
            origin="authored",
            pack_id=metadata.pack_id,
            pack_version=metadata.pack_version,
        )

    def object_steps(self, metadata: PackMetadata, rows: list[tuple[object, ...]]) -> tuple[ProvenanceStep, ...]:
        steps = [self.pack_step(metadata)]
        if rows:
            steps.append(
                ProvenanceStep(
                    layer="object",
                    identifier=rows[0][0],
                    origin="authored",
                    source_path=rows[0][1],
                    pack_id=metadata.pack_id,
                    pack_version=metadata.pack_version,
                )
            )
        return tuple(steps)

    def unit_steps(self, metadata: PackMetadata, rows: list[tuple[object, ...]]) -> tuple[ProvenanceStep, ...]:
        steps = [self.pack_step(metadata)]
        if rows:
            steps.append(
                ProvenanceStep(
                    layer="unit",
                    identifier=rows[0][0],
                    origin="authored",
                    source_path=rows[0][2],
                    pack_id=metadata.pack_id,
                    pack_version=metadata.pack_version,
                )
            )
        return tuple(steps)

    def edge_steps(
        self,
        metadata: PackMetadata,
        rows: list[tuple[object, ...]],
        subject_id: str,
        predicate: str,
        object_id: str,
    ) -> tuple[ProvenanceStep, ...]:
        steps = [self.pack_step(metadata)]
        if rows:
            steps.append(
                ProvenanceStep(
                    layer="edge",
                    identifier=f"{subject_id}--{predicate}-->{object_id}",
                    origin=rows[0][0],
                    pack_id=metadata.pack_id,
                    pack_version=metadata.pack_version,
                    metadata={"confidence": rows[0][1]} if rows[0][1] is not None else None,
                )
            )
        return tuple(steps)
