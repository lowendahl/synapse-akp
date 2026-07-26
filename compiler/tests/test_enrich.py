"""Tests for enrichment stage (ADR-012 — NLP enrichment)."""

from kp_compiler.domain.models import KnowledgeObject, Relationship
from kp_compiler.stages.enrich import (
    detect_fuzzy_duplicates,
    enrich_corpus,
    expand_aliases,
    extract_acronyms_from_text,
)


def _make_obj(
    obj_id: str = "csu.metric.test",
    title: str = "Test Metric",
    aliases: list[str] | None = None,
    raw_body: str = "",
) -> KnowledgeObject:
    return KnowledgeObject(
        id=obj_id,
        title=title,
        type="Metric",
        domain="csu",
        source_path="csu/metrics/test.md",
        raw_body=raw_body,
        sections=[],
        relationships=[],
        aliases=list(aliases or []),
        properties={},
    )


class TestExtractAcronyms:
    """Verify regex-based acronym extraction from text."""

    def test_extracts_standard_pattern(self) -> None:
        text = "Customer Success Plan (CSP) is required for all accounts."
        found = extract_acronyms_from_text(text)
        assert any(a == "CSP" for a, _ in found)

    def test_extracts_multi_word_expansion(self) -> None:
        text = "Azure Consumed Revenue (ACR) drives growth."
        found = extract_acronyms_from_text(text)
        assert any(exp == "Azure Consumed Revenue" for _, exp in found)

    def test_ignores_short_names(self) -> None:
        text = "It (IT) is not a valid extraction."
        found = extract_acronyms_from_text(text)
        # "It" is only 2 chars — should be filtered
        assert len(found) == 0

    def test_no_matches_in_plain_text(self) -> None:
        found = extract_acronyms_from_text("No acronyms defined here.")
        assert found == []


class TestExpandAliases:
    """Verify alias expansion from known acronym dictionary."""

    def test_expands_known_acronym_in_title(self) -> None:
        obj = _make_obj(title="UDC Coverage Metric")
        new_aliases, count, _ = expand_aliases(obj)
        expansions = [a.lower() for a in new_aliases]
        assert "unified delivery coverage" in expansions
        assert count > 0

    def test_expands_body_acronyms(self) -> None:
        obj = _make_obj(raw_body="Quarterly Business Review (QBR) is monthly.")
        new_aliases, count, _ = expand_aliases(obj)
        alias_set = {a.lower() for a in new_aliases}
        assert "qbr" in alias_set or "quarterly business review" in alias_set

    def test_no_duplicate_aliases(self) -> None:
        obj = _make_obj(
            title="CSP Hierarchy",
            aliases=["Customer Success Plan"],
        )
        new_aliases, _, _ = expand_aliases(obj)
        # "Customer Success Plan" already exists — should not be re-added
        assert new_aliases.count("Customer Success Plan") == 0


class TestFuzzyDuplicates:
    """Verify fuzzy duplicate detection via rapidfuzz."""

    def test_detects_near_duplicate_titles(self) -> None:
        objs = [
            _make_obj(obj_id="a", title="Azure Consumption Revenue"),
            _make_obj(obj_id="b", title="Azure Consumed Revenue"),
        ]
        diags = detect_fuzzy_duplicates(objs, threshold=80)
        assert len(diags) >= 1
        assert "Fuzzy duplicate" in diags[0].message

    def test_no_false_positives_for_different_titles(self) -> None:
        objs = [
            _make_obj(obj_id="a", title="Cloud Migration Factory"),
            _make_obj(obj_id="b", title="Customer Success Plan"),
        ]
        diags = detect_fuzzy_duplicates(objs, threshold=85)
        assert len(diags) == 0

    def test_exact_duplicates_excluded(self) -> None:
        objs = [
            _make_obj(obj_id="a", title="UDC Metric"),
            _make_obj(obj_id="b", title="UDC Metric"),
        ]
        diags = detect_fuzzy_duplicates(objs, threshold=85)
        # exact match (score=100) but same title → excluded by != check
        assert len(diags) == 0


class TestEnrichCorpus:
    """Integration test: full enrichment pass."""

    def test_enriches_objects_with_aliases(self) -> None:
        objs = [
            _make_obj(obj_id="csu.metric.c2c", title="Job 1 C2C"),
            _make_obj(obj_id="csu.metric.udc", title="UDC Coverage"),
        ]
        result = enrich_corpus(objs)
        assert result.aliases_added > 0
        assert result.acronyms_resolved > 0
        assert len(result.objects) == 2

    def test_skips_objects_without_id(self) -> None:
        objs = [_make_obj(obj_id="", title="No ID Object")]
        result = enrich_corpus(objs)
        assert result.aliases_added == 0
        assert len(result.objects) == 1
