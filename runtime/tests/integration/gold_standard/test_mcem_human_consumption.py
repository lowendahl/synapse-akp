"""Gold standard tests for MCEM pack — human consumption output.

These tests validate that the explain operation produces correct, readable
output for human consumers against the MCEM (Microsoft Customer Engagement
Methodology) knowledge pack.
"""

from __future__ import annotations

import pytest

from akp_runtime.domain.explain_models import ExplainResult
from akp_runtime.operations.explain_concept import ExplainConceptOperation


class TestMcemHumanConsumption:
    """MCEM pack: 5 gold standard human-readable explanation tests."""

    # ─── Gold 1: ICP → Framework concept with planning context ────────────────

    def test_icp_resolves_to_framework_concept(
        self, mcem_explain: ExplainConceptOperation
    ) -> None:
        """ICP resolves to Integrated Customer Planning framework."""
        result = mcem_explain.explain("ICP", detail_level="standard")

        assert result is not None
        assert "Integrated Customer Planning" in result.concept_title
        assert result.synthesis_method == "structured_fallback"
        assert result.explanation.startswith("# Integrated Customer Planning")
        # Has real domain content
        assert len(result.explanation) > 100
        # ICP is the master framework — should connect to planning processes
        assert len(result.neighbor_titles) >= 2

    # ─── Gold 2: Account Planning → Process with related context ──────────────

    def test_account_planning_explains_process(
        self, mcem_explain: ExplainConceptOperation
    ) -> None:
        """Account Planning explains the planning process with relationships."""
        result = mcem_explain.explain("Account Planning", detail_level="standard")

        assert result is not None
        assert "Account Planning" in result.concept_title
        assert result.synthesis_method == "structured_fallback"
        assert len(result.cited_unit_ids) >= 1
        # Should have related processes/frameworks as neighbors
        assert len(result.neighbor_titles) >= 1

    # ─── Gold 3: UCR → Metric with measurement content ───────────────────────

    def test_ucr_explains_revenue_metric(
        self, mcem_explain: ExplainConceptOperation
    ) -> None:
        """UCR explains Unified Consumed Revenue metric clearly."""
        result = mcem_explain.explain("UCR", detail_level="standard")

        assert result is not None
        assert "Unified Consumed Revenue" in result.concept_title or "UCR" in result.concept_title
        assert result.synthesis_method == "structured_fallback"
        assert len(result.cited_unit_ids) >= 2
        # Has substance about revenue/consumption
        assert len(result.explanation) > 100

    # ─── Gold 4: PCI → Pipeline Coverage Index measurement ───────────────────

    def test_pci_explains_pipeline_coverage(
        self, mcem_explain: ExplainConceptOperation
    ) -> None:
        """PCI explains Pipeline Coverage Index with measurement context."""
        result = mcem_explain.explain("PCI", detail_level="standard")

        assert result is not None
        assert "Pipeline Coverage Index" in result.concept_title
        assert result.synthesis_method == "structured_fallback"
        assert len(result.cited_unit_ids) >= 2
        # Should connect to planning/stage concepts
        assert len(result.neighbor_titles) >= 1

    # ─── Gold 5: Committed Pipeline → detailed includes all units ────────────

    def test_committed_pipeline_detailed_is_comprehensive(
        self, mcem_explain: ExplainConceptOperation
    ) -> None:
        """Committed Pipeline at detailed level includes all available content."""
        result = mcem_explain.explain("Committed Pipeline", detail_level="detailed")

        assert result is not None
        assert "Committed Pipeline" in result.concept_title
        assert result.synthesis_method == "structured_fallback"
        # Detailed level gives everything
        assert len(result.cited_unit_ids) >= 2
        # Full explanation should be substantial
        assert len(result.explanation) > 150
        # Should connect to MCEM stages
        assert any("Stage" in t for t in result.neighbor_titles)
