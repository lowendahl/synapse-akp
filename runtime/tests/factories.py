"""Test factories for AKP Runtime domain models.

Produces valid instances with sensible defaults. All fields overridable.
"""

from pathlib import Path

from akp_runtime.domain.models import (
    ChannelScore,
    GraphEdgeHit,
    PackMetadata,
    ProvenanceStep,
    SearchHit,
    SemanticUnitRecord,
)


def make_pack_metadata(**overrides: object) -> PackMetadata:
    defaults: dict[str, object] = {
        "pack_id": "test.domain.pack",
        "pack_version": "1.0.0",
        "schema_version": "2.0.0",
        "compiler_version": "0.2.0",
        "path": Path(r"C:\packs\test.duckdb"),
        "content_hash": "abc123",
        "ontology_version": "1.0.0",
        "build_timestamp": "2026-01-01T00:00:00Z",
        "source_file_count": 5,
        "object_count": 10,
        "node_count": 10,
        "edge_count": 15,
        "semantic_unit_count": 20,
        "alias_count": 8,
        "bm25_vocab_size": 100,
        "embedding_model": "BAAI/bge-small-en-v1.5",
        "embedding_dimensions": 384,
        "cross_pack_refs": 2,
        "error_count": 0,
        "warning_count": 0,
    }
    defaults.update(overrides)
    return PackMetadata(**defaults)


def make_channel_score(**overrides: object) -> ChannelScore:
    defaults: dict[str, object] = {
        "channel": "bm25",
        "rank": 1,
        "raw_score": 0.85,
        "contribution": 0.016393,
    }
    defaults.update(overrides)
    return ChannelScore(**defaults)


def make_provenance_step(**overrides: object) -> ProvenanceStep:
    defaults: dict[str, object] = {
        "layer": "object",
        "identifier": "csu.metric.c2c",
        "origin": "authored",
        "source_path": "okf/csu/metrics/c2c.md",
        "pack_id": "test.domain.pack",
        "pack_version": "1.0.0",
    }
    defaults.update(overrides)
    return ProvenanceStep(**defaults)


def make_search_hit(**overrides: object) -> SearchHit:
    defaults: dict[str, object] = {
        "pack_id": "test.domain.pack",
        "pack_version": "1.0.0",
        "object_id": "csu.metric.c2c",
        "unit_id": "csu.metric.c2c::definition",
        "title": "Commit to Complete (C2C)",
        "object_type": "metric",
        "domain": "csu",
        "heading_path": "Definition",
        "snippet": "Measures completion rate against committed milestones.",
        "score": 0.85,
        "source_kind": "authored",
        "channels": (make_channel_score(),),
        "provenance": (make_provenance_step(),),
    }
    defaults.update(overrides)
    return SearchHit(**defaults)


def make_graph_edge_hit(**overrides: object) -> GraphEdgeHit:
    defaults: dict[str, object] = {
        "pack_id": "test.domain.pack",
        "subject_id": "csu.metric.c2c",
        "predicate": "measures",
        "object_id": "csu.outcome.delivery-excellence",
        "origin": "authored",
        "confidence": 0.95,
        "neighbor_title": "Delivery Excellence",
        "neighbor_type": "outcome",
        "provenance": (make_provenance_step(),),
    }
    defaults.update(overrides)
    return GraphEdgeHit(**defaults)


def make_semantic_unit_record(**overrides: object) -> SemanticUnitRecord:
    defaults: dict[str, object] = {
        "unit_id": "csu.metric.c2c::definition",
        "source_object_id": "csu.metric.c2c",
        "heading_path": "Definition",
        "content": "Measures completion rate against committed milestones.",
        "context": "CSU delivery metric tracking milestone adherence.",
        "object_type": "metric",
        "domain": "csu",
        "title": "Commit to Complete (C2C)",
        "description": "Tracks delivery milestones.",
        "source_path": "okf/csu/metrics/c2c.md",
        "source_kind": "authored",
    }
    defaults.update(overrides)
    return SemanticUnitRecord(**defaults)
