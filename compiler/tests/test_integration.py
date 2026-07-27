"""Integration test — full pipeline compile + consumer query."""

import tempfile
from pathlib import Path

import duckdb

from kp_compiler.pipeline.compiler import compile_pack

FIXTURE_ONTOLOGY = {
    "version": "1.0.0",
    "id_pattern": r"^[a-z]+\.[a-z]+\.[a-z0-9-]+$",
    "object_types": {
        "Metric": {"description": "A metric", "required_fields": ["id", "title"]},
        "Stage": {"description": "A stage", "required_fields": ["id", "title"]},
        "Process": {"description": "A process", "required_fields": ["id", "title"]},
        "Pipeline": {"description": "Pipeline", "required_fields": ["id", "title"]},
        "Index": {"description": "Index page", "required_fields": []},
        "Log": {"description": "Change log", "required_fields": []},
    },
    "predicates": {
        "references": {"description": "References another object"},
        "depends_on": {"description": "Depends on another object"},
    },
    "constraints": [],
}


def _write_fixture_corpus(tmpdir: Path) -> Path:
    """Create a minimal OKF fixture corpus."""
    corpus = tmpdir / "okf" / "csu"
    metrics = corpus / "metrics"
    metrics.mkdir(parents=True)

    (metrics / "job1.md").write_text(
        "---\n"
        "title: Job 1 C2C\n"
        "id: csu.metric.job1-c2c\n"
        "type: Metric\n"
        "aliases:\n  - C2C\n  - Commit to Complete\n"
        "tags:\n  - kpi\n  - pipeline\n"
        "description: Committed milestone completion rate.\n"
        "---\n"
        "# Formula\nC2C = closed / committed\n"
        "# Source Systems\n- MSX Dataverse\n",
        encoding="utf-8",
    )

    (metrics / "udc.md").write_text(
        "---\n"
        "title: UDC\n"
        "id: csu.metric.udc\n"
        "type: Metric\n"
        "aliases:\n  - Unified Delivery Coverage\n"
        "tags:\n  - delivery\n"
        "description: Delivery coverage percentage.\n"
        "---\n"
        "# Definition\nUDC measures delivery against entitlement.\n",
        encoding="utf-8",
    )

    return corpus


def _write_ontology(tmpdir: Path) -> Path:
    """Write a fixture ontology.yaml."""
    from ruamel.yaml import YAML

    ontology_path = tmpdir / "ontology.yaml"
    yaml = YAML()
    with open(ontology_path, "w", encoding="utf-8") as f:
        yaml.dump(FIXTURE_ONTOLOGY, f)
    return ontology_path


class TestFullPipeline:
    def test_compile_produces_queryable_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            corpus = _write_fixture_corpus(tmpdir)
            ontology = _write_ontology(tmpdir)
            output = tmpdir / "test.duckdb"

            from kp_compiler.domain.rules import PackRules

            # Use rules with no outcome assertions — test corpus is too small
            rules = PackRules.model_validate({"outcome_assertions": []})

            success, diagnostics = compile_pack(
                source_root=corpus,
                ontology_path=ontology,
                output_path=output,
                pack_id="test-pack",
                rules=rules,
            )

            assert success is True
            assert output.exists()

            # Query the pack
            con = duckdb.connect(str(output), read_only=True)

            # Objects table
            objects = con.execute("SELECT id, title, type FROM objects ORDER BY id").fetchall()
            assert len(objects) == 2
            ids = [r[0] for r in objects]
            assert "csu.metric.job1-c2c" in ids
            assert "csu.metric.udc" in ids

            # Aliases
            alias_count = con.execute("SELECT COUNT(*) FROM aliases").fetchone()[0]
            assert alias_count > 0

            c2c_alias = con.execute("SELECT canonical_id FROM aliases WHERE alias = 'c2c'").fetchone()
            assert c2c_alias is not None
            assert c2c_alias[0] == "csu.metric.job1-c2c"

            # Semantic units
            unit_count = con.execute("SELECT COUNT(*) FROM semantic_units").fetchone()[0]
            assert unit_count > 0

            # Nodes
            node_count = con.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]
            assert node_count == 2

            # Manifest
            pack_id = con.execute("SELECT value FROM manifest WHERE key = 'pack_id'").fetchone()
            assert pack_id[0] == "test-pack"

            con.close()
