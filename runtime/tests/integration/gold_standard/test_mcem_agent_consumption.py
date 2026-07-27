"""Gold standard tests for MCEM pack — agent consumption output.

These tests validate that the explain operation produces correct, structured
data suitable for machine (agent) consumers against the MCEM pack.
"""

from __future__ import annotations

import pytest

from akp_runtime.domain.explain_models import ExplainResult
from akp_runtime.infrastructure.duckdb_loader import DuckDBLoadedPack
from akp_runtime.operations.explain_concept import ExplainConceptOperation


class TestMcemAgentConsumption:
    """MCEM pack: 5 gold standard agent-structured output tests."""

    # ─── Gold 1: ICP — concept role takes priority in resolution ──────────────

    def test_icp_resolution_prioritizes_concept_role(
        self, mcem_pack: DuckDBLoadedPack
    ) -> None:
        """ICP resolves to Framework (concept role) over other types."""
        hits = mcem_pack.exact_matches("ICP", limit=5)

        assert len(hits) >= 1
        # First hit must be the concept-role object (Framework)
        assert hits[0].object_id == "mcem.planning.integrated-customer-planning-icp"
        assert hits[0].object_type == "Framework"

    # ─── Gold 2: Account Planning — semantic units are well-structured ────────

    def test_account_planning_units_have_valid_structure(
        self, mcem_pack: DuckDBLoadedPack
    ) -> None:
        """Account Planning semantic units are well-structured for agents."""
        hits = mcem_pack.exact_matches("Account Planning", limit=1)
        assert len(hits) >= 1

        units = mcem_pack.concept_units(hits[0].object_id, limit=20)
        assert len(units) >= 1

        for unit in units:
            assert unit.unit_id, "unit_id required"
            assert unit.source_object_id == hits[0].object_id
            assert unit.heading_path, "heading_path required for agent parsing"
            assert unit.content and len(unit.content) > 5

    # ─── Gold 3: UCR — graph neighbors provide measurement relationships ─────

    def test_ucr_neighbors_expose_stage_relationships(
        self, mcem_pack: DuckDBLoadedPack
    ) -> None:
        """UCR graph neighbors connect to MCEM stages for agent navigation."""
        hits = mcem_pack.exact_matches("UCR", limit=1)
        assert len(hits) >= 1

        neighbors = mcem_pack.graph_neighbors(hits[0].object_id, hops=1, predicates=(), limit=20)
        assert len(neighbors) >= 1

        # UCR should relate to MCEM stages or delivery concepts
        neighbor_titles = [n.neighbor_title for n in neighbors]
        assert any("Stage" in t or "Realize" in t or "Enhanced" in t for t in neighbor_titles)

        for neighbor in neighbors:
            assert neighbor.predicate, "predicate required for agent reasoning"
            assert neighbor.neighbor_title, "title required for agent display"

    # ─── Gold 4: PCI — ExplainResult contract is complete for agents ──────────

    def test_pci_explain_result_is_agent_parseable(
        self, mcem_explain: ExplainConceptOperation
    ) -> None:
        """PCI ExplainResult satisfies the full agent consumption contract."""
        result = mcem_explain.explain("PCI", detail_level="standard")

        assert result is not None
        # Structural completeness for agent consumers
        assert isinstance(result.concept_title, str) and result.concept_title
        assert isinstance(result.explanation, str) and result.explanation
        assert isinstance(result.cited_unit_ids, list)
        assert all(isinstance(uid, str) and ":" in uid for uid in result.cited_unit_ids)
        assert result.synthesis_method == "structured_fallback"
        assert isinstance(result.fallback_reason, str)
        assert result.detail_level == "standard"
        assert isinstance(result.neighbor_titles, list)
        assert all(isinstance(t, str) for t in result.neighbor_titles)

    # ─── Gold 5: Committed Pipeline — cited units traceable to pack objects ───

    def test_committed_pipeline_citations_are_traceable(
        self, mcem_pack: DuckDBLoadedPack, mcem_explain: ExplainConceptOperation
    ) -> None:
        """Every cited unit in Committed Pipeline traces to a real pack unit."""
        result = mcem_explain.explain("Committed Pipeline", detail_level="detailed")

        assert result is not None
        assert len(result.cited_unit_ids) >= 2

        # Verify traceability
        hits = mcem_pack.exact_matches("Committed Pipeline", limit=1)
        assert len(hits) >= 1
        all_units = mcem_pack.concept_units(hits[0].object_id, limit=50)
        valid_ids = {u.unit_id for u in all_units}

        for cited_id in result.cited_unit_ids:
            assert cited_id in valid_ids, (
                f"Cited unit {cited_id} not traceable to Committed Pipeline object"
            )
