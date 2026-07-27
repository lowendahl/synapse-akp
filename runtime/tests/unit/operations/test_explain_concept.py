"""Tests for the Explain Concept operation (docs/components/explain.md).

These tests are written RED — the implementation does not exist yet.
Every test traces to a promise (P-EXP-*) or invariant (INV-EXP-*) in the
component specification.

ADR: ADR-038 (Explain Operation)
Component: docs/components/explain.md
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable
from unittest.mock import MagicMock

import pytest

from tests.factories import (
    make_graph_edge_hit,
    make_search_hit,
    make_semantic_unit_record,
)

# ─── Stub protocols (stand-ins until real contracts are created) ─────────────
# These mirror what the component spec requires. The implementation phase
# will move these into akp_runtime.contracts.protocols.


@runtime_checkable
class SemanticReasoningClient(Protocol):
    """Protocol for LLM-backed explanation synthesis."""

    def synthesize_explanation(
        self,
        concept_title: str,
        concept_type: str,
        semantic_units: list[object],
        neighbors: list[object],
        detail_level: str,
    ) -> SynthesisResult: ...


@dataclass(frozen=True)
class SynthesisResult:
    """Result from LLM synthesis."""

    prose: str
    cited_unit_ids: list[str]
    confidence: float


@dataclass(frozen=True)
class ExplainResult:
    """Expected output contract for the explain operation."""

    concept_title: str
    explanation: str
    cited_unit_ids: list[str]
    synthesis_method: str  # "llm" or "structured_fallback"
    fallback_reason: str | None  # diagnostic when fallback is used
    detail_level: str
    neighbor_titles: list[str]


# ─── Test fixtures ──────────────────────────────────────────────────────────


@pytest.fixture()
def pack_with_concept() -> MagicMock:
    """A LoadedPack stub that resolves a concept with units and neighbors."""
    pack = MagicMock()
    pack.lookup_concept.return_value = make_search_hit(
        object_id="csu.metric.udc",
        title="Unit Delivery Cost (UDC)",
        object_type="metric",
    )
    pack.exact_matches.return_value = [make_search_hit(object_id="csu.metric.udc", title="Unit Delivery Cost (UDC)")]
    pack.concept_units.return_value = [
        make_semantic_unit_record(
            unit_id="csu.metric.udc::definition",
            heading_path="Definition",
            content="Unit Delivery Cost measures the cost per unit of work delivered.",
            source_object_id="csu.metric.udc",
            title="Unit Delivery Cost (UDC)",
        ),
        make_semantic_unit_record(
            unit_id="csu.metric.udc::formula",
            heading_path="Formula",
            content="UDC = Total Cost / Units Delivered",
            source_object_id="csu.metric.udc",
            title="Unit Delivery Cost (UDC)",
        ),
        make_semantic_unit_record(
            unit_id="csu.metric.udc::thresholds",
            heading_path="Thresholds",
            content="Green: <$500, Yellow: $500-$800, Red: >$800",
            source_object_id="csu.metric.udc",
            title="Unit Delivery Cost (UDC)",
        ),
        make_semantic_unit_record(
            unit_id="csu.metric.udc::business-rules",
            heading_path="Business Rules",
            content="Only completed units count. Rework is excluded.",
            source_object_id="csu.metric.udc",
            title="Unit Delivery Cost (UDC)",
        ),
    ]
    pack.graph_neighbors.return_value = [
        make_graph_edge_hit(
            subject_id="csu.metric.udc",
            predicate="measures",
            object_id="csu.outcome.cost-efficiency",
            neighbor_title="Cost Efficiency",
            neighbor_type="outcome",
        ),
        make_graph_edge_hit(
            subject_id="csu.metric.udc",
            predicate="used_by",
            object_id="csu.role.delivery-manager",
            neighbor_title="Delivery Manager",
            neighbor_type="role",
        ),
    ]
    return pack


@pytest.fixture()
def pack_without_concept() -> MagicMock:
    """A LoadedPack stub that finds no matching concept."""
    pack = MagicMock()
    pack.lookup_concept.return_value = None
    pack.exact_matches.return_value = []
    return pack


@pytest.fixture()
def successful_reasoning_client() -> MagicMock:
    """A SemanticReasoningClient that returns synthesized prose."""
    client = MagicMock()
    client.synthesize_explanation.return_value = SynthesisResult(
        prose=(
            "Unit Delivery Cost (UDC) measures the cost per unit of work "
            "delivered. It is calculated as Total Cost divided by Units "
            "Delivered. UDC is a key measure of Cost Efficiency."
        ),
        cited_unit_ids=["csu.metric.udc::definition", "csu.metric.udc::formula"],
        confidence=0.92,
    )
    return client


@pytest.fixture()
def failing_reasoning_client() -> MagicMock:
    """A SemanticReasoningClient that raises an error."""
    client = MagicMock()
    client.synthesize_explanation.side_effect = RuntimeError("LLM service unavailable")
    return client


@pytest.fixture()
def declining_reasoning_client() -> MagicMock:
    """A SemanticReasoningClient that declines (NotImplementedError)."""
    client = MagicMock()
    client.synthesize_explanation.side_effect = NotImplementedError("not supported")
    return client


# ─── P-EXP-001: Valid concept → explanation with title + cited units ────────


class TestPromiseExplanationContent:
    """P-EXP-001: Valid concept → explanation with title and cited unit IDs."""

    def test_p_exp_001_returns_explanation_with_title(self, pack_with_concept: MagicMock) -> None:
        """P-EXP-001: Explanation contains the concept's title."""
        from akp_runtime.operations.explain_concept import ExplainConceptOperation

        operation = ExplainConceptOperation(pack=pack_with_concept, reasoning_client=None)
        result = operation.explain(query="csu.metric.udc", detail_level="standard")

        assert result is not None
        assert result.concept_title == "Unit Delivery Cost (UDC)"

    def test_p_exp_001_returns_at_least_one_cited_unit(self, pack_with_concept: MagicMock) -> None:
        """P-EXP-001: Explanation cites at least one semantic unit ID."""
        from akp_runtime.operations.explain_concept import ExplainConceptOperation

        operation = ExplainConceptOperation(pack=pack_with_concept, reasoning_client=None)
        result = operation.explain(query="csu.metric.udc", detail_level="standard")

        assert result is not None
        assert len(result.cited_unit_ids) >= 1


# ─── P-EXP-002: No reasoning client → structured Markdown fallback ─────────


class TestPromiseStructuredFallback:
    """P-EXP-002: Structured Markdown fallback when no LLM is available."""

    def test_p_exp_002_produces_markdown_without_reasoning_client(self, pack_with_concept: MagicMock) -> None:
        """P-EXP-002: Without a reasoning client, output is structured Markdown."""
        from akp_runtime.operations.explain_concept import ExplainConceptOperation

        operation = ExplainConceptOperation(pack=pack_with_concept, reasoning_client=None)
        result = operation.explain(query="csu.metric.udc", detail_level="standard")

        assert result is not None
        # Structured fallback organizes by heading
        assert "Definition" in result.explanation or "## " in result.explanation

    def test_p_exp_002_fallback_includes_semantic_unit_content(self, pack_with_concept: MagicMock) -> None:
        """P-EXP-002: Fallback includes actual content from semantic units."""
        from akp_runtime.operations.explain_concept import ExplainConceptOperation

        operation = ExplainConceptOperation(pack=pack_with_concept, reasoning_client=None)
        result = operation.explain(query="csu.metric.udc", detail_level="standard")

        assert result is not None
        assert "Unit Delivery Cost" in result.explanation


# ─── P-EXP-003: LLM synthesis → reports method as "llm" ────────────────────


class TestPromiseLlmSynthesis:
    """P-EXP-003: LLM-synthesized prose with correct synthesis method."""

    def test_p_exp_003_uses_llm_when_client_succeeds(
        self,
        pack_with_concept: MagicMock,
        successful_reasoning_client: MagicMock,
    ) -> None:
        """P-EXP-003: When reasoning client succeeds, method is 'llm'."""
        from akp_runtime.operations.explain_concept import ExplainConceptOperation

        operation = ExplainConceptOperation(
            pack=pack_with_concept,
            reasoning_client=successful_reasoning_client,
        )
        result = operation.explain(query="csu.metric.udc", detail_level="standard")

        assert result is not None
        assert result.synthesis_method == "llm"
        assert "Unit Delivery Cost" in result.explanation


# ─── P-EXP-004: Client error → fallback with diagnostic reason ─────────────


class TestPromiseGracefulDegradation:
    """P-EXP-004: Fallback with diagnostic reason on client error/decline."""

    def test_p_exp_004_falls_back_on_runtime_error(
        self,
        pack_with_concept: MagicMock,
        failing_reasoning_client: MagicMock,
    ) -> None:
        """P-EXP-004: RuntimeError triggers fallback, not exception propagation."""
        from akp_runtime.operations.explain_concept import ExplainConceptOperation

        operation = ExplainConceptOperation(
            pack=pack_with_concept,
            reasoning_client=failing_reasoning_client,
        )
        result = operation.explain(query="csu.metric.udc", detail_level="standard")

        assert result is not None
        assert result.synthesis_method == "structured_fallback"
        assert result.fallback_reason is not None
        assert "LLM service unavailable" in result.fallback_reason

    def test_p_exp_004_falls_back_on_not_implemented(
        self,
        pack_with_concept: MagicMock,
        declining_reasoning_client: MagicMock,
    ) -> None:
        """P-EXP-004: NotImplementedError triggers fallback with reason."""
        from akp_runtime.operations.explain_concept import ExplainConceptOperation

        operation = ExplainConceptOperation(
            pack=pack_with_concept,
            reasoning_client=declining_reasoning_client,
        )
        result = operation.explain(query="csu.metric.udc", detail_level="standard")

        assert result is not None
        assert result.synthesis_method == "structured_fallback"
        assert result.fallback_reason is not None
        assert "declined" in result.fallback_reason.lower() or "not supported" in result.fallback_reason.lower()

    def test_p_exp_004_no_client_includes_reason(self, pack_with_concept: MagicMock) -> None:
        """P-EXP-004: When no client configured, reason explains why."""
        from akp_runtime.operations.explain_concept import ExplainConceptOperation

        operation = ExplainConceptOperation(pack=pack_with_concept, reasoning_client=None)
        result = operation.explain(query="csu.metric.udc", detail_level="standard")

        assert result is not None
        assert result.fallback_reason is not None
        assert "no reasoning client" in result.fallback_reason.lower()


# ─── P-EXP-005: Detail levels filter semantic units ─────────────────────────


class TestPromiseDetailLevels:
    """P-EXP-005: Detail levels control which semantic units are included."""

    def test_p_exp_005_brief_includes_definition_only(self, pack_with_concept: MagicMock) -> None:
        """P-EXP-005: Brief includes definition/summary, excludes formulas."""
        from akp_runtime.operations.explain_concept import ExplainConceptOperation

        operation = ExplainConceptOperation(pack=pack_with_concept, reasoning_client=None)
        result = operation.explain(query="csu.metric.udc", detail_level="brief")

        assert result is not None
        assert result.detail_level == "brief"
        # Brief should NOT include business rules
        assert "Business Rules" not in result.explanation
        assert "Rework is excluded" not in result.explanation

    def test_p_exp_005_standard_includes_formula_and_thresholds(self, pack_with_concept: MagicMock) -> None:
        """P-EXP-005: Standard includes formulas and thresholds."""
        from akp_runtime.operations.explain_concept import ExplainConceptOperation

        operation = ExplainConceptOperation(pack=pack_with_concept, reasoning_client=None)
        result = operation.explain(query="csu.metric.udc", detail_level="standard")

        assert result is not None
        assert result.detail_level == "standard"
        assert "Formula" in result.explanation or "Total Cost" in result.explanation

    def test_p_exp_005_detailed_includes_all_units(self, pack_with_concept: MagicMock) -> None:
        """P-EXP-005: Detailed includes everything including business rules."""
        from akp_runtime.operations.explain_concept import ExplainConceptOperation

        operation = ExplainConceptOperation(pack=pack_with_concept, reasoning_client=None)
        result = operation.explain(query="csu.metric.udc", detail_level="detailed")

        assert result is not None
        assert result.detail_level == "detailed"
        assert "Business Rules" in result.explanation or "Rework" in result.explanation


# ─── P-EXP-006: Output always includes synthesis_method ─────────────────────


class TestPromiseSynthesisMethod:
    """P-EXP-006: synthesis_method is always present in output."""

    def test_p_exp_006_fallback_reports_structured_fallback(self, pack_with_concept: MagicMock) -> None:
        """P-EXP-006: Without LLM, synthesis_method is 'structured_fallback'."""
        from akp_runtime.operations.explain_concept import ExplainConceptOperation

        operation = ExplainConceptOperation(pack=pack_with_concept, reasoning_client=None)
        result = operation.explain(query="csu.metric.udc", detail_level="standard")

        assert result is not None
        assert result.synthesis_method == "structured_fallback"

    def test_p_exp_006_llm_reports_llm(
        self,
        pack_with_concept: MagicMock,
        successful_reasoning_client: MagicMock,
    ) -> None:
        """P-EXP-006: With LLM, synthesis_method is 'llm'."""
        from akp_runtime.operations.explain_concept import ExplainConceptOperation

        operation = ExplainConceptOperation(
            pack=pack_with_concept,
            reasoning_client=successful_reasoning_client,
        )
        result = operation.explain(query="csu.metric.udc", detail_level="standard")

        assert result is not None
        assert result.synthesis_method == "llm"


# ─── P-EXP-007: Unknown concept → None ─────────────────────────────────────


class TestPromiseUnknownConcept:
    """P-EXP-007: Unknown query returns None, never fabricates."""

    def test_p_exp_007_returns_none_for_unknown_concept(self, pack_without_concept: MagicMock) -> None:
        """P-EXP-007: No matching concept → None."""
        from akp_runtime.operations.explain_concept import ExplainConceptOperation

        operation = ExplainConceptOperation(pack=pack_without_concept, reasoning_client=None)
        result = operation.explain(query="nonexistent.concept", detail_level="standard")

        assert result is None


# ─── P-EXP-008: Neighbors referenced by title ──────────────────────────────


class TestPromiseNeighborTitles:
    """P-EXP-008: Related concepts are referenced by title, not raw IDs."""

    def test_p_exp_008_explanation_includes_neighbor_titles(self, pack_with_concept: MagicMock) -> None:
        """P-EXP-008: Neighbor titles appear in the explanation."""
        from akp_runtime.operations.explain_concept import ExplainConceptOperation

        operation = ExplainConceptOperation(pack=pack_with_concept, reasoning_client=None)
        result = operation.explain(query="csu.metric.udc", detail_level="standard")

        assert result is not None
        assert "Cost Efficiency" in result.explanation or "Cost Efficiency" in result.neighbor_titles

    def test_p_exp_008_raw_object_ids_not_in_explanation(self, pack_with_concept: MagicMock) -> None:
        """P-EXP-008: Raw object IDs should not appear in the prose."""
        from akp_runtime.operations.explain_concept import ExplainConceptOperation

        operation = ExplainConceptOperation(pack=pack_with_concept, reasoning_client=None)
        result = operation.explain(query="csu.metric.udc", detail_level="standard")

        assert result is not None
        # The raw object_id of the neighbor should not be in the explanation text
        assert "csu.outcome.cost-efficiency" not in result.explanation


# ─── INV-EXP-001: Never mutates pack state ─────────────────────────────────


class TestInvariantReadOnly:
    """INV-EXP-001: The operation never mutates pack state."""

    def test_inv_exp_001_no_mutating_calls_on_pack(self, pack_with_concept: MagicMock) -> None:
        """INV-EXP-001: Only read-only methods are called on the pack."""
        from akp_runtime.operations.explain_concept import ExplainConceptOperation

        operation = ExplainConceptOperation(pack=pack_with_concept, reasoning_client=None)
        operation.explain(query="csu.metric.udc", detail_level="standard")

        # Only these read-only methods should have been called
        allowed_methods = {"lookup_concept", "exact_matches", "concept_units", "graph_neighbors", "metadata"}
        called_methods = {call[0] for call in pack_with_concept.method_calls}
        assert called_methods.issubset(allowed_methods), (
            f"Unexpected pack methods called: {called_methods - allowed_methods}"
        )


# ─── INV-EXP-002: Depends on protocols, not concrete classes ───────────────


class TestInvariantProtocolDependency:
    """INV-EXP-002: Operation depends on protocols, not concrete classes."""

    def test_inv_exp_002_constructor_accepts_protocol_types(self) -> None:
        """INV-EXP-002: Constructor accepts protocol-typed arguments."""
        import inspect

        from akp_runtime.operations.explain_concept import ExplainConceptOperation

        sig = inspect.signature(ExplainConceptOperation.__init__)
        params = sig.parameters

        # 'pack' parameter should exist and not reference concrete class names
        assert "pack" in params
        # reasoning_client should be optional (can be None)
        assert "reasoning_client" in params


# ─── INV-EXP-003: Every claim traces to a cited unit ───────────────────────


class TestInvariantEvidenceGrounding:
    """INV-EXP-003: Cited unit IDs are real unit IDs from the pack."""

    def test_inv_exp_003_cited_ids_match_pack_units(self, pack_with_concept: MagicMock) -> None:
        """INV-EXP-003: All cited unit IDs exist in the pack's units."""
        from akp_runtime.operations.explain_concept import ExplainConceptOperation

        operation = ExplainConceptOperation(pack=pack_with_concept, reasoning_client=None)
        result = operation.explain(query="csu.metric.udc", detail_level="detailed")

        assert result is not None
        pack_unit_ids = {u.unit_id for u in pack_with_concept.concept_units.return_value}
        for cited_id in result.cited_unit_ids:
            assert cited_id in pack_unit_ids, f"Cited unit {cited_id} not in pack"


# ─── INV-EXP-004: Fallback produces valid Markdown ─────────────────────────


class TestInvariantValidMarkdown:
    """INV-EXP-004: Structured fallback produces valid Markdown."""

    def test_inv_exp_004_fallback_with_all_units(self, pack_with_concept: MagicMock) -> None:
        """INV-EXP-004: Fallback with full units produces valid Markdown."""
        from akp_runtime.operations.explain_concept import ExplainConceptOperation

        operation = ExplainConceptOperation(pack=pack_with_concept, reasoning_client=None)
        result = operation.explain(query="csu.metric.udc", detail_level="detailed")

        assert result is not None
        # Valid Markdown: has a heading with the concept title
        assert result.explanation.startswith("#") or "# " in result.explanation

    def test_inv_exp_004_fallback_with_empty_units(self) -> None:
        """INV-EXP-004: Fallback with zero units still produces valid Markdown."""
        from akp_runtime.operations.explain_concept import ExplainConceptOperation

        pack = MagicMock()
        pack.lookup_concept.return_value = make_search_hit(
            object_id="csu.metric.empty",
            title="Empty Metric",
        )
        pack.concept_units.return_value = []
        pack.graph_neighbors.return_value = []

        operation = ExplainConceptOperation(pack=pack, reasoning_client=None)
        result = operation.explain(query="csu.metric.empty", detail_level="standard")

        assert result is not None
        # Even with no units, produces valid Markdown with the title
        assert "Empty Metric" in result.explanation
        assert result.explanation.startswith("#") or "# " in result.explanation
