"""Tests for provenance chain assembly helpers."""

from __future__ import annotations

from types import MappingProxyType

import pytest

from akp_runtime.domain.provenance import (
    embedding_provenance,
    object_provenance,
    package_provenance,
    retrieval_provenance,
    unit_provenance,
)
from tests.factories import make_pack_metadata

MAPPING_PROXY_TYPE = type(MappingProxyType({}))
VALID_ORIGINS = {"authored", "derived", "inferred", "generated"}


def _assert_immutable_metadata(step: object) -> None:
    metadata = step.metadata
    assert isinstance(metadata, MAPPING_PROXY_TYPE)
    with pytest.raises(TypeError):
        metadata["x"] = "y"


# Invariant: package provenance attaches package-layer metadata from the manifest.
def test_package_provenance_contains_pack_metadata() -> None:
    meta = make_pack_metadata(content_hash="deadbeef")

    step = package_provenance(meta)

    assert step.layer == "package"
    assert step.identifier == meta.pack_id
    assert step.pack_id == meta.pack_id
    assert step.pack_version == meta.pack_version
    assert step.metadata["content_hash"] == "deadbeef"
    _assert_immutable_metadata(step)


# Invariant: object provenance carries the authored source path and object identity.
def test_object_provenance_contains_source_path() -> None:
    step = object_provenance(
        object_id="csu.metric.c2c",
        source_path="okf/csu/metrics/c2c.md",
        source_kind="authored",
        pack_id="test.domain.pack",
        pack_version="1.0.0",
    )

    assert step.layer == "object"
    assert step.identifier == "csu.metric.c2c"
    assert step.source_path == "okf/csu/metrics/c2c.md"
    assert step.origin == "authored"
    _assert_immutable_metadata(step)


# Invariant: unit provenance marks semantic-unit lineage explicitly.
def test_unit_provenance_uses_semantic_unit_layer() -> None:
    step = unit_provenance(
        unit_id="csu.metric.c2c::definition",
        source_kind="derived",
        pack_id="test.domain.pack",
    )

    assert step.layer == "semantic_unit"
    assert step.identifier == "csu.metric.c2c::definition"
    assert step.origin == "derived"
    assert step.pack_id == "test.domain.pack"
    _assert_immutable_metadata(step)


# Invariant: embedding provenance records model metadata for semantic retrieval lineage.
def test_embedding_provenance_contains_model_details() -> None:
    step = embedding_provenance(
        unit_id="csu.metric.c2c::definition",
        model_name="BAAI/bge-small-en-v1.5",
        dimensions=384,
        input_hash="abc123",
    )

    assert step.layer == "embedding"
    assert step.origin == "generated"
    assert step.metadata["model_name"] == "BAAI/bge-small-en-v1.5"
    assert step.metadata["dimensions"] == 384
    assert step.metadata["input_hash"] == "abc123"
    _assert_immutable_metadata(step)


# Invariant: retrieval provenance truncates query identifiers to 64 characters.
def test_retrieval_provenance_truncates_query_identifier() -> None:
    query = "x" * 80

    step = retrieval_provenance(query=query, channels_used=["bm25", "semantic"], final_score=0.75)

    assert step.layer == "retrieval"
    assert step.identifier == f"query:{query[:64]}"
    assert step.metadata["channels"] == ("bm25", "semantic")
    assert step.metadata["final_score"] == 0.75
    _assert_immutable_metadata(step)


# Invariant: every emitted provenance step uses a valid origin literal.
def test_provenance_helpers_emit_valid_origin_literals() -> None:
    steps = (
        package_provenance(make_pack_metadata()),
        object_provenance("csu.metric.c2c", "okf/csu/metrics/c2c.md", "authored", "test.domain.pack", "1.0.0"),
        unit_provenance("csu.metric.c2c::definition", "derived", "test.domain.pack"),
        embedding_provenance("csu.metric.c2c::definition", "BAAI/bge-small-en-v1.5", 384, "abc123"),
        retrieval_provenance("delivery", ["bm25"], 0.25),
    )

    assert {step.origin for step in steps}.issubset(VALID_ORIGINS)
