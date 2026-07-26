"""Knowledge Pack Explorer — generates a 3D interactive graph viewer.

Usage:
    kp-explore dist/kp-csu.duckdb dist/kp-mcem.duckdb
    kp-explore dist/kp-csu.duckdb --output explorer.html
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def extract_pack_data(pack_path: Path) -> dict:
    """Extract nodes, edges, aliases, and sections from a compiled pack."""
    import duckdb

    con = duckdb.connect(str(pack_path), read_only=True)
    pack_id = pack_path.stem  # e.g. kp-csu
    domain = pack_id.removeprefix("kp-")

    nodes = []
    for oid, title, otype, dom, desc in con.execute(
        "SELECT id, title, type, domain, description FROM objects"
    ).fetchall():
        nodes.append({
            "id": oid,
            "title": title or oid,
            "type": otype or "Unknown",
            "domain": dom or domain,
            "pack": pack_id,
            "description": (desc or "")[:500],
        })

    edges = []
    for src, tgt, pred in con.execute(
        "SELECT subject_id, object_id, predicate FROM edges"
    ).fetchall():
        edges.append({
            "source": src,
            "target": tgt,
            "predicate": pred or "references",
            "pack": pack_id,
        })

    # Cross-pack refs (with predicate since v0.2)
    cross_refs = []
    try:
        rows = con.execute(
            "SELECT source_id, target_qualified_id, predicate "
            "FROM cross_pack_refs WHERE resolved = true"
        ).fetchall()
    except Exception:
        # Fallback for packs without predicate column
        rows = []
        for src, tgt, _, resolved in con.execute(
            "SELECT source_id, target_qualified_id, target_pack, resolved "
            "FROM cross_pack_refs WHERE resolved = true"
        ).fetchall():
            rows.append((src, tgt, "references"))

    for src, tgt, pred in rows:
        cross_refs.append({
            "source": src,
            "target": tgt,
            "predicate": pred or "references",
            "pack": pack_id,
            "cross_pack": True,
        })

    # Semantic units for detail drawer
    units_by_obj: dict[str, list[dict]] = {}
    for _, sobj, heading, content in con.execute(
        "SELECT id, source_object_id, heading_path, content "
        "FROM semantic_units ORDER BY source_object_id, id"
    ).fetchall():
        units_by_obj.setdefault(sobj, []).append({
            "heading": heading or "",
            "content": (content or "")[:400],
        })

    # Aliases
    aliases_by_obj: dict[str, list[str]] = {}
    for alias, cid, _ in con.execute(
        "SELECT alias, canonical_id, alias_type FROM aliases"
    ).fetchall():
        aliases_by_obj.setdefault(cid, []).append(alias)

    for n in nodes:
        n["sections"] = units_by_obj.get(n["id"], [])[:10]
        n["aliases"] = aliases_by_obj.get(n["id"], [])[:20]

    con.close()
    return {"nodes": nodes, "edges": edges, "cross_refs": cross_refs}


def build_graph_json(pack_paths: list[Path]) -> str:
    """Merge data from multiple packs into a single graph JSON."""
    all_nodes: list[dict] = []
    all_links: list[dict] = []
    node_ids: set[str] = set()

    for pp in pack_paths:
        data = extract_pack_data(pp)
        all_nodes.extend(data["nodes"])
        node_ids.update(n["id"] for n in data["nodes"])
        all_links.extend(data["edges"])
        all_links.extend(data["cross_refs"])

    # Filter orphan links and deduplicate cross-pack refs
    seen: set[tuple[str, str]] = set()
    valid: list[dict] = []
    for l in all_links:
        if l["source"] not in node_ids or l["target"] not in node_ids:
            continue
        key = (l["source"], l["target"])
        if key in seen:
            continue
        seen.add(key)
        valid.append(l)
    return json.dumps({"nodes": all_nodes, "links": valid})


def get_html_template() -> str:
    """Assemble explorer HTML from modular source files.

    Reads explorer-app/index.html and inlines CSS, vendor JS, and app JS
    into their respective placeholder positions.
    """
    app_dir = Path(__file__).parent / "explorer-app"
    vendor_dir = Path(__file__).parent / "vendor"

    html_path = app_dir / "index.html"
    if not html_path.exists():
        print("Error: explorer-app/index.html not found", file=sys.stderr)
        sys.exit(1)

    html = html_path.read_text(encoding="utf-8")

    # ── Inline CSS ──────────────────────────────────────────
    css_files = ["theme.css", "layout.css", "drawer.css"]
    css_parts = []
    for name in css_files:
        p = app_dir / "css" / name
        if p.exists():
            css_parts.append(f"/* {name} */\n{p.read_text(encoding='utf-8')}")
    html = html.replace(
        "<!-- __CSS_PLACEHOLDER__ -->",
        f"<style>\n{''.join(css_parts)}\n</style>",
    )

    # ── Inline vendor JS ────────────────────────────────────
    vendor_files = ["3d-force-graph.min.js"]
    vendor_parts = []
    for name in vendor_files:
        p = vendor_dir / name
        if p.exists():
            vendor_parts.append(f"<script>\n{p.read_text(encoding='utf-8')}\n</script>")
    html = html.replace(
        "<!-- __VENDOR_PLACEHOLDER__ -->",
        "\n".join(vendor_parts),
    )

    # ── Inline app JS (order matters) ───────────────────────
    js_files = ["constants.js", "markdown.js", "nebula.js",
                "graph-config.js", "hover.js", "drawer.js", "main.js"]
    js_parts = []
    for name in js_files:
        p = app_dir / "js" / name
        if p.exists():
            js_parts.append(f"// ── {name} ──\n{p.read_text(encoding='utf-8')}")
    html = html.replace(
        "<!-- __APP_JS_PLACEHOLDER__ -->",
        f"<script>\n{''.join(js_parts)}\n</script>",
    )

    return html


def main() -> None:
    """Entry point for kp-explore command."""
    import argparse

    parser = argparse.ArgumentParser(
        prog="kp-explore",
        description="Generate a 3D interactive Knowledge Pack explorer",
    )
    parser.add_argument(
        "packs",
        type=Path,
        nargs="+",
        help="Paths to compiled pack(s) (.duckdb files)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("dist/pack-explorer.html"),
        help="Output HTML file path (default: dist/pack-explorer.html)",
    )

    args = parser.parse_args()

    # Validate packs exist
    for p in args.packs:
        if not p.exists():
            print(f"Error: pack '{p}' does not exist. Run kp-compile first.")
            sys.exit(1)

    # Extract and merge
    print(f"[explore] Loading {len(args.packs)} pack(s)...")
    graph_json = build_graph_json(args.packs)

    data = json.loads(graph_json)
    print(f"[explore] {len(data['nodes'])} nodes, {len(data['links'])} edges")

    # Build HTML
    template = get_html_template()
    html = template.replace("__GRAPH_DATA_PLACEHOLDER__", graph_json)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html, encoding="utf-8")
    size_kb = round(args.output.stat().st_size / 1024, 1)
    print(f"[explore] Written to {args.output} ({size_kb}KB)")
    print(f"[explore] Open in browser: file:///{args.output.resolve().as_posix()}")


if __name__ == "__main__":
    main()
