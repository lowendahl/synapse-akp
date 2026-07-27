"""Re-export facade — all domain models available from their canonical locations.

Import from this module for backward compatibility. Canonical sources:
- enumerations.py: ObjectType, Origin, MeasurementParadigm, Classification
- core_models.py: Relationship, Section, Provenance, SemanticUnit
- knowledge_objects.py: KnowledgeObject, MetricObject, EvidenceSourceObject, RoleObject, ProcessObject
"""

from kp_compiler.domain.core_models import Provenance, Relationship, Section, SemanticUnit
from kp_compiler.domain.enumerations import Classification, MeasurementParadigm, ObjectType, Origin
from kp_compiler.domain.knowledge_objects import (
    EvidenceSourceObject,
    KnowledgeObject,
    MetricObject,
    ProcessObject,
    RoleObject,
)


class _DomainModelExports:
    """Marker class preserving class-based module shape for the facade."""


__all__ = [
    "ObjectType",
    "Origin",
    "MeasurementParadigm",
    "Classification",
    "Relationship",
    "Section",
    "Provenance",
    "SemanticUnit",
    "KnowledgeObject",
    "MetricObject",
    "EvidenceSourceObject",
    "RoleObject",
    "ProcessObject",
]
