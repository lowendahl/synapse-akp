"""Provenance retrieval operation — full lineage chain for any artifact."""

from __future__ import annotations

from akp_runtime.contracts.mcp_models import GetProvenanceToolInput
from akp_runtime.domain.models import ProvenanceStep


class ProvenanceRetrievalOperation:
    """Retrieves the full provenance chain for an object, unit, or edge."""

    def get(self, request: GetProvenanceToolInput) -> tuple[ProvenanceStep, ...]:
        raise NotImplementedError("PBI #10")
