"""Stages package — pipeline step implementations."""

from kp_compiler.stages.discover_ontology import OntologyDiscoveryStage, discover_ontology, generate_ontology_yaml
from kp_compiler.stages.enrich import (
    CorpusEnricher,
    detect_fuzzy_duplicates,
    enrich_corpus,
    expand_aliases,
    extract_acronyms_from_text,
)
from kp_compiler.stages.outcome_validator import OutcomeValidationStage, run_assertion, validate_outcomes
from kp_compiler.stages.parse import (
    ParseStage,
    determine_object_type,
    extract_relationships,
    extract_sections,
    parse_frontmatter,
    parse_source,
)

__all__ = [
    "CorpusEnricher",
    "OntologyDiscoveryStage",
    "OutcomeValidationStage",
    "ParseStage",
    "detect_fuzzy_duplicates",
    "determine_object_type",
    "discover_ontology",
    "enrich_corpus",
    "expand_aliases",
    "extract_acronyms_from_text",
    "extract_relationships",
    "extract_sections",
    "generate_ontology_yaml",
    "parse_frontmatter",
    "parse_source",
    "run_assertion",
    "validate_outcomes",
]
