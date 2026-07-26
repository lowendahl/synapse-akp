"""Validator Stage — ontology enforcement and schema validation.

What: Validates KnowledgeObjects against the ontology and emits diagnostics.
Why: Catches violations early; prevents invalid objects from entering the graph.
Contracts: Receives list[KnowledgeObject] + Ontology. Produces list[Diagnostic].
Boundaries: Must NOT modify objects or perform enrichment.
Test strategy: Unit tests with crafted valid/invalid objects.
"""

from __future__ import annotations

from kp_compiler.contracts.protocols import Diagnostic, Severity
from kp_compiler.domain.models import KnowledgeObject, ObjectType
from kp_compiler.domain.ontology import Ontology


def validate_object(obj: KnowledgeObject, ontology: Ontology) -> list[Diagnostic]:
    """Validate a single object against the ontology. Returns diagnostics."""
    diagnostics: list[Diagnostic] = []

    # Skip reserved types (Index, Log) — they have relaxed requirements
    if obj.type in (ObjectType.INDEX, ObjectType.LOG):
        return diagnostics

    # Skip structural index files with no frontmatter at all
    if not obj.id and not obj.title and "index.md" in obj.source_path:
        return diagnostics

    # Check ID format
    if obj.id and not ontology.is_valid_id(obj.id):
        diagnostics.append(Diagnostic(
            severity=Severity.ERROR,
            source_file=obj.source_path,
            message=f"Invalid ID format: '{obj.id}' — expected pattern: {ontology.id_pattern}",
            stage="validate",
            object_id=obj.id,
        ))

    # Check ID is present
    if not obj.id:
        diagnostics.append(Diagnostic(
            severity=Severity.WARNING,
            source_file=obj.source_path,
            message=f"Missing stable ID for object '{obj.title}'",
            stage="validate",
        ))

    # Check type is in ontology
    if not ontology.is_valid_type(obj.type.value):
        diagnostics.append(Diagnostic(
            severity=Severity.ERROR,
            source_file=obj.source_path,
            message=f"Unknown type '{obj.type.value}' — not in ontology",
            stage="validate",
            object_id=obj.id,
        ))

    # Check required fields
    required = ontology.get_required_fields(obj.type.value)
    for field_name in required:
        if field_name == "id" and not obj.id:
            diagnostics.append(Diagnostic(
                severity=Severity.ERROR,
                source_file=obj.source_path,
                message=f"Required field 'id' is missing",
                stage="validate",
                object_id=obj.id or obj.title,
            ))
        elif field_name == "title" and not obj.title:
            diagnostics.append(Diagnostic(
                severity=Severity.ERROR,
                source_file=obj.source_path,
                message=f"Required field 'title' is missing",
                stage="validate",
                object_id=obj.id,
            ))
        elif field_name == "description" and not obj.description:
            diagnostics.append(Diagnostic(
                severity=Severity.WARNING,
                source_file=obj.source_path,
                message=f"Required field 'description' is missing",
                stage="validate",
                object_id=obj.id,
            ))

    # Validate relationship predicates
    for rel in obj.relationships:
        if rel.predicate != "references" and not ontology.is_valid_predicate(rel.predicate):
            diagnostics.append(Diagnostic(
                severity=Severity.ERROR,
                source_file=obj.source_path,
                message=f"Unknown predicate '{rel.predicate}'",
                stage="validate",
                object_id=obj.id,
            ))

    return diagnostics


def validate_corpus(objects: list[KnowledgeObject], ontology: Ontology) -> list[Diagnostic]:
    """Validate all objects and check for corpus-level constraints."""
    all_diagnostics: list[Diagnostic] = []

    # Per-object validation
    for obj in objects:
        all_diagnostics.extend(validate_object(obj, ontology))

    # Duplicate ID detection
    seen_ids: dict[str, str] = {}
    for obj in objects:
        if obj.id:
            if obj.id in seen_ids:
                all_diagnostics.append(Diagnostic(
                    severity=Severity.ERROR,
                    source_file=obj.source_path,
                    message=f"Duplicate ID '{obj.id}' — first seen in {seen_ids[obj.id]}",
                    stage="validate",
                    object_id=obj.id,
                ))
            else:
                seen_ids[obj.id] = obj.source_path

    return all_diagnostics
