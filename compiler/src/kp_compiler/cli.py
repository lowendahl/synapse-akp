"""Knowledge Pack Compiler CLI entry point."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> None:
    """Entry point for kp-compile command."""
    import argparse

    parser = argparse.ArgumentParser(
        prog="kp-compile",
        description="Compile OKF canonical sources into an immutable Knowledge Pack",
    )
    parser.add_argument(
        "source",
        type=Path,
        help="Path to OKF source directory (e.g., okf/csu or okf/mcem)",
    )
    parser.add_argument(
        "--ontology",
        type=Path,
        default=Path("okf/ontology.yaml"),
        help="Path to ontology.yaml",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("dist/kp-csu.duckdb"),
        help="Output path for the Knowledge Pack",
    )
    parser.add_argument(
        "--pack-id",
        default="kp-csu",
        help="Pack identifier",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Run validation without producing a pack",
    )
    parser.add_argument(
        "--dependency-pack",
        type=Path,
        default=None,
        help="Path to dependency pack for cross-pack validation (e.g., dist/kp-mcem.duckdb)",
    )
    parser.add_argument(
        "--skip-embeddings",
        action="store_true",
        help="Skip the dense embedding stage (faster builds)",
    )
    parser.add_argument(
        "--discover-ontology",
        action="store_true",
        help="Discover ontology from corpus and emit/merge ontology.yaml",
    )
    parser.add_argument(
        "--rules",
        type=Path,
        default=None,
        help="Path to pack-rules.yaml (default: <source>/../pack-rules.yaml)",
    )

    args = parser.parse_args()

    if not args.source.exists():
        print(f"Error: source path '{args.source}' does not exist")
        sys.exit(1)

    # ── Auto-detect pack.yaml manifest ──────────────────────────────────────
    pack_yaml = args.source / "pack.yaml"
    if pack_yaml.exists():
        from ruamel.yaml import YAML

        yaml = YAML(typ="safe")
        manifest = yaml.load(pack_yaml.read_text(encoding="utf-8"))
        print(f"[manifest] Loaded {pack_yaml}")

        # Apply manifest defaults — CLI flags override
        if args.pack_id == "kp-csu":  # default, not explicitly set
            args.pack_id = manifest.get("id", args.pack_id)
        if args.output == Path("dist/kp-csu.duckdb"):  # default
            compile_cfg = manifest.get("compile", {})
            if "output" in compile_cfg:
                args.output = args.source / compile_cfg["output"]
        if args.ontology == Path("okf/ontology.yaml"):  # default
            ont_rel = manifest.get("ontology")
            if ont_rel:
                args.ontology = (args.source / ont_rel).resolve()
        if args.rules is None:
            rules_rel = manifest.get("rules")
            if rules_rel:
                args.rules = (args.source / rules_rel).resolve()
        if args.dependency_pack is None:
            deps = manifest.get("dependencies", [])
            if deps:
                dep = deps[0]
                dep_path = dep.get("path", "")
                dep_pack_yaml = (args.source / dep_path / "pack.yaml")
                if dep_pack_yaml.exists():
                    dep_manifest = yaml.load(dep_pack_yaml.read_text(encoding="utf-8"))
                    dep_compile = dep_manifest.get("compile", {})
                    dep_output = dep_compile.get("output", "")
                    if dep_output:
                        candidate = (args.source / dep_path / dep_output).resolve()
                        if candidate.exists():
                            args.dependency_pack = candidate
                            print(f"[manifest] Auto-resolved dependency: {candidate}")

    if not args.discover_ontology and not args.ontology.exists():
        print(f"Error: ontology path '{args.ontology}' does not exist")
        print("Hint: use --discover-ontology to generate one from the corpus")
        sys.exit(1)

    # Load pack rules
    from kp_compiler.infrastructure.rules_loader import load_pack_rules

    rules_path = args.rules or (args.source.parent / "pack-rules.yaml")
    rules = load_pack_rules(rules_path)
    if rules_path.exists():
        print(f"[rules] Loaded {rules_path}")
    else:
        print("[rules] Using defaults (no pack-rules.yaml found)")

    from kp_compiler.pipeline.compiler import compile_pack

    success, diagnostics = compile_pack(
        source_root=args.source,
        ontology_path=args.ontology,
        output_path=args.output,
        pack_id=args.pack_id,
        dependency_pack=args.dependency_pack,
        skip_embeddings=args.skip_embeddings,
        discover_ontology=args.discover_ontology,
        rules=rules,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
