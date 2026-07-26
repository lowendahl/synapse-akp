"""Tests for cross-pack validation stage (ADR-012)."""

from kp_compiler.domain.models import KnowledgeObject, Relationship
from kp_compiler.stages.cross_pack import validate_cross_pack_refs


def _make_obj(
    obj_id: str,
    relationships: list[Relationship] | None = None,
    aliases: list[str] | None = None,
) -> KnowledgeObject:
    return KnowledgeObject(
        id=obj_id,
        title="Test Object",
        type="Process",
        domain="csu",
        source_path="csu/test.md",
        raw_body="",
        sections=[],
        relationships=list(relationships or []),
        aliases=list(aliases or []),
        properties={},
    )


class TestCrossPackValidation:
    """Verify cross-pack reference detection and validation."""

    def test_no_cross_refs_returns_clean(self) -> None:
        objs = [_make_obj("csu.process.deploy")]
        result = validate_cross_pack_refs(objs)
        assert result.refs_checked == 0
        assert result.refs_broken == 0

    def test_detects_cross_pack_relationship(self) -> None:
        rels = [Relationship(subject_id="csu.process.plan", predicate="implements", object_id="mcem.stage.envision")]
        objs = [_make_obj("csu.process.plan", relationships=rels)]
        result = validate_cross_pack_refs(objs, pack_id="kp-csu")
        assert result.refs_checked == 1
        assert len(result.cross_refs) == 1
        assert result.cross_refs[0][1] == "mcem.stage.envision"

    def test_detects_cross_pack_alias(self) -> None:
        """Aliases are no longer checked by cross-pack validator (only relationships)."""
        objs = [_make_obj("csu.process.plan", aliases=["mcem.stage.envision"])]
        result = validate_cross_pack_refs(objs, pack_id="kp-csu")
        assert result.refs_checked == 0  # aliases are not cross-pack refs

    def test_non_cross_refs_ignored(self) -> None:
        rels = [Relationship(subject_id="csu.process.plan", predicate="contains", object_id="csu.metric.udc")]
        objs = [_make_obj("csu.process.plan", relationships=rels)]
        result = validate_cross_pack_refs(objs, pack_id="kp-csu")
        assert result.refs_checked == 0

    def test_file_path_refs_ignored(self) -> None:
        """Markdown link paths like /mcem/stages/1-listen.md should be skipped."""
        rels = [Relationship(subject_id="csu.process.plan", predicate="references", object_id="/mcem/stages/1-listen.md")]
        objs = [_make_obj("csu.process.plan", relationships=rels)]
        result = validate_cross_pack_refs(objs, pack_id="kp-csu")
        assert result.refs_checked == 0

    def test_objects_without_id_skipped(self) -> None:
        objs = [_make_obj("")]
        result = validate_cross_pack_refs(objs)
        assert result.refs_checked == 0
