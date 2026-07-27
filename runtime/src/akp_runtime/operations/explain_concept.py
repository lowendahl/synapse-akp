"""Explain concept operation — human-readable prose from pack content.

What: Resolves a concept, retrieves semantic units, and synthesizes a
     human-readable explanation via LLM or structured fallback.
Why: Humans need coherent narratives, not raw structured data.
Boundaries: Depends on LoadedPack and SemanticReasoningClient protocols only.
"""

from __future__ import annotations

from akp_runtime.contracts.protocols import LoadedPack, SemanticReasoningClient
from akp_runtime.domain.explain_models import ExplainResult
from akp_runtime.domain.search_results import GraphEdgeHit, SearchHit, SemanticUnitRecord

# Heading patterns for detail level filtering
_BRIEF_HEADINGS = ("definition", "summary", "description", "overview")
_STANDARD_HEADINGS = _BRIEF_HEADINGS + (
    "formula",
    "threshold",
    "relationship",
    "context",
    "calculation",
    "metric",
)


class ExplainConceptOperation:
    """Synthesizes human-readable explanations for knowledge pack concepts."""

    def __init__(
        self,
        pack: LoadedPack,
        reasoning_client: SemanticReasoningClient | None,
    ) -> None:
        self._pack = pack
        self._reasoning_client = reasoning_client

    def explain(self, query: str, detail_level: str = "standard") -> ExplainResult | None:
        """Produce a human-readable explanation for a concept.

        Returns None if the query does not resolve to any concept.
        """
        concept = self._resolve_concept(query)
        if concept is None:
            return None

        all_units = self._pack.concept_units(concept.object_id, limit=50)
        neighbors = self._pack.graph_neighbors(concept.object_id, hops=1, predicates=(), limit=20)
        filtered_units = self._filter_units(all_units, detail_level)
        neighbor_titles = self._extract_neighbor_titles(neighbors)

        # Attempt LLM synthesis
        explanation, synthesis_method, fallback_reason = self._synthesize(
            concept, filtered_units, neighbors, detail_level
        )

        cited_unit_ids = [unit.unit_id for unit in filtered_units]

        return ExplainResult(
            concept_title=concept.title,
            explanation=explanation,
            cited_unit_ids=cited_unit_ids,
            synthesis_method=synthesis_method,
            fallback_reason=fallback_reason,
            detail_level=detail_level,
            neighbor_titles=neighbor_titles,
        )

    def _resolve_concept(self, query: str) -> SearchHit | None:
        """Resolve query to a concept via direct lookup then alias fallback."""
        hit = self._pack.lookup_concept(query)
        if hit is not None:
            return hit
        matches = self._pack.exact_matches(query, limit=1)
        if matches:
            return matches[0]
        return None

    def _filter_units(self, units: list[SemanticUnitRecord], detail_level: str) -> list[SemanticUnitRecord]:
        """Filter semantic units by detail level."""
        if detail_level == "detailed":
            return units
        allowed = _STANDARD_HEADINGS if detail_level == "standard" else _BRIEF_HEADINGS
        return [
            unit
            for unit in units
            if unit.heading_path.lower() in allowed or any(heading in unit.heading_path.lower() for heading in allowed)
        ]

    def _extract_neighbor_titles(self, neighbors: list[GraphEdgeHit]) -> list[str]:
        """Extract human-readable titles from graph neighbors."""
        titles: list[str] = []
        for neighbor in neighbors:
            if neighbor.neighbor_title and neighbor.neighbor_title not in titles:
                titles.append(neighbor.neighbor_title)
        return titles

    def _synthesize(
        self,
        concept: SearchHit,
        units: list[SemanticUnitRecord],
        neighbors: list[GraphEdgeHit],
        detail_level: str,
    ) -> tuple[str, str, str | None]:
        """Attempt LLM synthesis, fall back to structured Markdown.

        Returns (explanation, synthesis_method, fallback_reason).
        """
        if self._reasoning_client is None:
            fallback = self._build_fallback(concept, units, neighbors)
            return fallback, "structured_fallback", "no reasoning client configured"

        try:
            result = self._reasoning_client.synthesize_explanation(
                concept_title=concept.title,
                concept_type=concept.object_type,
                semantic_units=units,
                neighbors=neighbors,
                detail_level=detail_level,
            )
            return result.prose, "llm", None
        except NotImplementedError as error:
            fallback = self._build_fallback(concept, units, neighbors)
            return fallback, "structured_fallback", f"reasoning client declined: {error}"
        except Exception as error:  # noqa: BLE001
            fallback = self._build_fallback(concept, units, neighbors)
            return fallback, "structured_fallback", f"reasoning client error: {error}"

    def _build_fallback(
        self,
        concept: SearchHit,
        units: list[SemanticUnitRecord],
        neighbors: list[GraphEdgeHit],
    ) -> str:
        """Assemble structured Markdown from semantic units and neighbors."""
        lines: list[str] = [f"# {concept.title}", ""]

        for unit in units:
            heading = unit.heading_path if unit.heading_path else "Content"
            lines.append(f"## {heading}")
            lines.append("")
            lines.append(unit.content)
            lines.append("")

        neighbor_titles = self._extract_neighbor_titles(neighbors)
        if neighbor_titles:
            lines.append("## Related Concepts")
            lines.append("")
            for title in neighbor_titles:
                lines.append(f"- {title}")
            lines.append("")

        return "\n".join(lines)
