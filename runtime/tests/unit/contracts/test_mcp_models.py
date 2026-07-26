"""Tests for MCP boundary models exposed by the runtime."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from hypothesis import given
from hypothesis import strategies as st
from pydantic import BaseModel, ValidationError

from akp_runtime.contracts.mcp_models import (
    ChannelScoreModel,
    ConceptUnitModel,
    ExpandGraphToolInput,
    ExpandGraphToolOutput,
    GetProvenanceToolInput,
    GetProvenanceToolOutput,
    GraphEdgeModel,
    LookupConceptToolInput,
    LookupConceptToolOutput,
    PackBindingModel,
    ProvenanceStepModel,
    RuntimeConfigModel,
    SearchResultModel,
    SearchToolInput,
    SearchToolOutput,
)
from tests.factories import make_graph_edge_hit, make_provenance_step, make_search_hit

NON_EMPTY_TEXT = st.text(min_size=1, max_size=20)
SMALL_TEXT = st.text(max_size=20)


def _json_metadata(metadata: dict[str, object]) -> dict[str, object]:
    return {key: list(value) if isinstance(value, tuple) else value for key, value in metadata.items()}


def channel_score_payload(**overrides: object) -> dict[str, object]:
    channel = make_search_hit().channels[0]
    payload: dict[str, object] = {
        "channel": channel.channel,
        "rank": channel.rank,
        "raw_score": channel.raw_score,
        "contribution": channel.contribution,
    }
    payload.update(overrides)
    return payload


def provenance_step_payload(**overrides: object) -> dict[str, object]:
    step = make_provenance_step(**overrides)
    payload: dict[str, object] = {
        "layer": step.layer,
        "identifier": step.identifier,
        "origin": step.origin,
        "source_path": step.source_path,
        "source_revision": step.source_revision,
        "pack_id": step.pack_id,
        "pack_version": step.pack_version,
        "metadata": _json_metadata(dict(step.metadata)),
    }
    payload.update(overrides)
    return payload


def search_result_payload(**overrides: object) -> dict[str, object]:
    hit = make_search_hit(**overrides)
    payload: dict[str, object] = {
        "pack_id": hit.pack_id,
        "pack_version": hit.pack_version,
        "object_id": hit.object_id,
        "unit_id": hit.unit_id,
        "title": hit.title,
        "object_type": hit.object_type,
        "domain": hit.domain,
        "heading_path": hit.heading_path,
        "snippet": hit.snippet,
        "score": hit.score,
        "source_kind": hit.source_kind,
        "channels": [channel_score_payload()],
        "provenance": [provenance_step_payload()],
    }
    payload.update(overrides)
    return payload


def graph_edge_payload(**overrides: object) -> dict[str, object]:
    edge = make_graph_edge_hit(**overrides)
    payload: dict[str, object] = {
        "pack_id": edge.pack_id,
        "subject_id": edge.subject_id,
        "predicate": edge.predicate,
        "object_id": edge.object_id,
        "origin": edge.origin,
        "confidence": edge.confidence,
        "neighbor_title": edge.neighbor_title,
        "neighbor_type": edge.neighbor_type,
        "provenance": [provenance_step_payload()],
    }
    payload.update(overrides)
    return payload


def _round_trip_model(model: BaseModel) -> BaseModel:
    return type(model)(**model.model_dump(mode="json"))


# Invariant: minimal MCP inputs validate and retain sensible defaults.
@pytest.mark.parametrize(
    ("model_type", "payload"),
    (
        (PackBindingModel, {"pack_id": "test.domain.pack", "path": Path(r"C:\packs\one.duckdb")}),
        (SearchToolInput, {"query": "delivery"}),
        (LookupConceptToolInput, {"identifier": "csu.metric.c2c"}),
        (ExpandGraphToolInput, {"object_id": "csu.metric.c2c"}),
        (GetProvenanceToolInput, {"object_id": "csu.metric.c2c"}),
        (RuntimeConfigModel, {}),
    ),
)
def test_boundary_models_accept_minimal_payloads(model_type: type[BaseModel], payload: dict[str, Any]) -> None:
    model = model_type(**payload)
    assert isinstance(model, model_type)


# Invariant: fully-populated MCP models validate realistic runtime payloads.
def test_boundary_models_accept_fully_populated_payloads() -> None:
    config = RuntimeConfigModel(
        server_name="akp-runtime-prod",
        default_limit=25,
        lexical_k=30,
        semantic_k=15,
        graph_boost_top_n=5,
        graph_boost_value=0.25,
        rrf_k=75,
        max_hops=2,
        embeddings_enabled=False,
        config_path=Path(r"C:\config\runtime.yaml"),
        packs=[PackBindingModel(pack_id="test.domain.pack", path=Path(r"C:\packs\one.duckdb"), required=False)],
    )
    search = SearchToolInput(
        query="delivery excellence",
        pack_ids=["test.domain.pack"],
        limit=5,
        include_semantic=False,
        include_graph_boost=False,
        object_types=["metric"],
        domains=["csu"],
    )
    lookup = LookupConceptToolInput(
        identifier="csu.metric.c2c",
        pack_ids=["test.domain.pack"],
        include_units=False,
        include_neighbors=False,
        neighbor_limit=3,
    )
    expand = ExpandGraphToolInput(
        object_id="csu.metric.c2c",
        pack_ids=["test.domain.pack"],
        hops=2,
        predicates=["measures"],
        limit=7,
    )
    provenance = GetProvenanceToolInput(
        pack_id="test.domain.pack",
        edge_subject_id="csu.metric.c2c",
        edge_predicate="measures",
        edge_object_id="csu.outcome.delivery-excellence",
    )

    assert config.packs[0].required is False
    assert search.include_semantic is False
    assert lookup.neighbor_limit == 3
    assert expand.hops == 2
    assert provenance.edge_predicate == "measures"


# Invariant: MCP contracts reject unknown fields because extra='forbid' is part of the public API.
@pytest.mark.parametrize(
    ("model_type", "payload"),
    (
        (PackBindingModel, {"pack_id": "test.domain.pack", "path": Path(r"C:\packs\one.duckdb"), "extra": True}),
        (SearchToolInput, {"query": "delivery", "extra": True}),
        (LookupConceptToolInput, {"identifier": "csu.metric.c2c", "extra": True}),
        (ExpandGraphToolInput, {"object_id": "csu.metric.c2c", "extra": True}),
        (GetProvenanceToolInput, {"object_id": "csu.metric.c2c", "extra": True}),
        (ChannelScoreModel, {"channel": "bm25", "rank": 1, "raw_score": 1.0, "contribution": 1.0, "extra": True}),
    ),
)
def test_boundary_models_forbid_unknown_fields(model_type: type[BaseModel], payload: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        model_type(**payload)


# Invariant: constrained MCP fields enforce documented boundary values.
@pytest.mark.parametrize(
    ("model_type", "payload"),
    (
        (PackBindingModel, {"pack_id": "", "path": Path(r"C:\packs\one.duckdb")}),
        (SearchToolInput, {"query": "delivery", "limit": 0}),
        (SearchToolInput, {"query": "delivery", "limit": 51}),
        (LookupConceptToolInput, {"identifier": "csu.metric.c2c", "neighbor_limit": 0}),
        (ExpandGraphToolInput, {"object_id": "csu.metric.c2c", "hops": 0}),
        (ExpandGraphToolInput, {"object_id": "csu.metric.c2c", "limit": 101}),
        (RuntimeConfigModel, {"default_limit": 0}),
        (RuntimeConfigModel, {"graph_boost_value": 1.1}),
        (RuntimeConfigModel, {"rrf_k": 201}),
    ),
)
def test_boundary_models_reject_out_of_range_values(
    model_type: type[BaseModel],
    payload: dict[str, Any],
) -> None:
    with pytest.raises(ValidationError):
        model_type(**payload)


# Invariant: runtime config defaults encode sensible retrieval behavior.
def test_runtime_config_defaults_are_sensible() -> None:
    config = RuntimeConfigModel()

    assert config.server_name == "akp-runtime"
    assert config.default_limit == 10
    assert config.lexical_k == 20
    assert config.semantic_k == 20
    assert config.graph_boost_top_n == 3
    assert config.graph_boost_value == 0.1
    assert config.rrf_k == 60
    assert config.max_hops == 3
    assert config.embeddings_enabled is True
    assert config.packs == []


# Invariant: provenance lookup must target exactly one of object, unit, or edge.
def test_get_provenance_accepts_exactly_one_valid_target() -> None:
    object_target = GetProvenanceToolInput(object_id="csu.metric.c2c")
    unit_target = GetProvenanceToolInput(unit_id="csu.metric.c2c::definition")
    edge_target = GetProvenanceToolInput(
        edge_subject_id="csu.metric.c2c",
        edge_predicate="measures",
        edge_object_id="csu.outcome.delivery-excellence",
    )

    assert object_target.object_id == "csu.metric.c2c"
    assert unit_target.unit_id == "csu.metric.c2c::definition"
    assert edge_target.edge_predicate == "measures"


# Invariant: provenance lookup rejects zero targets, multiple targets, and partial edges.
@pytest.mark.parametrize(
    "payload",
    (
        {},
        {"pack_id": "test.domain.pack"},
        {"object_id": "csu.metric.c2c", "unit_id": "csu.metric.c2c::definition"},
        {
            "object_id": "csu.metric.c2c",
            "edge_subject_id": "csu.metric.c2c",
            "edge_predicate": "measures",
            "edge_object_id": "csu.outcome.delivery-excellence",
        },
        {"edge_subject_id": "csu.metric.c2c", "edge_predicate": "measures"},
        {"edge_subject_id": "csu.metric.c2c", "edge_object_id": "csu.outcome.delivery-excellence"},
        {"edge_predicate": "measures", "edge_object_id": "csu.outcome.delivery-excellence"},
    ),
)
def test_get_provenance_rejects_invalid_target_combinations(payload: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        GetProvenanceToolInput(**payload)


# Invariant: MCP JSON payloads round-trip cleanly through model_dump(mode='json').
@pytest.mark.parametrize(
    ("model_type", "payload"),
    (
        (ChannelScoreModel, channel_score_payload()),
        (ProvenanceStepModel, provenance_step_payload()),
        (SearchResultModel, search_result_payload()),
        (SearchToolOutput, {"results": [search_result_payload()]}),
        (
            ConceptUnitModel,
            {
                "unit_id": "csu.metric.c2c::definition",
                "heading_path": "Definition",
                "snippet": "Measures completion rate against committed milestones.",
            },
        ),
        (GraphEdgeModel, graph_edge_payload()),
        (
            LookupConceptToolOutput,
            {
                "pack_id": "test.domain.pack",
                "object_id": "csu.metric.c2c",
                "title": "Commit to Complete (C2C)",
                "object_type": "metric",
                "domain": "csu",
                "description": "Tracks delivery milestones.",
                "source_kind": "authored",
                "units": [
                    {
                        "unit_id": "csu.metric.c2c::definition",
                        "heading_path": "Definition",
                        "snippet": "Measures completion rate against committed milestones.",
                    }
                ],
                "neighbors": [graph_edge_payload()],
                "provenance": [provenance_step_payload()],
            },
        ),
        (
            ExpandGraphToolOutput,
            {
                "seed_object_id": "csu.metric.c2c",
                "hops": 2,
                "edges": [graph_edge_payload()],
            },
        ),
        (
            GetProvenanceToolOutput,
            {
                "target_type": "object",
                "target_id": "csu.metric.c2c",
                "provenance": [provenance_step_payload()],
            },
        ),
    ),
)
def test_output_models_validate_realistic_payloads_and_round_trip(
    model_type: type[BaseModel],
    payload: dict[str, Any],
) -> None:
    model = model_type(**payload)
    restored = model_type(**model.model_dump(mode="json"))

    assert restored == model


# Invariant: valid search inputs survive arbitrary JSON round-trips.
@given(
    query=NON_EMPTY_TEXT,
    pack_ids=st.lists(NON_EMPTY_TEXT, max_size=3),
    limit=st.integers(min_value=1, max_value=50),
    include_semantic=st.booleans(),
    include_graph_boost=st.booleans(),
    object_types=st.lists(SMALL_TEXT, max_size=3),
    domains=st.lists(SMALL_TEXT, max_size=3),
)
def test_search_tool_input_round_trips_via_json(
    query: str,
    pack_ids: list[str],
    limit: int,
    include_semantic: bool,
    include_graph_boost: bool,
    object_types: list[str],
    domains: list[str],
) -> None:
    model = SearchToolInput(
        query=query,
        pack_ids=pack_ids,
        limit=limit,
        include_semantic=include_semantic,
        include_graph_boost=include_graph_boost,
        object_types=object_types,
        domains=domains,
    )

    assert _round_trip_model(model) == model


# Invariant: valid search outputs survive arbitrary JSON round-trips.
@given(
    object_id=NON_EMPTY_TEXT,
    unit_id=st.one_of(st.none(), NON_EMPTY_TEXT),
    score=st.floats(min_value=0.0, max_value=10.0, allow_nan=False, allow_infinity=False),
)
def test_search_result_round_trips_via_json(object_id: str, unit_id: str | None, score: float) -> None:
    payload = search_result_payload(object_id=object_id, unit_id=unit_id, score=score)
    model = SearchResultModel(**payload)

    assert _round_trip_model(model) == model
