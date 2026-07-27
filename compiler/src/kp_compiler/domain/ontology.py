"""Ontology loading and enforcement.

What: Loads ontology.yaml and provides validation methods.
Why: Single source of truth for allowed types, predicates, and constraints (ADR-002).
Contracts: Pure domain logic — no IO (loading is done by caller).
Boundaries: Must NOT read files directly — receives parsed YAML dict.
Test strategy: Unit tests with inline ontology dicts.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass(frozen=True)
class PredicateSpec:
    """Definition of an allowed relationship predicate."""

    name: str
    description: str = ""
    inverse: str = ""
    subject_types: list[str] = field(default_factory=list)
    object_types: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ObjectTypeSpec:
    """Definition of an allowed object type."""

    name: str
    description: str = ""
    required_fields: list[str] = field(default_factory=list)
    optional_fields: list[str] = field(default_factory=list)
    domains: list[str] = field(default_factory=list)
    resolution_role: str = "neutral"


@dataclass
class Ontology:
    """Loaded ontology providing validation methods."""

    version: str
    object_types: dict[str, ObjectTypeSpec] = field(default_factory=dict)
    predicates: dict[str, PredicateSpec] = field(default_factory=dict)
    id_pattern: str = r"^(mcem|csu)\.[a-z_]+\.[a-z0-9-]+$"

    @classmethod
    def from_dict(cls, data: dict) -> Ontology:
        """Construct Ontology from parsed YAML dict."""
        obj_types: dict[str, ObjectTypeSpec] = {}
        for name, spec in (data.get("object_types") or {}).items():
            obj_types[name] = ObjectTypeSpec(
                name=name,
                description=spec.get("description", ""),
                required_fields=spec.get("required_fields", []),
                optional_fields=spec.get("optional_fields", []),
                domains=spec.get("domains", []),
                resolution_role=spec.get("resolution_role", "neutral"),
            )

        predicates: dict[str, PredicateSpec] = {}
        for name, spec in (data.get("predicates") or {}).items():
            constraints = spec.get("constraints", {})
            predicates[name] = PredicateSpec(
                name=name,
                description=spec.get("description", ""),
                inverse=spec.get("inverse", ""),
                subject_types=constraints.get("subject_types", []),
                object_types=constraints.get("object_types", []),
            )

        constraints_data = data.get("constraints", {})
        if isinstance(constraints_data, list):
            constraints_data = {}
        id_format = constraints_data.get("id_format", {})
        if isinstance(id_format, dict):
            id_pattern = id_format.get("pattern", cls.id_pattern)
        else:
            id_pattern = data.get("id_pattern", cls.id_pattern)

        return cls(
            version=data.get("version", "0.0.0"),
            object_types=obj_types,
            predicates=predicates,
            id_pattern=id_pattern,
        )

    def is_valid_type(self, type_name: str) -> bool:
        """Check if a type name is in the ontology."""
        # Normalize: "Evidence Source" -> check against keys
        return type_name in self.object_types or type_name.replace(" ", "_") in self.object_types

    def is_valid_predicate(self, predicate: str) -> bool:
        """Check if a predicate is in the ontology (including inverses)."""
        if predicate in self.predicates:
            return True
        return any(spec.inverse == predicate for spec in self.predicates.values())

    def merge_discovered_predicates(self, discovered_predicates: dict[str, object]) -> int:
        """Merge corpus-discovered predicates into the ontology.

        Returns the count of newly added predicates.
        """
        added = 0
        for name in discovered_predicates:
            if not self.is_valid_predicate(name):
                self.predicates[name] = PredicateSpec(name=name, description="Auto-discovered from corpus")
                added += 1
        return added

    def is_valid_id(self, id_value: str) -> bool:
        """Check if an ID matches the required format."""
        return bool(re.match(self.id_pattern, id_value))

    def get_required_fields(self, type_name: str) -> list[str]:
        """Get required fields for a given type."""
        key = type_name.replace(" ", "_")
        spec = self.object_types.get(type_name) or self.object_types.get(key)
        if spec:
            return spec.required_fields
        return []

    def get_resolution_role(self, type_name: str) -> str:
        """Get the resolution role for a given type (concept/measurement/evidence/neutral)."""
        key = type_name.replace(" ", "_")
        spec = self.object_types.get(type_name) or self.object_types.get(key)
        if spec:
            return spec.resolution_role
        return "neutral"
