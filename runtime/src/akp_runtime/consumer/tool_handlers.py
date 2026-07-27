"""Tool handler registry — maps MCP tool calls to runtime operations.

What: Stateless handler methods that delegate to LoadedPack operations.
Why: Keeps MCP server thin; business logic stays in operations layer.
Boundaries: Only imports from contracts + operations + domain.
"""

from __future__ import annotations

import logging
from typing import Any

from akp_runtime.consumer.search_handler import HybridSearchHandler
from akp_runtime.contracts.protocols import QueryEmbedder, VectorIndex
from akp_runtime.infrastructure.duckdb_loader import DuckDBLoadedPack
from akp_runtime.operations.explain_concept import ExplainConceptOperation

logger = logging.getLogger(__name__)


class ToolHandlerRegistry:
    """Dispatches MCP tool calls to the appropriate pack operations."""

    def __init__(
        self,
        packs: dict[str, DuckDBLoadedPack],
        vector_indexes: dict[str, VectorIndex] | None = None,
        embedder: QueryEmbedder | None = None,
    ) -> None:
        self._packs = packs
        self._vector_indexes = vector_indexes or {}
        self._embedder = embedder

    def handle_search(
        self,
        query: str,
        limit: int,
        pack_ids: list[str],
        object_types: list[str],
    ) -> dict[str, Any]:
        """Search across packs using hybrid retrieval (alias + BM25 + vectors)."""
        results: list[dict] = []
        target_packs = self._resolve_packs(pack_ids)

        for pack_id, pack in target_packs.items():
            handler = HybridSearchHandler(
                pack=pack,
                vector_index=self._vector_indexes.get(pack_id),
                embedder=self._embedder,
            )
            pack_results = handler.search(query, limit=limit - len(results), object_types=object_types)
            results.extend(pack_results)
            if len(results) >= limit:
                break

        return {"results": results[:limit], "total": len(results)}

    def handle_lookup(
        self,
        identifier: str,
        include_units: bool,
        include_neighbors: bool,
        neighbor_limit: int,
    ) -> dict[str, Any]:
        """Look up a concept by ID or alias across all packs."""
        for _pack_id, pack in self._packs.items():
            hit = pack.lookup_concept(identifier)
            if hit is None:
                matches = pack.exact_matches(identifier, limit=1)
                if matches:
                    hit = matches[0]

            if hit is None:
                continue

            result: dict[str, Any] = {
                "pack_id": hit.pack_id,
                "object_id": hit.object_id,
                "title": hit.title,
                "object_type": hit.object_type,
                "domain": hit.domain,
                "description": hit.snippet or "",
            }

            if include_units:
                units = pack.concept_units(hit.object_id, limit=50)
                result["units"] = [
                    {"unit_id": u.unit_id, "heading_path": u.heading_path, "content": u.content} for u in units
                ]

            if include_neighbors:
                neighbors = pack.graph_neighbors(hit.object_id, hops=1, predicates=(), limit=neighbor_limit)
                result["neighbors"] = [
                    {
                        "subject_id": n.subject_id,
                        "predicate": n.predicate,
                        "object_id": n.object_id,
                        "neighbor_title": n.neighbor_title,
                        "neighbor_type": n.neighbor_type,
                    }
                    for n in neighbors
                ]

            return result

        return {"error": f"Concept not found: {identifier}"}

    def handle_explain(self, query: str, detail_level: str) -> dict[str, Any]:
        """Explain a concept using the first pack that resolves it."""
        for _pack_id, pack in self._packs.items():
            operation = ExplainConceptOperation(pack=pack, reasoning_client=None)
            result = operation.explain(query, detail_level=detail_level)
            if result is not None:
                return {
                    "concept_title": result.concept_title,
                    "explanation": result.explanation,
                    "cited_unit_ids": result.cited_unit_ids,
                    "synthesis_method": result.synthesis_method,
                    "fallback_reason": result.fallback_reason,
                    "detail_level": result.detail_level,
                    "neighbor_titles": result.neighbor_titles,
                }

        return {"error": f"No concept found for: {query}"}

    def handle_expand_graph(
        self,
        object_id: str,
        hops: int,
        predicates: tuple[str, ...],
        limit: int,
    ) -> dict[str, Any]:
        """Expand the graph from a seed object."""
        for _pack_id, pack in self._packs.items():
            neighbors = pack.graph_neighbors(object_id, hops=hops, predicates=predicates, limit=limit)
            if neighbors:
                return {
                    "seed_object_id": object_id,
                    "hops": hops,
                    "edges": [
                        {
                            "subject_id": n.subject_id,
                            "predicate": n.predicate,
                            "object_id": n.object_id,
                            "neighbor_title": n.neighbor_title,
                            "neighbor_type": n.neighbor_type,
                            "confidence": n.confidence,
                        }
                        for n in neighbors
                    ],
                }

        return {"seed_object_id": object_id, "hops": hops, "edges": []}

    def handle_provenance(
        self,
        object_id: str | None,
        unit_id: str | None,
        edge_subject_id: str | None,
        edge_predicate: str | None,
        edge_object_id: str | None,
    ) -> dict[str, Any]:
        """Trace provenance for an artifact."""
        targets = sum([object_id is not None, unit_id is not None, edge_subject_id is not None])
        if targets != 1:
            return {"error": "Provide exactly one target: object_id, unit_id, or edge (subject+predicate+object)"}

        for _pack_id, pack in self._packs.items():
            if object_id:
                steps = pack.provenance_for_object(object_id)
                if steps:
                    return {
                        "target_type": "object",
                        "target_id": object_id,
                        "provenance": [self._step_to_dict(s) for s in steps],
                    }
            elif unit_id:
                steps = pack.provenance_for_unit(unit_id)
                if steps:
                    return {
                        "target_type": "semantic_unit",
                        "target_id": unit_id,
                        "provenance": [self._step_to_dict(s) for s in steps],
                    }
            elif edge_subject_id and edge_predicate and edge_object_id:
                steps = pack.provenance_for_edge(edge_subject_id, edge_predicate, edge_object_id)
                if steps:
                    return {
                        "target_type": "edge",
                        "target_id": f"{edge_subject_id}→{edge_predicate}→{edge_object_id}",
                        "provenance": [self._step_to_dict(s) for s in steps],
                    }

        return {"error": "No provenance found for the specified target"}

    def _resolve_packs(self, pack_ids: list[str]) -> dict[str, DuckDBLoadedPack]:
        """Filter packs by ID list, or return all if empty."""
        if not pack_ids:
            return self._packs
        return {pid: p for pid, p in self._packs.items() if pid in pack_ids}

    @staticmethod
    def _step_to_dict(step: object) -> dict[str, Any]:
        """Convert a ProvenanceStep to dict."""
        return {
            "layer": getattr(step, "layer", "unknown"),
            "identifier": getattr(step, "identifier", ""),
            "origin": getattr(step, "origin", "authored"),
            "source_path": getattr(step, "source_path", None),
            "pack_id": getattr(step, "pack_id", None),
            "pack_version": getattr(step, "pack_version", None),
        }
