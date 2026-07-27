"""Provenance retrieval operation — full lineage chain for any artifact."""

from __future__ import annotations

from akp_runtime.contracts.mcp_provenance import (
    GetProvenanceToolInput,
    GetProvenanceToolOutput,
    ProvenanceStepModel,
)
from akp_runtime.contracts.protocols import LoadedPack


class ProvenanceRetrievalOperation:
    """Retrieves the full provenance chain for an object, unit, or edge."""

    def __init__(self, pack: LoadedPack) -> None:
        self._pack = pack

    def get(self, request: GetProvenanceToolInput) -> GetProvenanceToolOutput:
        """Resolve provenance for the specified target."""
        if request.object_id is not None:
            steps = self._pack.provenance_for_object(request.object_id)
            target_type = "object"
            target_id = request.object_id
        elif request.unit_id is not None:
            steps = self._pack.provenance_for_unit(request.unit_id)
            target_type = "semantic_unit"
            target_id = request.unit_id
        else:
            steps = self._pack.provenance_for_edge(
                request.edge_subject_id,  # type: ignore[arg-type]
                request.edge_predicate,  # type: ignore[arg-type]
                request.edge_object_id,  # type: ignore[arg-type]
            )
            target_type = "edge"
            target_id = f"{request.edge_subject_id}--{request.edge_predicate}-->{request.edge_object_id}"

        provenance = [
            ProvenanceStepModel(
                layer=s.layer,
                identifier=s.identifier,
                origin=s.origin,
                source_path=s.source_path,
                pack_id=s.pack_id,
                pack_version=s.pack_version,
            )
            for s in steps
        ]

        return GetProvenanceToolOutput(
            target_type=target_type,  # type: ignore[arg-type]
            target_id=target_id,
            provenance=provenance,
        )
