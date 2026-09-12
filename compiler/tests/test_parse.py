"""Unit tests for the parser stage."""

import pytest

from kp_compiler.contracts.errors import OntologyViolation
from kp_compiler.domain.models import ObjectType
from kp_compiler.domain.ontology import Ontology
from kp_compiler.stages.knowledge_object_factory import KnowledgeObjectFactory
from kp_compiler.stages.parse import (
    extract_sections,
    parse_frontmatter,
    parse_source,
)


def _factory_with_ontology() -> KnowledgeObjectFactory:
    ontology = Ontology.from_dict(
        {
            "version": "test",
            "object_types": {
                "Stage": {"resolution_role": "concept", "aliases": ["MCEM Stage"]},
                "Pipeline": {"resolution_role": "concept", "aliases": ["Pipeline Object"]},
                "Organization": {"resolution_role": "concept", "aliases": ["Operating Model"]},
                "Metric": {"resolution_role": "measurement"},
            },
        }
    )
    return KnowledgeObjectFactory(ontology=ontology)


class TestParseFrontmatter:
    def test_extracts_yaml_and_body(self) -> None:
        content = "---\ntitle: Test\ntype: Metric\n---\n# Body\nContent here."
        fm, body = parse_frontmatter(content)
        assert fm["title"] == "Test"
        assert fm["type"] == "Metric"
        assert "# Body" in body

    def test_no_frontmatter_returns_empty_dict(self) -> None:
        content = "# Just markdown\nNo frontmatter here."
        fm, body = parse_frontmatter(content)
        assert fm == {}
        assert "# Just markdown" in body

    def test_empty_frontmatter(self) -> None:
        content = "---\n---\n# Body"
        fm, body = parse_frontmatter(content)
        assert fm is None or fm == {}


class TestExtractSections:
    def test_extracts_heading_sections(self) -> None:
        body = "# Heading One\nParagraph 1.\n## Heading Two\nParagraph 2."
        sections = extract_sections(body)
        assert len(sections) == 2
        assert sections[0].heading == "Heading One"
        assert sections[0].level == 1
        assert "Paragraph 1." in sections[0].content
        assert sections[1].heading == "Heading Two"
        assert sections[1].level == 2

    def test_no_headings_returns_single_section(self) -> None:
        body = "Just a paragraph.\nAnother line."
        sections = extract_sections(body)
        assert len(sections) == 1
        assert sections[0].heading == ""


class TestDetermineObjectType:
    def test_types_resolve_to_canonical_via_ontology(self) -> None:
        factory = _factory_with_ontology()
        assert factory.resolve_type("Metric") == "Metric"
        assert factory.resolve_type("MCEM Stage") == "Stage"
        assert factory.resolve_type("Pipeline Object") == "Pipeline"
        assert factory.resolve_type("Operating Model") == "Organization"

    def test_unknown_type_raises_ontology_violation(self) -> None:
        with pytest.raises(OntologyViolation):
            _factory_with_ontology().resolve_type("SomethingNew")


class TestParseSource:
    def test_parses_metric_object(self) -> None:
        content = (
            "---\n"
            "title: Job 1 C2C\n"
            "id: csu.metric.job1-c2c\n"
            "type: Metric\n"
            "aliases:\n  - C2C\n  - Commit to Complete\n"
            "tags:\n  - kpi\n"
            "description: Committed milestone completion rate.\n"
            "---\n"
            "# Formula\nC2C = closed / committed\n"
        )
        obj = parse_source(content, "csu/metrics/job1-c2c.md")
        assert obj.id == "csu.metric.job1-c2c"
        assert obj.type == ObjectType.METRIC
        assert obj.title == "Job 1 C2C"
        assert "C2C" in obj.aliases
        assert obj.domain == "csu"
        assert len(obj.sections) == 1
        assert obj.sections[0].heading == "Formula"

    def test_parses_mcem_stage(self) -> None:
        content = (
            "---\n"
            "title: Listen & Consult\n"
            "id: mcem.stage.listen-consult\n"
            "type: MCEM Stage\n"
            "description: First stage.\n"
            "---\n"
            "# Entry Criteria\nTrigger.\n"
        )
        obj = _factory_with_ontology().parse(content, "mcem/stages/listen-consult.md")
        assert obj.type == ObjectType.STAGE
        assert obj.domain == "mcem"
