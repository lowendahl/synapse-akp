"""Pack extraction helpers for the explorer."""

from __future__ import annotations

import json
from pathlib import Path

import duckdb

from kp_compiler.consumer.queries import (
    AliasRegistryQuery,
    CrossPackReferenceQuery,
    EdgeListQuery,
    LegacyCrossPackReferenceQuery,
    ObjectListQuery,
    SemanticUnitSectionsQuery,
)


class PackDataExtractor:
    """Extracts graph-ready data from compiled packs."""

    def extract_pack_data(self, pack_path: Path) -> dict:
        import duckdb

        connection = duckdb.connect(str(pack_path), read_only=True)
        pack_id = pack_path.stem
        domain = pack_id.removeprefix("kp-")
        try:
            nodes = self._nodes(connection, pack_id, domain)
            edges = self._edges(connection, pack_id)
            cross_refs = self._cross_refs(connection, pack_id)
            units = self._units_by_object(connection)
            aliases = self._aliases_by_object(connection)
        finally:
            connection.close()
        for node in nodes:
            node["sections"] = units.get(node["id"], [])[:10]
            node["aliases"] = aliases.get(node["id"], [])[:20]
        return {"nodes": nodes, "edges": edges, "cross_refs": cross_refs}

    def build_graph_json(self, pack_paths: list[Path]) -> str:
        nodes: list[dict] = []
        links: list[dict] = []
        node_ids: set[str] = set()
        for pack_path in pack_paths:
            data = self.extract_pack_data(pack_path)
            nodes.extend(data["nodes"])
            node_ids.update(node["id"] for node in data["nodes"])
            links.extend(data["edges"])
            links.extend(data["cross_refs"])
        seen: set[tuple[str, str, str]] = set()
        valid = []
        for link in links:
            source = link["source"]
            target = link["target"]
            # Resolve qualified cross-pack IDs to short node IDs
            if source not in node_ids:
                source = self._resolve_qualified_id(source, node_ids)
            if target not in node_ids:
                target = self._resolve_qualified_id(target, node_ids)
            if source and target:
                predicate = link.get("predicate", "references")
                key = (source, target, predicate)
                if key not in seen:
                    seen.add(key)
                    valid.append({**link, "source": source, "target": target})
        return json.dumps({"nodes": nodes, "links": valid})

    def _resolve_qualified_id(self, qualified_id: str, node_ids: set[str]) -> str | None:
        """Resolve a qualified cross-pack ID (e.g. mcem.stage.stage-1) to a node ID."""
        # Try as-is first
        if qualified_id in node_ids:
            return qualified_id
        # Strip domain.type. prefix: mcem.stage.stage-1-listen-consult -> stage-1-listen-consult
        parts = qualified_id.split(".")
        if len(parts) >= 3:
            short_id = ".".join(parts[2:])
            if short_id in node_ids:
                return short_id
        # Try last segment only
        if parts[-1] in node_ids:
            return parts[-1]
        return None

    def _nodes(
        self,
        connection: duckdb.DuckDBPyConnection,
        pack_id: str,
        domain: str,
    ) -> list[dict]:
        return [
            {
                "id": row[0],
                "title": row[1] or row[0],
                "type": row[2] or "Unknown",
                "domain": row[3] or domain,
                "pack": pack_id,
                "description": (row[4] or "")[:500],
            }
            for row in ObjectListQuery().execute(connection)
        ]

    def _edges(self, connection: duckdb.DuckDBPyConnection, pack_id: str) -> list[dict]:
        return [
            {"source": row[0], "target": row[1], "predicate": row[2] or "references", "pack": pack_id}
            for row in EdgeListQuery().execute(connection)
        ]

    def _cross_refs(self, connection: duckdb.DuckDBPyConnection, pack_id: str) -> list[dict]:
        try:
            rows = CrossPackReferenceQuery().execute(connection)
        except Exception:
            rows = [(row[0], row[1], "references") for row in LegacyCrossPackReferenceQuery().execute(connection)]
        return [
            {
                "source": row[0],
                "target": row[1],
                "predicate": row[2] or "references",
                "pack": pack_id,
                "cross_pack": True,
            }
            for row in rows
        ]

    def _units_by_object(self, connection: duckdb.DuckDBPyConnection) -> dict[str, list[dict]]:
        result: dict[str, list[dict]] = {}
        for _, source_object_id, heading, content in SemanticUnitSectionsQuery().execute(connection):
            result.setdefault(source_object_id, []).append({"heading": heading or "", "content": (content or "")[:400]})
        return result

    def _aliases_by_object(self, connection: duckdb.DuckDBPyConnection) -> dict[str, list[str]]:
        result: dict[str, list[str]] = {}
        for alias, canonical_id, _ in AliasRegistryQuery().execute(connection):
            result.setdefault(canonical_id, []).append(alias)
        return result
