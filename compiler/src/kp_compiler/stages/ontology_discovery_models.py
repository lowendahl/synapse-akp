"""Result models for ontology discovery."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DiscoveredType:
    name: str
    description: str = ""
    observed_count: int = 0
    domains: set[str] = field(default_factory=set)
    observed_fields: set[str] = field(default_factory=set)


@dataclass
class DiscoveredPredicate:
    name: str
    description: str = ""
    observed_count: int = 0
    subject_types: set[str] = field(default_factory=set)
    object_types: set[str] = field(default_factory=set)


@dataclass
class OntologyDiscoveryResult:
    types: dict[str, DiscoveredType] = field(default_factory=dict)
    predicates: dict[str, DiscoveredPredicate] = field(default_factory=dict)
    domains: set[str] = field(default_factory=set)
    id_prefixes: set[str] = field(default_factory=set)
    source_count: int = 0
