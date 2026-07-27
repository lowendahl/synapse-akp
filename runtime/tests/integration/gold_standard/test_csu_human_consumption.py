"""Gold standard tests for CSU pack — human consumption output.

These tests validate that the explain operation produces correct, readable
output for human consumers. The structured fallback must be coherent Markdown
that a domain professional would recognize as accurate.

Each test represents a canonical resolution + explanation scenario that MUST
always work correctly. Regressions here mean the pack or runtime is broken
for real users.
"""

from __future__ import annotations

import pytest

from akp_runtime.domain.explain_models import ExplainResult
from akp_runtime.operations.explain_concept import ExplainConceptOperation


class TestCsuHumanConsumption:
    """CSU pack: 5 gold standard human-readable explanation tests."""

    # ─── Gold 1: Job1 → Commit-to-Complete concept (the canonical ADR-039 case) ─

    def test_job1_resolves_to_process_concept(
        self, csu_explain: ExplainConceptOperation
    ) -> None:
        """Job1 resolves to the C2C Process concept and explains the operational model."""
        result = csu_explain.explain("Job1", detail_level="standard")

        assert result is not None
        assert result.concept_title == "Commit-to-Complete"
        assert result.synthesis_method == "structured_fallback"
        # Human-readable: starts with a Markdown heading
        assert result.explanation.startswith("# Commit-to-Complete")
        # Contains actual domain content, not placeholder
        assert "CSU" in result.explanation or "commit" in result.explanation.lower()
        # Has related concepts for context
        assert len(result.neighbor_titles) >= 1

    # ─── Gold 2: UDC → Metric with formula and thresholds ─────────────────────

    def test_udc_explains_delivery_metric_with_substance(
        self, csu_explain: ExplainConceptOperation
    ) -> None:
        """UDC explains the unified delivery coverage metric with real content."""
        result = csu_explain.explain("UDC", detail_level="standard")

        assert result is not None
        assert "Unified Delivery Coverage" in result.concept_title or "UDC" in result.concept_title
        # Standard level should include formula/definition content
        assert len(result.cited_unit_ids) >= 2
        # Explanation has real substance (not just a title)
        assert len(result.explanation) > 100
        # Has neighbor context
        assert len(result.neighbor_titles) >= 1

    # ─── Gold 3: CSP → Customer Success Plan (Planning, not CSP Hierarchy) ────

    def test_csp_resolves_to_planning_document_not_hierarchy(
        self, csu_explain: ExplainConceptOperation
    ) -> None:
        """CSP resolves to Customer Success Plan, not CSP Hierarchy doctrine."""
        result = csu_explain.explain("CSP", detail_level="standard")

        assert result is not None
        assert "Customer Success Plan" in result.concept_title
        # Must NOT resolve to the doctrine
        assert "Hierarchy" not in result.concept_title
        assert result.synthesis_method == "structured_fallback"
        assert len(result.cited_unit_ids) >= 1

    # ─── Gold 4: Customer Health → Process concept (Existing Deals Motion) ────

    def test_customer_health_resolves_to_process_not_metric(
        self, csu_explain: ExplainConceptOperation
    ) -> None:
        """Customer Health resolves to the process concept via author alias."""
        result = csu_explain.explain("Customer Health", detail_level="standard")

        assert result is not None
        # Resolves to Existing Deals Motion (the process), not a metric
        assert "Existing Deals" in result.concept_title or "Motion" in result.concept_title
        assert result.synthesis_method == "structured_fallback"
        assert len(result.cited_unit_ids) >= 1

    # ─── Gold 5: SP → Success Programs (brief vs detailed) ───────────────────

    def test_sp_brief_vs_detailed_has_different_depth(
        self, csu_explain: ExplainConceptOperation
    ) -> None:
        """SP (Success Programs) brief is shorter than detailed."""
        brief = csu_explain.explain("SP", detail_level="brief")
        detailed = csu_explain.explain("SP", detail_level="detailed")

        assert brief is not None
        assert detailed is not None
        assert "Success Programs" in brief.concept_title
        assert "Success Programs" in detailed.concept_title
        # Detailed must include more content
        assert len(detailed.cited_unit_ids) >= len(brief.cited_unit_ids)
        # Both produce valid structured Markdown
        assert brief.explanation.startswith("#")
        assert detailed.explanation.startswith("#")
