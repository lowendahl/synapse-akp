"""Knowledge Pack explorer CLI."""

from __future__ import annotations

import json
from pathlib import Path

from kp_compiler.consumer.explorer_template_builder import ExplorerTemplateBuilder
from kp_compiler.consumer.pack_data_extractor import PackDataExtractor


class ExplorerGenerator:
    """Backward-compatible CLI wrapper for explorer generation."""

    def __init__(self) -> None:
        self._explorer = KnowledgePackExplorer()

    def run(self, argv: list[str] | None = None) -> int:
        _ = argv
        self._explorer.main()
        return 0


class KnowledgePackExplorer:
    """Builds a self-contained explorer HTML artifact."""

    def __init__(self) -> None:
        self._extractor = PackDataExtractor()
        self._template_builder = ExplorerTemplateBuilder()

    def main(self) -> None:
        import argparse

        parser = argparse.ArgumentParser(
            prog="kp-explore",
            description="Generate a 3D interactive Knowledge Pack explorer",
        )
        parser.add_argument("packs", type=Path, nargs="+")
        parser.add_argument("--output", "-o", type=Path, default=Path("dist/pack-explorer.html"))
        args = parser.parse_args()
        for pack_path in args.packs:
            if not pack_path.exists():
                print(f"Error: pack '{pack_path}' does not exist. Run kp-compile first.")
                raise SystemExit(1)
        print(f"[explore] Loading {len(args.packs)} pack(s)...")
        graph_json = self._extractor.build_graph_json(args.packs)
        data = json.loads(graph_json)
        print(f"[explore] {len(data['nodes'])} nodes, {len(data['links'])} edges")
        html = self._template_builder.get_html_template().replace("__GRAPH_DATA_PLACEHOLDER__", graph_json)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(html, encoding="utf-8")
        size_kb = round(args.output.stat().st_size / 1024, 1)
        print(f"[explore] Written to {args.output} ({size_kb}KB)")
        print(f"[explore] Open in browser: file:///{args.output.resolve().as_posix()}")

    def extract_pack_data(self, pack_path: Path) -> dict:
        return self._extractor.extract_pack_data(pack_path)

    def build_graph_json(self, pack_paths: list[Path]) -> str:
        return self._extractor.build_graph_json(pack_paths)

    def get_html_template(self) -> str:
        return self._template_builder.get_html_template()


_explorer = KnowledgePackExplorer()
_generator = ExplorerGenerator()
extract_pack_data = _explorer.extract_pack_data
build_graph_json = _explorer.build_graph_json
get_html_template = _explorer.get_html_template


def main() -> None:
    raise SystemExit(_generator.run())


if __name__ == "__main__":
    main()
