"""Knowledge Pack Compiler CLI entry point."""

from __future__ import annotations

from pathlib import Path


class CompilerCli:
    """Command-line application for pack compilation."""

    @staticmethod
    def build_parser() -> object:
        import argparse

        parser = argparse.ArgumentParser(
            prog="kp-compile",
            description="Compile OKF canonical sources into an immutable Knowledge Pack",
        )
        parser.add_argument("source", type=Path, help="Path to OKF source directory (e.g., okf/csu or okf/mcem)")
        parser.add_argument("--ontology", type=Path, default=Path("okf/ontology.yaml"), help="Path to ontology.yaml")
        parser.add_argument(
            "--output",
            type=Path,
            default=Path("dist/kp-csu.duckdb"),
            help="Output path for the Knowledge Pack",
        )
        parser.add_argument("--pack-id", default="kp-csu", help="Pack identifier")
        parser.add_argument("--validate-only", action="store_true", help="Run validation without producing a pack")
        parser.add_argument(
            "--dependency-pack",
            type=Path,
            default=None,
            help="Path to dependency pack for cross-pack validation (e.g., dist/kp-mcem.duckdb)",
        )
        parser.add_argument("--skip-embeddings", action="store_true", help="Skip the dense embedding stage")
        parser.add_argument(
            "--discover-ontology",
            action="store_true",
            help="Discover ontology from corpus and emit or merge ontology.yaml",
        )
        parser.add_argument("--rules", type=Path, default=None, help="Path to pack-rules.yaml")
        return parser

    @staticmethod
    def _apply_manifest_defaults(args: object) -> None:
        pack_yaml = args.source / "pack.yaml"
        if not pack_yaml.exists():
            return

        from ruamel.yaml import YAML

        yaml = YAML(typ="safe")
        manifest = yaml.load(pack_yaml.read_text(encoding="utf-8"))
        print(f"[manifest] Loaded {pack_yaml}")

        if args.pack_id == "kp-csu":
            args.pack_id = manifest.get("id", args.pack_id)
        if args.output == Path("dist/kp-csu.duckdb"):
            compile_cfg = manifest.get("compile", {})
            if "output" in compile_cfg:
                args.output = args.source / compile_cfg["output"]
        if args.ontology == Path("okf/ontology.yaml"):
            ontology_relative_path = manifest.get("ontology")
            if ontology_relative_path:
                args.ontology = (args.source / ontology_relative_path).resolve()
        if args.rules is None:
            rules_relative_path = manifest.get("rules")
            if rules_relative_path:
                args.rules = (args.source / rules_relative_path).resolve()
        if args.dependency_pack is None:
            dependencies = manifest.get("dependencies", [])
            if not dependencies:
                return
            dependency_path = dependencies[0].get("path", "")
            dependency_pack_yaml = args.source / dependency_path / "pack.yaml"
            if not dependency_pack_yaml.exists():
                return
            dependency_manifest = yaml.load(dependency_pack_yaml.read_text(encoding="utf-8"))
            dependency_output = dependency_manifest.get("compile", {}).get("output", "")
            if not dependency_output:
                return
            candidate = (args.source / dependency_path / dependency_output).resolve()
            if candidate.exists():
                args.dependency_pack = candidate
                print(f"[manifest] Auto-resolved dependency: {candidate}")

    def run(self, argv: list[str] | None = None) -> int:
        """Run the compiler CLI and return a process exit code."""
        parser = self.build_parser()
        args = parser.parse_args(argv)

        if not args.source.exists():
            print(f"Error: source path '{args.source}' does not exist")
            return 1

        self._apply_manifest_defaults(args)

        if not args.discover_ontology and not args.ontology.exists():
            print(f"Error: ontology path '{args.ontology}' does not exist")
            print("Hint: use --discover-ontology to generate one from the corpus")
            return 1

        from kp_compiler.infrastructure.rules_loader import load_pack_rules
        from kp_compiler.pipeline.compiler import PackCompiler

        rules_path = args.rules or (args.source.parent / "pack-rules.yaml")
        rules = load_pack_rules(rules_path)
        if rules_path.exists():
            print(f"[rules] Loaded {rules_path}")
        else:
            print("[rules] Using defaults (no pack-rules.yaml found)")

        success, _diagnostics = PackCompiler().compile_pack(
            source_root=args.source,
            ontology_path=args.ontology,
            output_path=args.output,
            pack_id=args.pack_id,
            dependency_pack=args.dependency_pack,
            skip_embeddings=args.skip_embeddings,
            discover_ontology=args.discover_ontology,
            rules=rules,
        )
        return 0 if success else 1


def main() -> None:
    """Entry point for kp-compile command."""
    raise SystemExit(CompilerCli().run())


if __name__ == "__main__":
    main()
