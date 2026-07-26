"""Tests for ontology discovery stage (ADR-013)."""

import textwrap
from pathlib import Path

from kp_compiler.stages.discover_ontology import (
    OntologyDiscoveryResult,
    discover_ontology,
    generate_ontology_yaml,
)


def _write_md(tmp_path: Path, rel_path: str, frontmatter: str) -> Path:
    """Write a markdown file with frontmatter under tmp_path."""
    full = tmp_path / rel_path
    full.parent.mkdir(parents=True, exist_ok=True)
    content = f"---\n{frontmatter}\n---\n\n# Content\n"
    full.write_text(content, encoding="utf-8")
    return full


class TestDiscoverOntology:
    """Verify type and predicate extraction from frontmatter."""

    def test_discovers_types_from_frontmatter(self, tmp_path: Path) -> None:
        src = tmp_path / "csu"
        files = [
            _write_md(tmp_path, "csu/metrics/udc.md", "id: csu.metric.udc\ntitle: UDC\ntype: Metric"),
            _write_md(tmp_path, "csu/metrics/c2c.md", "id: csu.metric.c2c\ntitle: C2C\ntype: Metric"),
            _write_md(tmp_path, "csu/doctrine/csp.md", "id: csu.doctrine.csp\ntitle: CSP\ntype: Doctrine"),
        ]
        result = discover_ontology(files, src)

        assert "Metric" in result.types
        assert "Doctrine" in result.types
        assert result.types["Metric"].observed_count == 2
        assert "csu" in result.types["Metric"].domains

    def test_discovers_predicates_from_relationships(self, tmp_path: Path) -> None:
        src = tmp_path / "csu"
        fm = textwrap.dedent("""\
            id: csu.metric.udc
            title: UDC
            type: Metric
            relationships:
              - subject_id: csu.metric.udc
                predicate: measures
                object_id: csu.process.deploy
              - subject_id: csu.metric.udc
                predicate: evidenced_by
                object_id: csu.evidence.msxi""")
        files = [_write_md(tmp_path, "csu/metrics/udc.md", fm)]
        result = discover_ontology(files, src)

        assert "measures" in result.predicates
        assert "evidenced_by" in result.predicates
        assert "Metric" in result.predicates["measures"].subject_types

    def test_discovers_domains(self, tmp_path: Path) -> None:
        src = tmp_path / "mcem"
        files = [
            _write_md(tmp_path, "mcem/stages/envision.md", "id: mcem.stage.envision\ntitle: Envision\ntype: Stage"),
        ]
        result = discover_ontology(files, src)
        assert "mcem" in result.domains

    def test_discovers_id_prefixes(self, tmp_path: Path) -> None:
        src = tmp_path / "csu"
        files = [
            _write_md(tmp_path, "csu/metrics/udc.md", "id: csu.metric.udc\ntitle: UDC\ntype: Metric"),
        ]
        result = discover_ontology(files, src)
        assert "csu" in result.id_prefixes

    def test_handles_missing_frontmatter(self, tmp_path: Path) -> None:
        src = tmp_path / "csu"
        f = tmp_path / "csu" / "readme.md"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("# Just a readme\nNo frontmatter here.", encoding="utf-8")
        result = discover_ontology([f], src)
        assert len(result.types) == 0

    def test_empty_file_list(self, tmp_path: Path) -> None:
        src = tmp_path / "csu"
        src.mkdir(parents=True, exist_ok=True)
        result = discover_ontology([], src)
        assert result.source_count == 0
        assert len(result.types) == 0


class TestGenerateOntologyYaml:
    """Verify YAML generation from discovery results."""

    def test_generates_valid_yaml_structure(self) -> None:
        result = OntologyDiscoveryResult(
            types={"Metric": __import__("kp_compiler.stages.discover_ontology", fromlist=["DiscoveredType"]).DiscoveredType(
                name="Metric", observed_count=5, domains={"csu"}, observed_fields={"id", "title", "type"},
            )},
            predicates={},
            domains={"csu"},
            id_prefixes={"csu"},
            source_count=5,
        )
        yaml_str = generate_ontology_yaml(result)
        assert "object_types:" in yaml_str
        assert "Metric:" in yaml_str
        assert "predicates:" in yaml_str
        assert "auto_generated: true" in yaml_str

    def test_merge_preserves_existing_descriptions(self) -> None:
        from kp_compiler.stages.discover_ontology import DiscoveredType

        result = OntologyDiscoveryResult(
            types={"Metric": DiscoveredType(name="Metric", observed_count=3, domains={"csu"})},
            predicates={},
            domains={"csu"},
            id_prefixes={"csu"},
        )
        existing = {
            "object_types": {
                "Metric": {
                    "description": "A quantitative measurement",
                    "required_fields": ["id", "title", "description"],
                    "optional_fields": ["aliases", "formula"],
                    "domains": ["csu"],
                },
            },
            "predicates": {},
        }
        yaml_str = generate_ontology_yaml(result, existing)
        assert "A quantitative measurement" in yaml_str
        # Should NOT contain "Auto-discovered" since existing description exists
        assert "Auto-discovered type" not in yaml_str

    def test_marks_orphaned_types(self) -> None:
        result = OntologyDiscoveryResult(types={}, predicates={}, domains=set())
        existing = {
            "object_types": {
                "Legacy": {
                    "description": "Old type",
                    "required_fields": ["id"],
                    "domains": ["csu"],
                },
            },
            "predicates": {},
        }
        yaml_str = generate_ontology_yaml(result, existing)
        assert "ORPHAN" in yaml_str

    def test_marks_new_types(self) -> None:
        from kp_compiler.stages.discover_ontology import DiscoveredType

        result = OntologyDiscoveryResult(
            types={"Widget": DiscoveredType(name="Widget", observed_count=1, domains={"csu"})},
            predicates={},
            domains={"csu"},
            id_prefixes={"csu"},
        )
        existing = {"object_types": {}, "predicates": {}}
        yaml_str = generate_ontology_yaml(result, existing)
        assert "NEW: discovered from corpus" in yaml_str
