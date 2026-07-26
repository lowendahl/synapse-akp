"""Unit tests for the validator stage."""
from kp_compiler.contracts.protocols import Severity
from kp_compiler.domain.models import KnowledgeObject, ObjectType, Provenance
from kp_compiler.domain.ontology import Ontology
from kp_compiler.stages.validate import validate_corpus, validate_object

# Minimal ontology for testing
MINIMAL_ONTOLOGY_DATA = {
    "version": "1.0.0",
    "id_pattern": r"^[a-z]+\.[a-z]+\.[a-z0-9-]+$",
    "object_types": {
        "Metric": {"description": "A metric", "required_fields": ["id", "title"]},
        "Stage": {"description": "A stage", "required_fields": ["id", "title"]},
        "Process": {"description": "A process", "required_fields": ["id", "title"]},
    },
    "predicates": {
        "references": {"description": "References another object"},
        "depends_on": {"description": "Depends on another object"},
    },
    "constraints": [],
}


def _make_ontology() -> Ontology:
    return Ontology.from_dict(MINIMAL_ONTOLOGY_DATA)


def _make_object(
    obj_id: str = "csu.metric.test",
    title: str = "Test Metric",
    obj_type: ObjectType = ObjectType.METRIC,
) -> KnowledgeObject:
    return KnowledgeObject(
        id=obj_id,
        type=obj_type,
        title=title,
        description="A test object",
        domain="csu",
        status="stable",
        source_path="csu/metrics/test.md",
        provenance=Provenance(source_file="csu/metrics/test.md", stage="parse"),
    )


class TestValidateObject:
    def test_valid_object_no_errors(self) -> None:
        ontology = _make_ontology()
        obj = _make_object()
        diags = validate_object(obj, ontology)
        errors = [d for d in diags if d.severity == Severity.ERROR]
        assert len(errors) == 0

    def test_missing_id_emits_warning(self) -> None:
        ontology = _make_ontology()
        obj = _make_object(obj_id="")
        diags = validate_object(obj, ontology)
        warnings = [d for d in diags if d.severity == Severity.WARNING]
        assert any("Missing stable ID" in d.message for d in warnings)

    def test_invalid_id_format_emits_error(self) -> None:
        ontology = _make_ontology()
        obj = _make_object(obj_id="INVALID ID FORMAT")
        diags = validate_object(obj, ontology)
        errors = [d for d in diags if d.severity == Severity.ERROR]
        assert any("Invalid ID format" in d.message for d in errors)


class TestValidateCorpus:
    def test_duplicate_ids_detected(self) -> None:
        ontology = _make_ontology()
        obj1 = _make_object(obj_id="csu.metric.dup")
        obj2 = _make_object(obj_id="csu.metric.dup")
        obj2.source_path = "csu/metrics/dup2.md"
        diags = validate_corpus([obj1, obj2], ontology)
        errors = [d for d in diags if d.severity == Severity.ERROR]
        assert any("Duplicate ID" in d.message for d in errors)
