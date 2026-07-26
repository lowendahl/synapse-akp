"""RRF fusion and graph boost scoring logic.

Pure functions — no IO, no side effects, fully testable.
"""

from __future__ import annotations

from akp_runtime.domain.models import SearchHit


def rrf_fuse(
    ranked_lists: list[list[SearchHit]],
    rrf_k: int = 60,
) -> list[SearchHit]:
    """Fuse multiple ranked lists using Reciprocal Rank Fusion."""
    raise NotImplementedError("PBI #7")


def apply_graph_boost(
    candidates: list[SearchHit],
    adjacency: dict[str, set[str]],
    top_n: int = 3,
    boost_value: float = 0.1,
) -> list[SearchHit]:
    """Boost candidates whose source objects are 1-hop neighbors of top results."""
    raise NotImplementedError("PBI #7")


def stable_sort(hits: list[SearchHit]) -> list[SearchHit]:
    """Deterministic sort: -score, pack_id, object_id, unit_id."""
    return sorted(
        hits,
        key=lambda h: (-h.score, h.pack_id, h.object_id, h.unit_id or ""),
    )
