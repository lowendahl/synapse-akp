"""Concept lookup operation — ID, alias, and title resolution."""

from __future__ import annotations

from akp_runtime.contracts.mcp_models import LookupConceptToolInput
from akp_runtime.domain.models import SearchHit


class ConceptLookupOperation:
    """Resolves a concept by exact ID, alias, or title match."""

    def lookup(self, request: LookupConceptToolInput) -> SearchHit:
        raise NotImplementedError("PBI #8")
