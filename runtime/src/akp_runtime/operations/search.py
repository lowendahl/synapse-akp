"""Hybrid search operation — exact + BM25 + vector + RRF + graph boost."""

from __future__ import annotations

from akp_runtime.contracts.mcp_provenance import ProvenanceStepModel
from akp_runtime.contracts.mcp_search import (
    ChannelScoreModel,
    SearchResultModel,
    SearchToolInput,
    SearchToolOutput,
)
from akp_runtime.contracts.protocols import LoadedPack, QueryEmbedder, VectorIndex
from akp_runtime.domain.scoring import ReciprocalRankFusion, GraphProximityBooster


class HybridSearchOperation:
    """Implements the full hybrid search pipeline.

    Channels:
    1. Exact alias match
    2. BM25 lexical search
    3. (Optional) Dense vector semantic search
    4. RRF fusion across channels
    5. (Optional) Graph proximity boost
    """

    def __init__(
        self,
        pack: LoadedPack,
        embedder: QueryEmbedder | None = None,
        vector_index: VectorIndex | None = None,
    ) -> None:
        self._pack = pack
        self._embedder = embedder
        self._vector_index = vector_index
        self._rrf = ReciprocalRankFusion(k=60)
        self._booster = GraphProximityBooster()

    def search(self, request: SearchToolInput) -> SearchToolOutput:
        """Execute multi-channel hybrid search with RRF fusion."""
        ranked_lists = []

        # Channel 1: Exact alias match
        exact_hits = self._pack.exact_matches(request.query, limit=request.limit)
        if exact_hits:
            ranked_lists.append(exact_hits)

        # Channel 2: BM25 lexical search
        lexical_hits = self._pack.lexical_matches(request.query, top_k=request.limit * 2)
        if lexical_hits:
            ranked_lists.append(lexical_hits)

        # Channel 3: Dense vector semantic search (optional)
        if request.include_semantic and self._embedder and self._vector_index:
            query_vec = self._embedder.embed_query(request.query)
            semantic_hits = self._pack.semantic_matches(query_vec, top_k=request.limit * 2)
            if semantic_hits:
                ranked_lists.append(semantic_hits)

        # Channel 4: Object title fallback (if no results from above)
        if not ranked_lists:
            fallback_hits = self._pack.object_fallback(request.query, limit=request.limit)
            if fallback_hits:
                ranked_lists.append(fallback_hits)

        # RRF fusion
        if not ranked_lists:
            return SearchToolOutput(results=[])

        fused = self._rrf.fuse(ranked_lists)

        # Graph proximity boost (optional)
        if request.include_graph_boost and fused:
            # Build adjacency from top seeds
            adjacency: dict[str, set[str]] = {}
            seed_ids = [h.object_id for h in fused[:3]]
            for seed_id in seed_ids:
                edges = self._pack.graph_neighbors(seed_id, hops=1, predicates=(), limit=20)
                adjacency[seed_id] = {e.object_id for e in edges}
            fused = self._booster.boost(fused, adjacency)

        # Truncate to limit
        fused = fused[: request.limit]

        # Map to output models
        results = []
        for i, hit in enumerate(fused):
            prov_steps = self._pack.provenance_for_object(hit.object_id)
            results.append(SearchResultModel(
                pack_id=hit.pack_id,
                pack_version=hit.pack_version or self._pack.metadata.pack_version,
                object_id=hit.object_id,
                unit_id=hit.unit_id,
                title=hit.title,
                object_type=hit.object_type,
                domain=hit.domain,
                heading_path=hit.heading_path,
                snippet=hit.snippet or "",
                score=hit.score,
                source_kind=hit.source_kind or "authored",
                channels=[
                    ChannelScoreModel(
                        channel="bm25", rank=i + 1,
                        raw_score=hit.score, contribution=hit.score,
                    )
                ],
                provenance=[
                    ProvenanceStepModel(
                        layer=s.layer, identifier=s.identifier, origin=s.origin,
                        source_path=s.source_path, pack_id=s.pack_id,
                        pack_version=s.pack_version,
                    )
                    for s in prov_steps
                ],
            ))

        return SearchToolOutput(results=results)
