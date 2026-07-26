"""RRF fusion and graph boost scoring logic.

What: Pure scoring functions for hybrid retrieval fusion.
Why: Deterministic, testable scoring isolated from IO.
Contracts: P-FORMULA, P-DEDUP, P-BOOST, P-CHANNEL-INVARIANT, P-MONOTONIC.
Boundaries: Imports only from domain/models.py. No IO, no side effects.
"""

from __future__ import annotations

from dataclasses import replace

from akp_runtime.domain.models import SearchHit


def _dedup_key(hit: SearchHit) -> tuple[str, str, str | None]:
    """Deduplication identity: (pack_id, object_id, unit_id)."""
    return (hit.pack_id, hit.object_id, hit.unit_id)


def rrf_fuse(
    ranked_lists: list[list[SearchHit]],
    rrf_k: int = 60,
) -> list[SearchHit]:
    """Fuse multiple ranked lists using Reciprocal Rank Fusion.

    Formula: score(hit) = Σ 1/(rrf_k + rank) for each channel where hit appears.
    Rank is 1-based. Dedup key is (pack_id, object_id, unit_id).
    Output is stable-sorted by (-score, pack_id, object_id, unit_id).
    """
    if not ranked_lists:
        return []

    # Accumulate scores per dedup key
    scores: dict[tuple[str, str, str | None], float] = {}
    representatives: dict[tuple[str, str, str | None], SearchHit] = {}

    for channel in ranked_lists:
        for rank_0, hit in enumerate(channel):
            key = _dedup_key(hit)
            rrf_score = 1.0 / (rrf_k + rank_0 + 1)
            scores[key] = scores.get(key, 0.0) + rrf_score
            if key not in representatives:
                representatives[key] = hit

    # Build output with fused scores
    fused = [replace(representatives[key], score=score) for key, score in scores.items()]

    return stable_sort(fused)


def apply_graph_boost(
    candidates: list[SearchHit],
    adjacency: dict[str, set[str]],
    top_n: int = 3,
    boost_value: float = 0.1,
) -> list[SearchHit]:
    """Boost candidates whose source objects are 1-hop neighbors of top results.

    Only the top-N results (by pre-boost score) seed the neighbor set.
    Boost is additive: boosted_score = original_score + boost_value.
    Seeds themselves are NOT boosted.
    """
    if not candidates or not adjacency:
        return list(candidates)

    # Determine top-N seeds (by score, deterministic)
    sorted_candidates = stable_sort(candidates)
    seeds = {h.object_id for h in sorted_candidates[:top_n]}

    # Collect all 1-hop neighbors of seeds
    neighbor_set: set[str] = set()
    for seed_id in seeds:
        neighbor_set.update(adjacency.get(seed_id, set()))
    # Don't boost the seeds themselves
    neighbor_set -= seeds

    # Apply boost
    boosted = []
    for hit in candidates:
        if hit.object_id in neighbor_set:
            boosted.append(replace(hit, score=hit.score + boost_value))
        else:
            boosted.append(hit)

    return boosted


def stable_sort(hits: list[SearchHit]) -> list[SearchHit]:
    """Deterministic sort: -score, pack_id, object_id, unit_id."""
    return sorted(
        hits,
        key=lambda h: (-h.score, h.pack_id, h.object_id, h.unit_id or ""),
    )
