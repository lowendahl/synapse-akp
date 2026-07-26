"""Unit tests for the graph stage."""
from kp_compiler.domain.models import (
    KnowledgeObject,
    ObjectType,
    Provenance,
    Relationship,
)
from kp_compiler.stages.graph import build_graph


def _make_object(
    obj_id: str,
    title: str = "Test",
    relationships: list[Relationship] | None = None,
) -> KnowledgeObject:
    return KnowledgeObject(
        id=obj_id,
        type=ObjectType.METRIC,
        title=title,
        description="Test",
        domain="csu",
        status="stable",
        source_path=f"csu/{obj_id}.md",
        provenance=Provenance(source_file=f"csu/{obj_id}.md", stage="parse"),
        relationships=relationships or [],
    )


class TestBuildGraph:
    def test_nodes_created_for_objects_with_ids(self) -> None:
        objects = [_make_object("csu.metric.a"), _make_object("csu.metric.b")]
        result = build_graph(objects)
        assert result.metrics["node_count"] == 2

    def test_edges_created_for_relationships(self) -> None:
        rel = Relationship(
            subject_id="csu.metric.a",
            predicate="references",
            object_id="csu.metric.b",
        )
        objects = [
            _make_object("csu.metric.a", relationships=[rel]),
            _make_object("csu.metric.b"),
        ]
        result = build_graph(objects)
        assert result.metrics["edge_count"] == 1
        assert result.edges[0]["subject_id"] == "csu.metric.a"
        assert result.edges[0]["object_id"] == "csu.metric.b"

    def test_orphan_detection(self) -> None:
        objects = [_make_object("csu.metric.lonely")]
        result = build_graph(objects)
        assert result.metrics["orphan_count"] == 1

    def test_objects_without_id_skipped(self) -> None:
        obj = _make_object("")
        result = build_graph([obj])
        assert result.metrics["node_count"] == 0

    def test_pagerank_computed(self) -> None:
        rel = Relationship(
            subject_id="csu.metric.a",
            predicate="references",
            object_id="csu.metric.b",
        )
        objects = [
            _make_object("csu.metric.a", relationships=[rel]),
            _make_object("csu.metric.b"),
        ]
        result = build_graph(objects)
        # b should have higher pagerank (it has an incoming edge)
        a_pr = next(n["pagerank"] for n in result.nodes if n["id"] == "csu.metric.a")
        b_pr = next(n["pagerank"] for n in result.nodes if n["id"] == "csu.metric.b")
        assert b_pr > a_pr
