"""Validator Stage — ontology enforcement and schema validation.

What: Validates KnowledgeObjects against the ontology and emits diagnostics.
Why: Catches violations early; prevents invalid objects from entering the graph.
Contracts: Receives list[KnowledgeObject] + Ontology. Produces list[Diagnostic].
Boundaries: Must NOT modify objects or perform enrichment.
"""

from __future__ import annotations

from kp_compiler.contracts.protocols import Diagnostic, Severity
from kp_compiler.domain.models import KnowledgeObject, ObjectType
from kp_compiler.domain.ontology import Ontology


class OntologyValidator:
    """Validates knowledge objects against the ontology schema."""

    def __init__(self, ontology: Ontology) -> None:
        self._ontology = ontology

    def validate_object(self, obj: KnowledgeObject) -> list[Diagnostic]:
        """Validate a single object against the ontology. Returns diagnostics."""
        diagnostics: list[Diagnostic] = []

        if obj.type in (ObjectType.INDEX, ObjectType.LOG):
            return diagnostics

        if not obj.id and not obj.title and "index.md" in obj.source_path:
            return diagnostics

        self._check_id_format(obj, diagnostics)
        self._check_id_present(obj, diagnostics)
        self._check_type_valid(obj, diagnostics)
        self._check_required_fields(obj, diagnostics)
        self._check_predicates(obj, diagnostics)

        return diagnostics

    def validate_corpus(self, objects: list[KnowledgeObject]) -> list[Diagnostic]:
        """Validate all objects and check for corpus-level constraints."""
        all_diagnostics: list[Diagnostic] = []

        for obj in objects:
            all_diagnostics.extend(self.validate_object(obj))

        self._check_duplicate_ids(objects, all_diagnostics)
        return all_diagnostics

    def _check_id_format(self, obj: KnowledgeObject, diagnostics: list[Diagnostic]) -> None:
        if obj.id and not self._ontology.is_valid_id(obj.id):
            diagnostics.append(
                Diagnostic(
                    severity=Severity.ERROR,
                    source_file=obj.source_path,
                    message=f"Invalid ID format: '{obj.id}' — expected pattern: {self._ontology.id_pattern}",
                    stage="validate",
                    object_id=obj.id,
                )
            )

    def _check_id_present(self, obj: KnowledgeObject, diagnostics: list[Diagnostic]) -> None:
        if not obj.id:
            diagnostics.append(
                Diagnostic(
                    severity=Severity.WARNING,
                    source_file=obj.source_path,
                    message=f"Missing stable ID for object '{obj.title}'",
                    stage="validate",
                )
            )

    def _check_type_valid(self, obj: KnowledgeObject, diagnostics: list[Diagnostic]) -> None:
        if not self._ontology.is_valid_type(obj.type.value):
            diagnostics.append(
                Diagnostic(
                    severity=Severity.ERROR,
                    source_file=obj.source_path,
                    message=f"Unknown type '{obj.type.value}' — not in ontology",
                    stage="validate",
                    object_id=obj.id,
                )
            )

    def _check_required_fields(self, obj: KnowledgeObject, diagnostics: list[Diagnostic]) -> None:
        required = self._ontology.get_required_fields(obj.type.value)
        for field_name in required:
            if field_name == "id" and not obj.id:
                diagnostics.append(
                    Diagnostic(
                        severity=Severity.ERROR,
                        source_file=obj.source_path,
                        message="Required field 'id' is missing",
                        stage="validate",
                        object_id=obj.id or obj.title,
                    )
                )
            elif field_name == "title" and not obj.title:
                diagnostics.append(
                    Diagnostic(
                        severity=Severity.ERROR,
                        source_file=obj.source_path,
                        message="Required field 'title' is missing",
                        stage="validate",
                        object_id=obj.id,
                    )
                )
            elif field_name == "description" and not obj.description:
                diagnostics.append(
                    Diagnostic(
                        severity=Severity.WARNING,
                        source_file=obj.source_path,
                        message="Required field 'description' is missing",
                        stage="validate",
                        object_id=obj.id,
                    )
                )

    def _check_predicates(self, obj: KnowledgeObject, diagnostics: list[Diagnostic]) -> None:
        for rel in obj.relationships:
            if rel.predicate != "references" and not self._ontology.is_valid_predicate(rel.predicate):
                diagnostics.append(
                    Diagnostic(
                        severity=Severity.ERROR,
                        source_file=obj.source_path,
                        message=f"Unknown predicate '{rel.predicate}'",
                        stage="validate",
                        object_id=obj.id,
                    )
                )

    def _check_duplicate_ids(
        self,
        objects: list[KnowledgeObject],
        diagnostics: list[Diagnostic],
    ) -> None:
        seen_ids: dict[str, str] = {}
        for obj in objects:
            if obj.id:
                if obj.id in seen_ids:
                    diagnostics.append(
                        Diagnostic(
                            severity=Severity.ERROR,
                            source_file=obj.source_path,
                            message=f"Duplicate ID '{obj.id}' — first seen in {seen_ids[obj.id]}",
                            stage="validate",
                            object_id=obj.id,
                        )
                    )
                else:
                    seen_ids[obj.id] = obj.source_path


# Backward-compatible module-level functions


def validate_object(obj: KnowledgeObject, ontology: Ontology) -> list[Diagnostic]:
    """Validate a single object against the ontology."""
    return OntologyValidator(ontology).validate_object(obj)


def validate_corpus(objects: list[KnowledgeObject], ontology: Ontology) -> list[Diagnostic]:
    """Validate all objects and check for corpus-level constraints."""
    return OntologyValidator(ontology).validate_corpus(objects)
