"""Gold standard tests for CSU pack — agent consumption output.

These tests validate that the explain operation produces correct, structured
data suitable for machine (agent) consumers. The output must have proper
provenance, typed fields, and machine-parseable structure that an LLM or
downstream tool can reliably consume.

Each test validates the contract surface that agents depend on.
"""

from __future__ import annotations

import pytest

from akp_runtime.domain.explain_models import ExplainResult
from akp_runtime.infrastructure.duckdb_loader import DuckDBLoadedPack
from akp_runtime.operations.explain_concept import ExplainConceptOperation


class TestCsuAgentConsumption:
    """CSU pack: 5 gold standard agent-structured output tests."""

    # ─── Gold 1: Job1 — resolution priority is correct (concept > measurement > evidence) ─

    def test_job1_resolution_priority_concept_over_kpi(
        self, csu_pack: DuckDBLoadedPack
    ) -> None:
        """Job1 resolves to Process (concept role), NOT KPI (measurement role)."""
        hits = csu_pack.exact_matches("Job1", limit=5)

        assert len(hits) >= 2
        # First result must be the concept-role object
        assert hits[0].object_type == "Process"
        assert hits[0].object_id == "csu.process.commit-to-complete"
        # KPI should be present but ranked lower
        kpi_hits = [h for h in hits if h.object_type == "KPI"]
        assert len(kpi_hits) >= 1

    # ─── Gold 2: UDC — semantic units have required fields ────────────────────

    def test_udc_semantic_units_have_complete_fields(
        self, csu_pack: DuckDBLoadedPack
    ) -> None:
        """UDC semantic units have all required fields for agent consumption."""
        hits = csu_pack.exact_matches("UDC", limit=1)
        assert len(hits) >= 1

        units = csu_pack.concept_units(hits[0].object_id, limit=20)
        assert len(units) >= 2

        for unit in units:
            # Every semantic unit must have these fields populated
            assert unit.unit_id, "unit_id must not be empty"
            assert unit.source_object_id, "source_object_id must not be empty"
            assert unit.heading_path, "heading_path must not be empty"
            assert unit.content, "content must not be empty"
            assert len(unit.content) > 10, "content must have substance"

    # ─── Gold 3: CSP — graph neighbors provide typed relationships ────────────

    def test_csp_graph_neighbors_have_typed_edges(
        self, csu_pack: DuckDBLoadedPack
    ) -> None:
        """CSP graph neighbors expose predicate, type, and title for agents."""
        hits = csu_pack.exact_matches("CSP", limit=1)
        assert len(hits) >= 1
        assert "Customer Success Plan" in hits[0].title

        neighbors = csu_pack.graph_neighbors(hits[0].object_id, hops=1, predicates=(), limit=20)
        # CSP should have at least one relationship
        assert len(neighbors) >= 1

        for neighbor in neighbors:
            assert neighbor.predicate, "predicate must not be empty"
            assert neighbor.neighbor_title, "neighbor_title must not be empty"
            # Agent needs the subject/object relationship direction
            assert neighbor.subject_id or neighbor.object_id

    # ─── Gold 4: Customer Health — ExplainResult has all contract fields ──────

    def test_customer_health_explain_result_contract_complete(
        self, csu_explain: ExplainConceptOperation
    ) -> None:
        """ExplainResult for Customer Health has every contract field populated."""
        result = csu_explain.explain("Customer Health", detail_level="standard")

        assert result is not None
        # All fields from the ExplainResult contract
        assert isinstance(result.concept_title, str) and len(result.concept_title) > 0
        assert isinstance(result.explanation, str) and len(result.explanation) > 0
        assert isinstance(result.cited_unit_ids, list) and len(result.cited_unit_ids) >= 1
        assert result.synthesis_method in ("llm", "structured_fallback")
        assert isinstance(result.fallback_reason, str)  # populated because no LLM
        assert result.detail_level == "standard"
        assert isinstance(result.neighbor_titles, list)

    # ─── Gold 5: SP — cited unit IDs are valid pack references ────────────────

    def test_sp_cited_unit_ids_are_valid_pack_references(
        self, csu_pack: DuckDBLoadedPack, csu_explain: ExplainConceptOperation
    ) -> None:
        """Every cited_unit_id in SP explanation is a real pack unit ID."""
        result = csu_explain.explain("SP", detail_level="detailed")

        assert result is not None
        assert len(result.cited_unit_ids) >= 1

        # Verify each cited unit actually exists in the pack
        hits = csu_pack.exact_matches("SP", limit=1)
        assert len(hits) >= 1
        all_units = csu_pack.concept_units(hits[0].object_id, limit=50)
        valid_ids = {u.unit_id for u in all_units}

        for cited_id in result.cited_unit_ids:
            assert cited_id in valid_ids, f"Cited unit {cited_id} not found in pack"
