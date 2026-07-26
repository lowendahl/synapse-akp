"""Tests for deterministic runtime scoring behavior."""

from __future__ import annotations

import pytest
from hypothesis import given
from hypothesis import strategies as st

from akp_runtime.domain.scoring import apply_graph_boost, rrf_fuse, stable_sort
from tests.factories import make_search_hit


# Invariant: RRF fusion returns an empty list for empty channel input.
@pytest.mark.skip(reason="PBI #7: not yet implemented")
def test_rrf_fuse_returns_empty_list_for_empty_input() -> None:
    assert rrf_fuse([]) == []


# Invariant: RRF uses score = 1 / (k + rank) for a single ranked list.
@pytest.mark.skip(reason="PBI #7: not yet implemented")
def test_rrf_fuse_single_channel_uses_documented_formula() -> None:
    hit = make_search_hit(score=0.0)

    fused = rrf_fuse([[hit]], rrf_k=60)

    assert fused[0].score == pytest.approx(1 / 61)


# Invariant: RRF sums contributions across channels and deduplicates repeated hits.
@pytest.mark.skip(reason="PBI #7: not yet implemented")
def test_rrf_fuse_sums_multi_channel_contributions_for_duplicate_hits() -> None:
    shared = make_search_hit(score=0.0)
    other = make_search_hit(object_id="csu.metric.lead-time", score=0.0)

    fused = rrf_fuse([[shared, other], [shared]], rrf_k=60)

    assert fused[0].score == pytest.approx((1 / 61) + (1 / 61))
    assert fused[1].score == pytest.approx(1 / 62)


# Invariant: graph boost affects only 1-hop neighbors of the top-N result set.
@pytest.mark.skip(reason="PBI #7: not yet implemented")
def test_apply_graph_boost_only_boosts_neighbors() -> None:
    anchor = make_search_hit(object_id="a", score=1.0)
    neighbor = make_search_hit(object_id="b", score=0.5)
    stranger = make_search_hit(object_id="c", score=0.5)

    boosted = apply_graph_boost(
        [anchor, neighbor, stranger],
        adjacency={"a": {"b"}},
        top_n=1,
        boost_value=0.1,
    )

    by_id = {hit.object_id: hit for hit in boosted}
    assert by_id["a"].score == pytest.approx(1.0)
    assert by_id["b"].score == pytest.approx(0.6)
    assert by_id["c"].score == pytest.approx(0.5)


# Invariant: stable_sort uses the documented deterministic sort key.
def test_stable_sort_uses_documented_key() -> None:
    hits = [
        make_search_hit(pack_id="z.pack", object_id="beta", unit_id="b", score=0.4),
        make_search_hit(pack_id="a.pack", object_id="beta", unit_id="a", score=0.9),
        make_search_hit(pack_id="a.pack", object_id="alpha", unit_id="z", score=0.9),
        make_search_hit(pack_id="a.pack", object_id="alpha", unit_id=None, score=0.9),
        make_search_hit(pack_id="a.pack", object_id="alpha", unit_id="a", score=0.9),
    ]

    ordered = stable_sort(hits)

    assert [(hit.score, hit.pack_id, hit.object_id, hit.unit_id) for hit in ordered] == [
        (0.9, "a.pack", "alpha", None),
        (0.9, "a.pack", "alpha", "a"),
        (0.9, "a.pack", "alpha", "z"),
        (0.9, "a.pack", "beta", "a"),
        (0.4, "z.pack", "beta", "b"),
    ]


# Invariant: deterministic sorting is idempotent.
def test_stable_sort_is_idempotent() -> None:
    hits = [
        make_search_hit(pack_id="b.pack", object_id="b", unit_id="u2", score=0.5),
        make_search_hit(pack_id="a.pack", object_id="a", unit_id="u1", score=0.7),
        make_search_hit(pack_id="a.pack", object_id="a", unit_id=None, score=0.7),
    ]

    once = stable_sort(hits)
    twice = stable_sort(once)

    assert twice == once


# Invariant: same hits in any input order must produce the same stable result order.
@given(order=st.permutations((0, 1, 2, 3)))
def test_stable_sort_is_deterministic_across_input_permutations(order: tuple[int, ...]) -> None:
    source_hits = [
        make_search_hit(pack_id="b.pack", object_id="beta", unit_id="u2", score=0.5),
        make_search_hit(pack_id="a.pack", object_id="alpha", unit_id="u1", score=0.7),
        make_search_hit(pack_id="a.pack", object_id="alpha", unit_id=None, score=0.7),
        make_search_hit(pack_id="a.pack", object_id="beta", unit_id="u0", score=0.7),
    ]
    permuted = [source_hits[index] for index in order]

    assert stable_sort(permuted) == stable_sort(source_hits)


# Invariant: channel-order permutation must not change fused scores.
@pytest.mark.skip(reason="PBI #7: not yet implemented")
@given(order=st.permutations((0, 1, 2)))
def test_rrf_fuse_is_invariant_to_channel_order(order: tuple[int, ...]) -> None:
    channels = [
        [make_search_hit(object_id="a", score=0.0)],
        [make_search_hit(object_id="a", score=0.0), make_search_hit(object_id="b", score=0.0)],
        [make_search_hit(object_id="b", score=0.0)],
    ]
    permuted = [channels[index] for index in order]

    assert rrf_fuse(permuted, rrf_k=60) == rrf_fuse(channels, rrf_k=60)


# Invariant: adding a retrieval channel can only increase or preserve a hit score.
@pytest.mark.skip(reason="PBI #7: not yet implemented")
def test_rrf_fuse_never_lowers_score_when_adding_a_channel() -> None:
    shared = make_search_hit(object_id="a", score=0.0)

    baseline = rrf_fuse([[shared]], rrf_k=60)
    expanded = rrf_fuse([[shared], [shared]], rrf_k=60)

    assert expanded[0].score >= baseline[0].score
