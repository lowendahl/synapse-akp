"""Hybrid search handler — multi-channel retrieval with vector support.

What: Combines alias, BM25, and vector search channels into deduplicated results.
Why: Separates search orchestration from tool dispatch and MCP wiring.
Boundaries: Consumer layer — uses LoadedPack + VectorIndex + Embedder protocols.
"""

from __future__ import annotations

import logging
from typing import Any

from akp_runtime.contracts.protocols import QueryEmbedder, VectorIndex
from akp_runtime.domain.models import SearchHit
from akp_runtime.infrastructure.duckdb_loader import DuckDBLoadedPack

logger = logging.getLogger(__name__)


class HybridSearchHandler:
    """Orchestrates multi-channel search across a single pack."""

    def __init__(
        self,
        pack: DuckDBLoadedPack,
        vector_index: VectorIndex | None = None,
        embedder: QueryEmbedder | None = None,
    ) -> None:
        self._pack = pack
        self._vector_index = vector_index
        self._embedder = embedder

    def search(self, query: str, limit: int, object_types: list[str]) -> list[dict[str, Any]]:
        """Execute hybrid search: alias → BM25 → vector → deduplicate → filter."""
        # Channel 1: Exact alias match (highest priority)
        hits = self._pack.exact_matches(query, limit=limit)

        # Channel 2: BM25 lexical search
        lexical_hits = self._pack.lexical_matches(query, top_k=limit * 2)

        # Channel 3: Vector semantic search
        vector_hits = self._vector_search(query, limit)

        # Merge: deduplicate by object_id, prioritize exact > lexical > vector
        seen_ids: set[str] = set()
        merged: list[SearchHit] = []
        for hit_list in [hits, lexical_hits, vector_hits]:
            for hit in hit_list:
                if hit.object_id not in seen_ids:
                    seen_ids.add(hit.object_id)
                    merged.append(hit)

        # Fallback if nothing found
        if not merged:
            merged = self._pack.object_fallback(query, limit=limit)

        # Filter by type and serialize
        results: list[dict[str, Any]] = []
        for hit in merged:
            if object_types and hit.object_type not in object_types:
                continue
            results.append(
                {
                    "pack_id": hit.pack_id,
                    "object_id": hit.object_id,
                    "title": hit.title,
                    "object_type": hit.object_type,
                    "domain": hit.domain,
                    "snippet": hit.snippet or "",
                    "score": hit.score,
                }
            )
            if len(results) >= limit:
                break

        return results

    def _vector_search(self, query: str, limit: int) -> list[SearchHit]:
        """Run vector semantic search if embedder and index are available."""
        if not self._embedder or not self._vector_index:
            return []

        try:
            query_vector = self._embedder.embed_query(query)
            nearest = self._vector_index.search(query_vector, top_k=limit * 2)
            results: list[SearchHit] = []
            for unit_id, score in nearest:
                object_id = self._extract_object_id(unit_id)
                if object_id:
                    obj_hit = self._pack.lookup_concept(object_id)
                    if obj_hit:
                        obj_hit.score = score
                        results.append(obj_hit)
            return results
        except Exception:
            logger.debug("Vector search failed", exc_info=True)
            return []

    @staticmethod
    def _extract_object_id(unit_id: str) -> str | None:
        """Extract object_id from unit_id format 'su:object_id:suffix'."""
        parts = unit_id.split(":")
        if len(parts) >= 3:
            # su:mcem.metric.pipeline-coverage-index-pci:0 → mcem.metric.pipeline-coverage-index-pci
            return ":".join(parts[1:-1])
        elif len(parts) == 2:
            return parts[1]
        return None
