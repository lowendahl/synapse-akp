"""pack.yaml `source_root` decouples the discovery root from the config dir.

A small sibling pack dir can point at an authored tree it does not own (ADR-010: the
website `knowledge/` tree is the single source; its pack config stays out of it).
"""

from __future__ import annotations

from argparse import Namespace
from pathlib import Path

from kp_compiler.cli import CompilerCli


def _config_dir(tmp_path: Path, source_root_value: str) -> Path:
    config = tmp_path / "pack"
    config.mkdir()
    (config / "pack.yaml").write_text(
        "id: kp-example\n"
        "domain: example\n"
        "ontology: ./ontology.yaml\n"
        "rules: ./pack-rules.yaml\n"
        f"source_root: {source_root_value}\n"
        "exclude: [assets/**]\n",
        encoding="utf-8",
    )
    (config / "ontology.yaml").write_text("version: '0.1.0'\ntypes: {}\n", encoding="utf-8")
    (config / "pack-rules.yaml").write_text("min_objects: 1\n", encoding="utf-8")
    return config


def test_source_root_points_discovery_at_a_sibling_tree(tmp_path: Path) -> None:
    sources = tmp_path / "knowledge"
    (sources / "concepts").mkdir(parents=True)
    (sources / "concepts" / "a.md").write_text("# a\n", encoding="utf-8")

    config = _config_dir(tmp_path, "../knowledge")
    args = Namespace(
        source=config,
        pack_id="kp-csu",
        output=Path("dist/kp-csu.duckdb"),
        ontology=Path("okf/ontology.yaml"),
        rules=None,
        dependency_pack=None,
    )
    CompilerCli._apply_manifest_defaults(args)

    assert args.discovery_root == sources.resolve()
    # Config (ontology/rules) still resolves against the config dir, not the source tree.
    assert args.ontology == (config / "ontology.yaml").resolve()
    assert args.rules == (config / "pack-rules.yaml").resolve()


def test_absent_source_root_leaves_discovery_at_config_dir(tmp_path: Path) -> None:
    config = tmp_path / "okf-style"
    config.mkdir()
    (config / "pack.yaml").write_text("id: kp-inline\ndomain: inline\n", encoding="utf-8")
    args = Namespace(
        source=config,
        pack_id="kp-csu",
        output=Path("dist/kp-csu.duckdb"),
        ontology=Path("okf/ontology.yaml"),
        rules=None,
        dependency_pack=None,
    )
    CompilerCli._apply_manifest_defaults(args)

    assert not hasattr(args, "discovery_root")
