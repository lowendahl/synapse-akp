"""Concept lookup operation — ID, alias, and title resolution."""

from __future__ import annotations

from akp_runtime.contracts.mcp_graph import GraphEdgeModel
from akp_runtime.contracts.mcp_lookup import (
    ConceptUnitModel,
    LookupConceptToolInput,
    LookupConceptToolOutput,
)
from akp_runtime.contracts.mcp_provenance import ProvenanceStepModel
from akp_runtime.contracts.protocols import LoadedPack


class ConceptLookupOperation:
    """Resolves a concept by exact ID, alias, or title match."""

    def __init__(self, pack: LoadedPack) -> None:
        self._pack = pack

    def lookup(self, request: LookupConceptToolInput) -> LookupConceptToolOutput | None:
        """Resolve identifier → full concept with units and neighbors."""
        hit = self._pack.lookup_concept(request.identifier)
        if hit is None:
            # Try alias resolution
            matches = self._pack.exact_matches(request.identifier, limit=1)
            if matches:
                hit = self._pack.lookup_concept(matches[0].object_id)
        if hit is None:
            return None

        # Semantic units
        units: list[ConceptUnitModel] = []
        if request.include_units:
            raw_units = self._pack.concept_units(hit.object_id, limit=20)
            units = [
                ConceptUnitModel(
                    unit_id=u.unit_id,
                    heading_path=u.heading_path or "",
                    snippet=u.content[:400] if u.content else "",
                )
                for u in raw_units
            ]

        # Graph neighbors
        neighbors: list[GraphEdgeModel] = []
        if request.include_neighbors:
            edges = self._pack.graph_neighbors(
                hit.object_id,
                hops=1,
                predicates=(),
                limit=request.neighbor_limit,
            )
            neighbors = [
                GraphEdgeModel(
                    pack_id=e.pack_id,
                    subject_id=e.subject_id,
                    predicate=e.predicate,
                    object_id=e.object_id,
                    origin=e.origin or "authored",
                    confidence=e.confidence,
                    neighbor_title=e.neighbor_title,
                    neighbor_type=e.neighbor_type,
                    provenance=[
                        ProvenanceStepModel(
                            layer=s.layer,
                            identifier=s.identifier,
                            origin=s.origin,
                            source_path=s.source_path,
                            pack_id=s.pack_id,
                            pack_version=s.pack_version,
                        )
                        for s in (e.provenance or ())
                    ],
                )
                for e in edges
            ]

        # Provenance
        prov_steps = self._pack.provenance_for_object(hit.object_id)
        provenance = [
            ProvenanceStepModel(
                layer=s.layer,
                identifier=s.identifier,
                origin=s.origin,
                source_path=s.source_path,
                pack_id=s.pack_id,
                pack_version=s.pack_version,
            )
            for s in prov_steps
        ]

        return LookupConceptToolOutput(
            pack_id=hit.pack_id,
            object_id=hit.object_id,
            title=hit.title,
            object_type=hit.object_type,
            domain=hit.domain,
            description=hit.snippet or "",
            source_kind=hit.source_kind or "authored",
            units=units,
            neighbors=neighbors,
            provenance=provenance,
        )
