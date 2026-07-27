"""Domain models for the explain operation.

What: Frozen dataclasses for explanation results and LLM synthesis output.
Why: Value semantics ensure immutable, hashable results consistent with
     the rest of the domain layer.
Boundaries: No IO, no infrastructure imports.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SynthesisResult:
    """Result returned by a SemanticReasoningClient synthesis call."""

    prose: str
    cited_unit_ids: list[str]
    confidence: float


@dataclass(frozen=True)
class ExplainResult:
    """Output of the explain concept operation."""

    concept_title: str
    explanation: str
    cited_unit_ids: list[str]
    synthesis_method: str  # "llm" or "structured_fallback"
    fallback_reason: str | None
    detail_level: str
    neighbor_titles: list[str]


class _ExplainModels:
    """Marker class preserving class-based module shape."""
