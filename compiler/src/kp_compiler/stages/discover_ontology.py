"""Ontology Discovery Stage -- infers ontology from corpus frontmatter (ADR-013).

What: Scans OKF source files, extracts types + predicates, emits ontology.yaml.
Why: Corpus is the source of truth; ontology should be derived, then frozen.
Contracts: Receives source file paths. Produces Ontology + optional YAML output.
Boundaries: Read-only scan of frontmatter. No object mutation.
Test strategy: Unit tests with synthetic frontmatter; verify type/predicate extraction.
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class DiscoveredType:
    """An object type discovered from corpus frontmatter."""

    name: str
    description: str = ""
    observed_count: int = 0
    domains: set[str] = field(default_factory=set)
    observed_fields: set[str] = field(default_factory=set)


@dataclass
class DiscoveredPredicate:
    """A relationship predicate discovered from corpus frontmatter."""

    name: str
    description: str = ""
    observed_count: int = 0
    subject_types: set[str] = field(default_factory=set)
    object_types: set[str] = field(default_factory=set)


@dataclass
class OntologyDiscoveryResult:
    """Output of the ontology discovery stage."""

    types: dict[str, DiscoveredType] = field(default_factory=dict)
    predicates: dict[str, DiscoveredPredicate] = field(default_factory=dict)
    domains: set[str] = field(default_factory=set)
    id_prefixes: set[str] = field(default_factory=set)
    source_count: int = 0


def _extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown content."""
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    try:
        from ruamel.yaml import YAML
        yaml = YAML(typ="safe")
        return yaml.load(match.group(1)) or {}
    except Exception:
        return {}


# Map raw frontmatter type strings to canonical ontology type names.
# This mirrors the parser's type_map but returns the ontology key.
_CANONICAL_TYPE: dict[str, str] = {
    "Framework": "Framework",
    "MCEM Stage": "Stage",
    "Stage": "Stage",
    "Methodology": "Methodology",
    "Strategy": "Strategy",
    "Organization": "Organization",
    "Operating Model": "Organization",
    "Role": "Role",
    "Process": "Process",
    "Metric": "Metric",
    "Metric Collection": "Metric",
    "KPI": "KPI",
    "Doctrine": "Doctrine",
    "Program": "Program",
    "Outcome Framework": "Outcome",
    "Outcome": "Outcome",
    "Evidence Source": "Evidence_Source",
    "Evidence Map": "Evidence_Map",
    "Risk Indicator": "Risk",
    "Risk Signal": "Risk",
    "Risk": "Risk",
    "Priority": "Priority",
    "Planning Artifact": "Planning",
    "Planning": "Planning",
    "Taxonomy": "Taxonomy",
    "Pipeline Object": "Pipeline",
    "Pipeline": "Pipeline",
    "Governance": "Governance",
    "GTM": "GTM",
    "Contract": "Contract",
    "Delivery": "Delivery",
    "Measurement": "Measurement",
    "Measurement Concept": "Measurement",
    "ADR": "ADR",
    "Index": "Index",
    "Log": "Log",
}


def _infer_domain(file_path: str) -> str:
    """Infer domain from file path."""
    normalized = file_path.replace("\\", "/")
    if "/mcem/" in normalized or normalized.startswith("mcem/"):
        return "mcem"
    if "/csu/" in normalized or normalized.startswith("csu/"):
        return "csu"
    return "unknown"


def discover_ontology(
    source_files: list[Path],
    source_root: Path,
) -> OntologyDiscoveryResult:
    """Scan source files and discover types, predicates, and domains.

    This performs a lightweight frontmatter-only pass (no full parse)
    to extract structural metadata for ontology generation.
    """
    result = OntologyDiscoveryResult()
    result.source_count = len(source_files)

    for file_path in source_files:
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            continue

        fm = _extract_frontmatter(content)
        if not fm:
            continue

        rel_path = str(file_path.relative_to(source_root.parent)).replace("\\", "/")
        domain = _infer_domain(rel_path)
        result.domains.add(domain)

        # -- Extract object type --
        raw_type = fm.get("type", "")
        if raw_type:
            obj_type = _CANONICAL_TYPE.get(raw_type, raw_type)
            if obj_type not in result.types:
                result.types[obj_type] = DiscoveredType(name=obj_type)
            dt = result.types[obj_type]
            dt.observed_count += 1
            dt.domains.add(domain)
            dt.observed_fields.update(fm.keys())
        else:
            obj_type = ""

        # -- Extract ID prefix --
        obj_id = fm.get("id", "")
        if obj_id and "." in obj_id:
            prefix = obj_id.rsplit(".", 1)[0]
            result.id_prefixes.add(prefix.split(".")[0])

        # -- Extract relationship predicates --
        relationships = fm.get("relationships", [])
        if isinstance(relationships, list):
            for rel in relationships:
                if not isinstance(rel, dict):
                    continue
                predicate = rel.get("predicate", "")
                target_id = rel.get("object_id", "")
                if predicate:
                    if predicate not in result.predicates:
                        result.predicates[predicate] = DiscoveredPredicate(name=predicate)
                    dp = result.predicates[predicate]
                    dp.observed_count += 1
                    if obj_type:
                        dp.subject_types.add(obj_type)
                    # Infer object type from target ID category
                    if target_id and "." in target_id:
                        parts = target_id.split(".")
                        if len(parts) >= 2:
                            dp.object_types.add(parts[1].replace("_", " ").title())

    return result


def generate_ontology_yaml(
    result: OntologyDiscoveryResult,
    existing_ontology: dict | None = None,
) -> str:
    """Generate ontology.yaml content from discovery result.

    If existing_ontology is provided, merges: keeps existing descriptions
    and constraints, adds newly discovered types/predicates.
    """
    lines: list[str] = []
    now = datetime.now(timezone.utc).isoformat()

    lines.append("# Knowledge Pack Ontology -- auto-discovered")
    lines.append(f"# Generated: {now}")
    lines.append("# Review and remove 'auto_generated: true' to freeze.")
    lines.append("")
    lines.append('version: "1.1.0"')
    lines.append(f'generated: "{now}"')
    lines.append("auto_generated: true")
    lines.append("")

    # -- Object Types --
    lines.append("# " + "-" * 61)
    lines.append("# Object Types")
    lines.append("# " + "-" * 61)
    lines.append("")
    lines.append("object_types:")
    lines.append("")

    existing_types = {}
    if existing_ontology:
        existing_types = existing_ontology.get("object_types", {})

    # Merge: existing first, then new
    all_type_names = list(existing_types.keys())
    for name in sorted(result.types.keys()):
        if name not in all_type_names:
            all_type_names.append(name)

    for type_name in all_type_names:
        existing = existing_types.get(type_name, {})
        discovered = result.types.get(type_name)

        # Use existing description if available, else generate
        description = existing.get("description", "")
        if not description and discovered:
            description = f"Auto-discovered type ({discovered.observed_count} instances)"

        # Merge domains
        domains: set[str] = set()
        if existing.get("domains"):
            domains.update(existing["domains"])
        if discovered:
            domains.update(discovered.domains)

        # Use existing required_fields or default
        required_fields = existing.get("required_fields", ["id", "title", "description"])
        optional_fields = existing.get("optional_fields", ["aliases", "tags", "status"])

        lines.append(f"  {type_name}:")
        lines.append(f'    description: "{description}"')
        lines.append(f"    required_fields: [{', '.join(required_fields)}]")
        lines.append(f"    optional_fields: [{', '.join(optional_fields)}]")
        lines.append(f"    domains: [{', '.join(sorted(domains))}]")

        if discovered and type_name not in existing_types:
            lines.append("    # NEW: discovered from corpus")
        elif not discovered and type_name in existing_types:
            lines.append("    # ORPHAN: not found in corpus")

        lines.append("")

    # -- Predicates --
    lines.append("# " + "-" * 61)
    lines.append("# Relationship Predicates")
    lines.append("# " + "-" * 61)
    lines.append("")
    lines.append("predicates:")
    lines.append("")

    existing_predicates = {}
    if existing_ontology:
        existing_predicates = existing_ontology.get("predicates", {})

    all_pred_names = list(existing_predicates.keys())
    for name in sorted(result.predicates.keys()):
        if name not in all_pred_names:
            all_pred_names.append(name)

    for pred_name in all_pred_names:
        existing = existing_predicates.get(pred_name, {})
        discovered = result.predicates.get(pred_name)

        description = existing.get("description", "")
        if not description and discovered:
            description = f"Auto-discovered predicate ({discovered.observed_count} usages)"

        inverse = existing.get("inverse", "")

        lines.append(f"  {pred_name}:")
        lines.append(f'    description: "{description}"')
        if inverse:
            lines.append(f"    inverse: {inverse}")

        # Constraints: merge existing with discovered
        existing_constraints = existing.get("constraints", {})
        subject_types: set[str] = set()
        object_types: set[str] = set()

        if isinstance(existing_constraints, dict):
            subject_types.update(existing_constraints.get("subject_types", []))
            object_types.update(existing_constraints.get("object_types", []))
        if discovered:
            subject_types.update(discovered.subject_types)
            object_types.update(discovered.object_types)

        if subject_types or object_types:
            lines.append("    constraints:")
            if subject_types:
                lines.append(f"      subject_types: [{', '.join(sorted(subject_types))}]")
            if object_types:
                lines.append(f"      object_types: [{', '.join(sorted(object_types))}]")
        else:
            lines.append("    constraints: {}")

        if discovered and pred_name not in existing_predicates:
            lines.append("    # NEW: discovered from corpus")
        elif not discovered and pred_name in existing_predicates:
            lines.append("    # ORPHAN: not found in corpus")

        lines.append("")

    # -- Constraints --
    lines.append("# " + "-" * 61)
    lines.append("# Constraints")
    lines.append("# " + "-" * 61)
    lines.append("")
    lines.append("constraints:")
    lines.append("")

    # Infer ID pattern from observed prefixes
    prefixes = sorted(result.id_prefixes) if result.id_prefixes else ["mcem", "csu"]
    prefix_pattern = "|".join(prefixes)
    lines.append("  id_format:")
    lines.append(f'    pattern: "^({prefix_pattern})\\\\.[a-z_]+\\\\.[a-z0-9-]+$"')
    lines.append('    description: "IDs must be domain.category.slug in lowercase kebab"')
    lines.append("")
    lines.append("  unique_ids:")
    lines.append('    scope: "global"')
    lines.append('    description: "No two objects may share the same ID across packs"')
    lines.append("")

    return "\n".join(lines)
