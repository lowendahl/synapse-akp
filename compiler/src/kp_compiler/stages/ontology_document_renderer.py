"""Renders ontology discovery results to ontology.yaml text."""

from __future__ import annotations

from datetime import UTC, datetime

from kp_compiler.stages.ontology_discovery_models import OntologyDiscoveryResult


class OntologyDocumentRenderer:
    """Builds ontology.yaml content from discovered metadata."""

    def render(self, result: OntologyDiscoveryResult, existing_ontology: dict | None = None) -> str:
        lines: list[str] = []
        timestamp = datetime.now(UTC).isoformat()
        self._header(lines, timestamp)
        self._render_types(lines, result, existing_ontology or {})
        self._render_predicates(lines, result, existing_ontology or {})
        self._render_constraints(lines, result)
        return "\n".join(lines)

    def _header(self, lines: list[str], timestamp: str) -> None:
        lines.extend(
            [
                "# Knowledge Pack Ontology -- auto-discovered",
                f"# Generated: {timestamp}",
                "# Review and remove 'auto_generated: true' to freeze.",
                "",
                'version: "1.1.0"',
                f'generated: "{timestamp}"',
                "auto_generated: true",
                "",
            ]
        )

    def _render_types(self, lines: list[str], result: OntologyDiscoveryResult, existing_ontology: dict) -> None:
        lines.extend(
            [
                "# -------------------------------------------------------------",
                "# Object Types",
                "# -------------------------------------------------------------",
                "",
                "object_types:",
                "",
            ]
        )
        existing_types = existing_ontology.get("object_types", {})
        names = list(existing_types.keys())
        names.extend(name for name in sorted(result.types) if name not in names)
        for type_name in names:
            existing = existing_types.get(type_name, {})
            discovered = result.types.get(type_name)
            description = existing.get("description") or self._describe_type(discovered)
            domains = sorted(set(existing.get("domains", [])) | (discovered.domains if discovered else set()))
            required_fields = existing.get("required_fields", ["id", "title", "description"])
            optional_fields = existing.get("optional_fields", ["aliases", "tags", "status"])
            lines.extend(
                [
                    f"  {type_name}:",
                    f'    description: "{description}"',
                    f"    required_fields: [{', '.join(required_fields)}]",
                    f"    optional_fields: [{', '.join(optional_fields)}]",
                    f"    domains: [{', '.join(domains)}]",
                ]
            )
            if discovered and type_name not in existing_types:
                lines.append("    # NEW: discovered from corpus")
            elif not discovered and type_name in existing_types:
                lines.append("    # ORPHAN: not found in corpus")
            lines.append("")

    def _render_predicates(self, lines: list[str], result: OntologyDiscoveryResult, existing_ontology: dict) -> None:
        lines.extend(
            [
                "# -------------------------------------------------------------",
                "# Relationship Predicates",
                "# -------------------------------------------------------------",
                "",
                "predicates:",
                "",
            ]
        )
        existing_predicates = existing_ontology.get("predicates", {})
        names = list(existing_predicates.keys())
        names.extend(name for name in sorted(result.predicates) if name not in names)
        for predicate_name in names:
            existing = existing_predicates.get(predicate_name, {})
            discovered = result.predicates.get(predicate_name)
            description = existing.get("description") or self._describe_predicate(discovered)
            inverse = existing.get("inverse", "")
            subject_types = set(existing.get("constraints", {}).get("subject_types", []))
            object_types = set(existing.get("constraints", {}).get("object_types", []))
            if discovered:
                subject_types.update(discovered.subject_types)
                object_types.update(discovered.object_types)
            lines.extend([f"  {predicate_name}:", f'    description: "{description}"'])
            if inverse:
                lines.append(f"    inverse: {inverse}")
            if subject_types or object_types:
                lines.append("    constraints:")
                if subject_types:
                    lines.append(f"      subject_types: [{', '.join(sorted(subject_types))}]")
                if object_types:
                    lines.append(f"      object_types: [{', '.join(sorted(object_types))}]")
            else:
                lines.append("    constraints: {}")
            if discovered and predicate_name not in existing_predicates:
                lines.append("    # NEW: discovered from corpus")
            elif not discovered and predicate_name in existing_predicates:
                lines.append("    # ORPHAN: not found in corpus")
            lines.append("")

    def _render_constraints(self, lines: list[str], result: OntologyDiscoveryResult) -> None:
        prefixes = sorted(result.id_prefixes) if result.id_prefixes else ["mcem", "csu"]
        pattern = "|".join(prefixes)
        lines.extend(
            [
                "# -------------------------------------------------------------",
                "# Constraints",
                "# -------------------------------------------------------------",
                "",
                "constraints:",
                "",
                "  id_format:",
                f'    pattern: "^({pattern})\\\\.[a-z_]+\\\\.[a-z0-9-]+$"',
                '    description: "IDs must be domain.category.slug in lowercase kebab"',
                "",
                "  unique_ids:",
                '    scope: "global"',
                '    description: "No two objects may share the same ID across packs"',
                "",
            ]
        )

    def _describe_type(self, discovered: object | None) -> str:
        return f"Auto-discovered type ({discovered.observed_count} instances)" if discovered else ""

    def _describe_predicate(self, discovered: object | None) -> str:
        return f"Auto-discovered predicate ({discovered.observed_count} usages)" if discovered else ""
