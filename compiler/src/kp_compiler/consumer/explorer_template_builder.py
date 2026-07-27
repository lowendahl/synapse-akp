"""HTML template assembly for the pack explorer."""

from __future__ import annotations

import sys
from pathlib import Path


class ExplorerTemplateBuilder:
    """Inlines explorer assets into a self-contained HTML page."""

    def get_html_template(self) -> str:
        app_dir = Path(__file__).parent / "explorer-app"
        vendor_dir = Path(__file__).parent / "vendor"
        app_scripts = [
            "constants.js",
            "markdown.js",
            "nebula.js",
            "graph-config.js",
            "hover.js",
            "drawer.js",
            "main.js",
        ]
        html_path = app_dir / "index.html"
        if not html_path.exists():
            print("Error: explorer-app/index.html not found", file=sys.stderr)
            raise SystemExit(1)
        html = html_path.read_text(encoding="utf-8")
        html = html.replace(
            "<!-- __CSS_PLACEHOLDER__ -->",
            "<style>\n" + self._join_files(app_dir / "css", ["theme.css", "layout.css", "drawer.css"]) + "\n</style>",
        )
        html = html.replace(
            "<!-- __VENDOR_PLACEHOLDER__ -->",
            self._script_block(vendor_dir, ["3d-force-graph.min.js"]),
        )
        html = html.replace(
            "<!-- __APP_JS_PLACEHOLDER__ -->",
            "<script>\n" + self._join_files(app_dir / "js", app_scripts, prefix="// ── {name} ──\n") + "\n</script>",
        )
        return html

    def _join_files(self, directory: Path, names: list[str], prefix: str = "/* {name} */\n") -> str:
        parts = []
        for name in names:
            path = directory / name
            if path.exists():
                parts.append(prefix.format(name=name) + path.read_text(encoding="utf-8"))
        return "\n".join(parts)

    def _script_block(self, directory: Path, names: list[str]) -> str:
        return "\n".join(
            f"<script>\n{(directory / name).read_text(encoding='utf-8')}\n</script>"
            for name in names
            if (directory / name).exists()
        )
