"""Tests for the Pack Rules engine and Outcome Validator."""

from __future__ import annotations

from pathlib import Path

import duckdb
import pytest

from kp_compiler.domain.rules import (
    AliasRules,
    AssertionKind,
    OutcomeAssertion,
    PackRules,
    QualityThresholds,
)
from kp_compiler.infrastructure.rules_loader import load_pack_rules
from kp_compiler.stages.outcome_validator import (
    OutcomeReport,
    run_assertion,
    validate_outcomes,
)


# ── AliasRules unit tests ──────────────────────────────────────────────────


class TestAliasRules:
    """Test the alias quality gate logic."""

    def test_stopword_blocked(self) -> None:
        rules = AliasRules()
        blocked, reason = rules.is_blocked("this")
        assert blocked is True
        assert "stopword" in reason

    def test_short_alias_blocked(self) -> None:
        rules = AliasRules(min_length=3)
        blocked, reason = rules.is_blocked("ab")
        assert blocked is True
        assert "too short" in reason

    def test_blocked_pattern_numbers(self) -> None:
        rules = AliasRules()
        blocked, reason = rules.is_blocked("123")
        assert blocked is True
        assert "blocked pattern" in reason

    def test_blocked_pattern_single_letter(self) -> None:
        rules = AliasRules()
        blocked, reason = rules.is_blocked("x")
        assert blocked is True
        # Will match either min_length or blocked pattern

    def test_valid_alias_passes(self) -> None:
        rules = AliasRules()
        blocked, _ = rules.is_blocked("C2C")
        assert blocked is False

    def test_valid_expansion_passes(self) -> None:
        rules = AliasRules()
        blocked, _ = rules.is_blocked("Commit to Complete")
        assert blocked is False

    def test_custom_stopwords(self) -> None:
        rules = AliasRules(stopwords=frozenset({"azure", "cloud"}))
        assert rules.is_blocked("azure")[0] is True
        assert rules.is_blocked("C2C")[0] is False

    def test_case_insensitive(self) -> None:
        rules = AliasRules()
        blocked, _ = rules.is_blocked("THIS")
        assert blocked is True

    def test_whitespace_trimmed(self) -> None:
        rules = AliasRules()
        blocked, _ = rules.is_blocked("  this  ")
        assert blocked is True


# ── PackRules parsing tests ────────────────────────────────────────────────


class TestPackRules:
    """Test Pydantic parsing and defaults."""

    def test_default_factory(self) -> None:
        rules = PackRules.default()
        assert rules.version == "1.0"
        assert len(rules.alias_rules.stopwords) > 10
        assert len(rules.outcome_assertions) == 3
        assert rules.quality_thresholds.fail_on_error is True

    def test_from_minimal_dict(self) -> None:
        rules = PackRules.model_validate({"version": "2.0"})
        assert rules.version == "2.0"
        # Defaults should fill in
        assert rules.alias_rules.min_length == 2

    def test_from_full_dict(self) -> None:
        data = {
            "version": "1.0",
            "alias_rules": {
                "stopwords": ["foo", "bar"],
                "min_length": 3,
                "max_tag_fanout": 20,
                "max_explicit_fanout": 10,
                "blocked_patterns": [r"^\d+$"],
            },
            "outcome_assertions": [
                {
                    "name": "test-assertion",
                    "rule": "max_tag_coverage",
                    "params": {"threshold": 0.5},
                },
            ],
            "quality_thresholds": {
                "min_assertion_pass_rate": 0.9,
                "fail_on_error": False,
            },
        }
        rules = PackRules.model_validate(data)
        assert rules.alias_rules.min_length == 3
        assert len(rules.outcome_assertions) == 1
        assert rules.outcome_assertions[0].rule == AssertionKind.MAX_TAG_COVERAGE
        assert rules.quality_thresholds.fail_on_error is False

    def test_invalid_pattern_raises(self) -> None:
        with pytest.raises(Exception):
            AliasRules(blocked_patterns=["[invalid"])

    def test_frozen_model(self) -> None:
        rules = PackRules.default()
        with pytest.raises(Exception):
            rules.version = "2.0"  # type: ignore[misc]


# ── Rules loader tests ─────────────────────────────────────────────────────


class TestRulesLoader:
    """Test YAML loading and validation."""

    def test_missing_file_returns_defaults(self, tmp_path: Path) -> None:
        rules = load_pack_rules(tmp_path / "nonexistent.yaml")
        assert rules.version == "1.0"
        assert len(rules.alias_rules.stopwords) > 10

    def test_empty_file_returns_defaults(self, tmp_path: Path) -> None:
        p = tmp_path / "empty.yaml"
        p.write_text("", encoding="utf-8")
        rules = load_pack_rules(p)
        assert rules.version == "1.0"

    def test_loads_real_rules_file(self) -> None:
        rules_path = Path(__file__).parent.parent / "okf" / "pack-rules.yaml"
        if not rules_path.exists():
            # Try from compiler root
            rules_path = Path(__file__).parent.parent.parent.parent / "okf" / "pack-rules.yaml"
        if rules_path.exists():
            rules = load_pack_rules(rules_path)
            assert rules.version == "1.0"
            assert "this" in rules.alias_rules.stopwords


# ── Outcome validator tests ────────────────────────────────────────────────


def _make_test_pack(tmp_path: Path) -> Path:
    """Create a minimal DuckDB pack for testing."""
    pack_path = tmp_path / "test.duckdb"
    con = duckdb.connect(str(pack_path))

    con.execute("""
        CREATE TABLE objects (
            id VARCHAR PRIMARY KEY,
            type VARCHAR NOT NULL,
            title VARCHAR,
            description VARCHAR,
            domain VARCHAR,
            status VARCHAR,
            aliases JSON,
            tags JSON,
            source_path VARCHAR,
            properties JSON
        )
    """)
    con.execute("""
        INSERT INTO objects (id, type, title, description, domain)
        VALUES
            ('csu.metric.c2c', 'KPI', 'Job 1 — Commit to Complete (C2C)', 'C2C metric', 'csu'),
            ('csu.metric.nnr', 'KPI', 'NNR — Net New Revenue', 'NNR metric', 'csu'),
            ('csu.process.delivery', 'Process', 'CSU Delivery Process', 'Main delivery', 'csu')
    """)

    con.execute("""
        CREATE TABLE aliases (
            alias VARCHAR NOT NULL,
            canonical_id VARCHAR NOT NULL,
            alias_type VARCHAR DEFAULT 'exact'
        )
    """)
    con.execute("""
        INSERT INTO aliases (alias, canonical_id, alias_type) VALUES
            ('Job 1 — Commit to Complete (C2C)', 'csu.metric.c2c', 'title'),
            ('c2c', 'csu.metric.c2c', 'explicit'),
            ('NNR — Net New Revenue', 'csu.metric.nnr', 'title'),
            ('nnr', 'csu.metric.nnr', 'explicit'),
            ('CSU Delivery Process', 'csu.process.delivery', 'title'),
            ('csu', 'csu.metric.c2c', 'tag'),
            ('csu', 'csu.metric.nnr', 'tag'),
            ('csu', 'csu.process.delivery', 'tag')
    """)

    con.close()
    return pack_path


class TestOutcomeValidator:
    """Test outcome assertions against a test pack."""

    def test_alias_owner_in_top_k_passes(self, tmp_path: Path) -> None:
        pack = _make_test_pack(tmp_path)
        assertion = OutcomeAssertion(
            name="test",
            rule=AssertionKind.ALIAS_OWNER_IN_TOP_K,
            params={"k": 3, "sample": 100},
        )
        con = duckdb.connect(str(pack), read_only=True)
        result = run_assertion(assertion, con)
        con.close()
        assert result.passed is True

    def test_max_tag_coverage_fails_with_low_threshold(self, tmp_path: Path) -> None:
        pack = _make_test_pack(tmp_path)
        assertion = OutcomeAssertion(
            name="test",
            rule=AssertionKind.MAX_TAG_COVERAGE,
            params={"threshold": 0.5},
        )
        con = duckdb.connect(str(pack), read_only=True)
        result = run_assertion(assertion, con)
        con.close()
        # "csu" tag covers 3/3 = 100% > 50%
        assert result.passed is False
        assert any("csu" in f for f in result.failures)

    def test_max_tag_coverage_passes_with_high_threshold(self, tmp_path: Path) -> None:
        pack = _make_test_pack(tmp_path)
        assertion = OutcomeAssertion(
            name="test",
            rule=AssertionKind.MAX_TAG_COVERAGE,
            params={"threshold": 1.0},
        )
        con = duckdb.connect(str(pack), read_only=True)
        result = run_assertion(assertion, con)
        con.close()
        assert result.passed is True

    def test_title_self_retrieval_passes(self, tmp_path: Path) -> None:
        pack = _make_test_pack(tmp_path)
        assertion = OutcomeAssertion(
            name="test",
            rule=AssertionKind.TITLE_SELF_RETRIEVAL,
            params={"k": 5, "sample": 100},
        )
        con = duckdb.connect(str(pack), read_only=True)
        result = run_assertion(assertion, con)
        con.close()
        assert result.passed is True

    def test_no_orphan_aliases_passes(self, tmp_path: Path) -> None:
        pack = _make_test_pack(tmp_path)
        assertion = OutcomeAssertion(
            name="test",
            rule=AssertionKind.NO_ORPHAN_ALIASES,
            params={},
        )
        con = duckdb.connect(str(pack), read_only=True)
        result = run_assertion(assertion, con)
        con.close()
        assert result.passed is True

    def test_validate_outcomes_full(self, tmp_path: Path) -> None:
        pack = _make_test_pack(tmp_path)
        rules = PackRules.model_validate({
            "outcome_assertions": [
                {"name": "alias-check", "rule": "alias_owner_in_top_k", "params": {"k": 3}},
                {"name": "tag-check", "rule": "max_tag_coverage", "params": {"threshold": 1.0}},
            ],
            "quality_thresholds": {"min_assertion_pass_rate": 1.0},
        })
        report = validate_outcomes(pack, rules)
        assert report.passed is True
        assert report.pass_rate == 1.0


# ── Enrichment gate integration test ───────────────────────────────────────


class TestEnrichmentGate:
    """Test that the alias gate filters aliases during enrichment."""

    def test_stopword_filtered_in_enrichment(self) -> None:
        from kp_compiler.domain.models import KnowledgeObject, ObjectType, Section
        from kp_compiler.stages.enrich import enrich_corpus

        obj = KnowledgeObject(
            id="test.obj.1",
            title="This Test Object",
            type=ObjectType.PROCESS,
            domain="test",
            description="A test object",
            raw_body="This Object (THIS) is important",
            sections=[Section(heading="Body", content="Content here", level=2)],
        )
        rules = PackRules.model_validate({
            "alias_rules": {"stopwords": ["this"]},
        })
        result = enrich_corpus([obj], rules)
        aliases_lower = [a.lower() for a in result.objects[0].aliases]
        assert "this" not in aliases_lower

    def test_enrichment_without_rules_still_works(self) -> None:
        from kp_compiler.domain.models import KnowledgeObject, ObjectType, Section
        from kp_compiler.stages.enrich import enrich_corpus

        obj = KnowledgeObject(
            id="test.obj.2",
            title="CSU Process",
            type=ObjectType.PROCESS,
            domain="test",
            description="Test",
            raw_body="Customer Success Unit (CSU) does things",
            sections=[Section(heading="Body", content="Content", level=2)],
        )
        result = enrich_corpus([obj])  # No rules = backward compatible
        assert result.aliases_added >= 0
