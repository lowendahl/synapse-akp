"""RRF fusion and graph boost scoring logic.

What: Domain scoring classes for hybrid retrieval fusion.
Why: Deterministic, testable scoring isolated from IO.
Contracts: P-FORMULA, P-DEDUP, P-BOOST, P-CHANNEL-INVARIANT, P-MONOTONIC.
Boundaries: Imports only from domain/models.py. No IO, no side effects.
"""

from __future__ import annotations

from dataclasses import replace

from akp_runtime.domain.models import SearchHit


class ReciprocalRankFusion:
    """Fuses multiple ranked lists using the RRF formula.

    Formula: score(hit) = Σ 1/(k + rank) for each channel where hit appears.
    Rank is 1-based. Dedup key is (pack_id, object_id, unit_id).
    Output is stable-sorted by (-score, pack_id, object_id, unit_id).
    """

    def __init__(self, k: int = 60) -> None:
        self._k = k

    @staticmethod
    def _dedup_key(hit: SearchHit) -> tuple[str, str, str | None]:
        """Deduplication identity: (pack_id, object_id, unit_id)."""
        return (hit.pack_id, hit.object_id, hit.unit_id)

    def fuse(self, ranked_lists: list[list[SearchHit]]) -> list[SearchHit]:
        """Fuse multiple ranked lists into a single scored list."""
        if not ranked_lists:
            return []

        scores: dict[tuple[str, str, str | None], float] = {}
        representatives: dict[tuple[str, str, str | None], SearchHit] = {}

        for channel in ranked_lists:
            for rank_0, hit in enumerate(channel):
                key = self._dedup_key(hit)
                rrf_score = 1.0 / (self._k + rank_0 + 1)
                scores[key] = scores.get(key, 0.0) + rrf_score
                if key not in representatives:
                    representatives[key] = hit

        fused = [replace(representatives[key], score=score) for key, score in scores.items()]
        return ResultSorter.stable_sort(fused)


class GraphProximityBooster:
    """Boosts candidates whose source objects are 1-hop neighbors of top results.

    Only the top-N results (by pre-boost score) seed the neighbor set.
    Boost is additive: boosted_score = original_score + boost_value.
    Seeds themselves are NOT boosted.
    """

    def __init__(self, top_n: int = 3, boost_value: float = 0.1) -> None:
        self._top_n = top_n
        self._boost_value = boost_value

    def boost(
        self,
        candidates: list[SearchHit],
        adjacency: dict[str, set[str]],
    ) -> list[SearchHit]:
        """Apply graph proximity boost to candidates."""
        if not candidates or not adjacency:
            return list(candidates)

        sorted_candidates = ResultSorter.stable_sort(candidates)
        seeds = {h.object_id for h in sorted_candidates[: self._top_n]}

        neighbor_set: set[str] = set()
        for seed_id in seeds:
            neighbor_set.update(adjacency.get(seed_id, set()))
        neighbor_set -= seeds

        boosted = []
        for hit in candidates:
            if hit.object_id in neighbor_set:
                boosted.append(replace(hit, score=hit.score + self._boost_value))
            else:
                boosted.append(hit)

        return boosted


class ResultSorter:
    """Deterministic scoring sort for search results."""

    @staticmethod
    def stable_sort(hits: list[SearchHit]) -> list[SearchHit]:
        """Sort by -score, then pack_id, object_id, unit_id for determinism."""
        return sorted(
            hits,
            key=lambda h: (-h.score, h.pack_id, h.object_id, h.unit_id or ""),
        )


# ─── Backward-compatible module-level functions ─────────────────────────────
# These delegate to the class implementations for existing consumers.

_default_rrf = ReciprocalRankFusion()
_default_booster = GraphProximityBooster()


def rrf_fuse(ranked_lists: list[list[SearchHit]], rrf_k: int = 60) -> list[SearchHit]:
    """Backward-compatible wrapper around ReciprocalRankFusion."""
    if rrf_k != 60:
        return ReciprocalRankFusion(k=rrf_k).fuse(ranked_lists)
    return _default_rrf.fuse(ranked_lists)


def apply_graph_boost(
    candidates: list[SearchHit],
    adjacency: dict[str, set[str]],
    top_n: int = 3,
    boost_value: float = 0.1,
) -> list[SearchHit]:
    """Backward-compatible wrapper around GraphProximityBooster."""
    return GraphProximityBooster(top_n=top_n, boost_value=boost_value).boost(candidates, adjacency)


def stable_sort(hits: list[SearchHit]) -> list[SearchHit]:
    """Backward-compatible wrapper around ResultSorter."""
    return ResultSorter.stable_sort(hits)
