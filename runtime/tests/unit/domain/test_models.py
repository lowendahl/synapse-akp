"""Tests for immutable runtime domain models."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, fields
from types import MappingProxyType

import pytest

from akp_runtime.domain.models import PackMetadata, ProvenanceStep
from tests.factories import (
    make_channel_score,
    make_graph_edge_hit,
    make_pack_metadata,
    make_provenance_step,
    make_search_hit,
    make_semantic_unit_record,
)

MAPPING_PROXY_TYPE = type(MappingProxyType({}))
EXPECTED_MANIFEST_KEYS = {
    "pack_id",
    "pack_version",
    "schema_version",
    "ontology_version",
    "compiler_version",
    "build_timestamp",
    "source_file_count",
    "object_count",
    "node_count",
    "edge_count",
    "semantic_unit_count",
    "alias_count",
    "bm25_vocab_size",
    "embedding_model",
    "embedding_dimensions",
    "cross_pack_refs",
    "content_hash",
    "error_count",
    "warning_count",
}


# Invariant: all domain dataclasses are frozen and reject mutation.
@pytest.mark.parametrize(
    ("instance", "attribute", "value"),
    (
        (make_pack_metadata(), "pack_id", "other.pack"),
        (make_semantic_unit_record(), "title", "Other title"),
        (make_channel_score(), "raw_score", 0.1),
        (make_provenance_step(), "identifier", "other.id"),
        (make_search_hit(), "score", 0.1),
        (make_graph_edge_hit(), "predicate", "depends_on"),
    ),
)
def test_domain_models_are_frozen(instance: object, attribute: str, value: object) -> None:
    with pytest.raises(FrozenInstanceError):
        setattr(instance, attribute, value)


# Invariant: provenance metadata is deeply immutable and list values are frozen to tuples.
def test_provenance_metadata_is_deeply_immutable() -> None:
    channels = ["bm25", "semantic"]
    step = ProvenanceStep(
        layer="retrieval",
        identifier="query:test",
        origin="generated",
        metadata={"channels": channels, "score": 0.75},
    )
    channels.append("graph_boost")

    assert isinstance(step.metadata, MAPPING_PROXY_TYPE)
    assert step.metadata["channels"] == ("bm25", "semantic")
    assert step.metadata["score"] == 0.75
    with pytest.raises(TypeError):
        step.metadata["channels"] = ("x",)


# Invariant: PackMetadata mirrors the 19 required manifest keys plus runtime path state.
def test_pack_metadata_contains_all_required_manifest_fields() -> None:
    field_names = {field.name for field in fields(PackMetadata)}

    assert EXPECTED_MANIFEST_KEYS.issubset(field_names)
    assert len(EXPECTED_MANIFEST_KEYS) == 19
    assert field_names == EXPECTED_MANIFEST_KEYS | {"path"}


# Invariant: tuple-valued result fields remain immutable containers.
def test_result_tuple_fields_are_immutable() -> None:
    hit = make_search_hit()
    edge = make_graph_edge_hit()

    assert isinstance(hit.channels, tuple)
    assert isinstance(hit.provenance, tuple)
    assert isinstance(edge.provenance, tuple)
    with pytest.raises(AttributeError):
        hit.channels.append(make_channel_score())
    with pytest.raises(AttributeError):
        hit.provenance.append(make_provenance_step())


# Invariant: domain models use stable value semantics for equality and hashing where supported.
def test_domain_model_equality_and_hashing_work() -> None:
    meta_a = make_pack_metadata()
    meta_b = make_pack_metadata()
    meta_c = make_pack_metadata(pack_id="other.pack")
    hit_a = make_search_hit()
    hit_b = make_search_hit()
    hit_c = make_search_hit(object_id="csu.metric.other")

    assert meta_a == meta_b
    assert hash(meta_a) == hash(meta_b)
    assert meta_a != meta_c
    assert len({meta_a, meta_b, meta_c}) == 2
    assert hit_a == hit_b
    assert hit_a != hit_c


# Invariant: per-instance metadata defaults never leak state across model instances.
def test_domain_model_defaults_do_not_leak_between_instances() -> None:
    first = make_provenance_step(metadata={"channels": ["bm25"]})
    second = make_provenance_step(metadata={"channels": ["semantic"]})
    empty_a = make_provenance_step()
    empty_b = make_provenance_step()

    assert first.metadata["channels"] == ("bm25",)
    assert second.metadata["channels"] == ("semantic",)
    assert dict(empty_a.metadata) == {}
    assert dict(empty_b.metadata) == {}
