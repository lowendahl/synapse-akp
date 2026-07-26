"""Parser Stage — Markdown + YAML → Pydantic Domain Objects.

What: Reads OKF markdown files and produces typed KnowledgeObject instances.
Why: Separates raw file parsing from normalization, validation, and enrichment.
Contracts: Depends on SourceReader (Protocol). Produces list[KnowledgeObject].
Boundaries: Must NOT validate ontology, resolve references, or perform enrichment.
"""

from __future__ import annotations

import re
from typing import Any

from markdown_it import MarkdownIt

from kp_compiler.domain.models import (
    KnowledgeObject,
    MetricObject,
    ObjectType,
    Provenance,
    Relationship,
    Section,
)


class SourceParser:
    """Parses OKF markdown files into typed KnowledgeObject instances."""

    _TYPE_MAP: dict[str, ObjectType] = {
        "Framework": ObjectType.FRAMEWORK,
        "MCEM Stage": ObjectType.STAGE,
        "Stage": ObjectType.STAGE,
        "Methodology": ObjectType.METHODOLOGY,
        "Strategy": ObjectType.STRATEGY,
        "Organization": ObjectType.ORGANIZATION,
        "Operating Model": ObjectType.ORGANIZATION,
        "Role": ObjectType.ROLE,
        "Process": ObjectType.PROCESS,
        "Metric": ObjectType.METRIC,
        "Metric Collection": ObjectType.METRIC,
        "KPI": ObjectType.KPI,
        "Doctrine": ObjectType.DOCTRINE,
        "Program": ObjectType.PROGRAM,
        "Outcome Framework": ObjectType.OUTCOME,
        "Evidence Source": ObjectType.EVIDENCE_SOURCE,
        "Evidence Map": ObjectType.EVIDENCE_MAP,
        "Risk Indicator": ObjectType.RISK,
        "Risk Signal": ObjectType.RISK,
        "Priority": ObjectType.PRIORITY,
        "Planning Artifact": ObjectType.PLANNING,
        "Taxonomy": ObjectType.TAXONOMY,
        "Pipeline Object": ObjectType.PIPELINE,
        "Pipeline Field": ObjectType.PIPELINE,
        "Pipeline Taxonomy": ObjectType.PIPELINE,
        "Governance": ObjectType.GOVERNANCE,
        "Governance Rhythm": ObjectType.GOVERNANCE,
        "GTM Concept": ObjectType.GTM,
        "Contract Model": ObjectType.CONTRACT,
        "Delivery Offering": ObjectType.DELIVERY,
        "Measurement Concept": ObjectType.MEASUREMENT,
        "ADR": ObjectType.ADR,
        "Index": ObjectType.INDEX,
        "Log": ObjectType.LOG,
    }

    def parse(self, content: str, source_path: str) -> KnowledgeObject:
        """Parse a single OKF source file into a KnowledgeObject."""
        frontmatter, body = self._extract_frontmatter(content)

        raw_type = frontmatter.get("type", "")
        obj_type = self._resolve_type(raw_type) if raw_type else ObjectType.PROCESS
        obj_id = frontmatter.get("id", "")
        title = frontmatter.get("title", "")
        description = frontmatter.get("description", "")
        aliases = frontmatter.get("aliases", []) or []
        tags = frontmatter.get("tags", []) or []
        status = frontmatter.get("status", "stable")

        domain = self._infer_domain(source_path)
        sections = self._extract_sections(body)
        relationships = self._extract_relationships(body, obj_id)
        relationships.extend(self._extract_frontmatter_relationships(frontmatter, obj_id))

        provenance = Provenance(source_file=source_path, stage="parse")

        if obj_type in (ObjectType.METRIC, ObjectType.KPI):
            return MetricObject(
                id=obj_id, type=obj_type, title=title, description=description,
                aliases=aliases, tags=tags, domain=domain, status=status,
                source_path=source_path, provenance=provenance,
                relationships=relationships, sections=sections, raw_body=body,
                formula=frontmatter.get("formula"),
                classification=frontmatter.get("classification"),
                measurement_paradigm=frontmatter.get("measurement_paradigm"),
            )

        return KnowledgeObject(
            id=obj_id, type=obj_type, title=title, description=description,
            aliases=aliases, tags=tags, domain=domain, status=status,
            source_path=source_path, provenance=provenance,
            relationships=relationships, sections=sections, raw_body=body,
        )

    def _extract_frontmatter(self, content: str) -> tuple[dict[str, Any], str]:
        from ruamel.yaml import YAML

        match = re.match(r"^---\s*\n(.+?)\n---\s*\n?(.*)", content, re.DOTALL)
        if not match:
            return {}, content

        yaml = YAML(typ="safe")
        frontmatter = yaml.load(match.group(1)) or {}
        body = match.group(2)
        return frontmatter, body

    def _extract_sections(self, body: str) -> list[Section]:
        sections: list[Section] = []
        current_heading = ""
        current_level = 0
        current_lines: list[str] = []
        current_line_start = 0

        for i, line in enumerate(body.split("\n"), start=1):
            heading_match = re.match(r"^(#{1,6})\s+(.+)$", line)
            if heading_match:
                if current_heading or current_lines:
                    sections.append(Section(
                        heading=current_heading, level=current_level,
                        content="\n".join(current_lines).strip(),
                        source_line=current_line_start,
                    ))
                current_heading = heading_match.group(2).strip()
                current_level = len(heading_match.group(1))
                current_lines = []
                current_line_start = i
            else:
                current_lines.append(line)

        if current_heading or current_lines:
            sections.append(Section(
                heading=current_heading, level=current_level,
                content="\n".join(current_lines).strip(),
                source_line=current_line_start,
            ))

        return sections

    def _extract_relationships(self, body: str, source_id: str) -> list[Relationship]:
        relationships: list[Relationship] = []
        link_pattern = re.compile(r"\[([^\]]+)\]\((/[^)]+\.md)\)")

        for match in link_pattern.finditer(body):
            target_path = match.group(2)
            relationships.append(Relationship(
                subject_id=source_id, predicate="references", object_id=target_path,
            ))

        return relationships

    def _extract_frontmatter_relationships(
        self, frontmatter: dict[str, Any], obj_id: str,
    ) -> list[Relationship]:
        relationships: list[Relationship] = []
        fm_rels = frontmatter.get("relationships") or []
        for rel in fm_rels:
            if isinstance(rel, dict) and "predicate" in rel:
                target = rel.get("object") or rel.get("object_id") or ""
                if target:
                    relationships.append(Relationship(
                        subject_id=obj_id, predicate=rel["predicate"], object_id=target,
                    ))
        return relationships

    def _resolve_type(self, type_str: str) -> ObjectType:
        result = self._TYPE_MAP.get(type_str)
        if result is None:
            from kp_compiler.contracts.errors import OntologyViolation
            raise OntologyViolation(
                source_file="", object_id="",
                violation=f"Unknown type '{type_str}' — not in type map",
            )
        return result

    def _infer_domain(self, source_path: str) -> str:
        normalized_path = source_path.replace("\\", "/")
        if "/mcem/" in normalized_path or normalized_path.startswith("mcem/"):
            return "mcem"
        if "/csu/" in normalized_path or normalized_path.startswith("csu/"):
            return "csu"
        return ""


# Backward-compatible module-level functions

_parser = SourceParser()


def parse_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Extract YAML frontmatter and body from markdown content."""
    return _parser._extract_frontmatter(content)


def extract_sections(body: str) -> list[Section]:
    """Extract heading-delimited sections from markdown body."""
    return _parser._extract_sections(body)


def extract_relationships(body: str, source_id: str) -> list[Relationship]:
    """Extract cross-references from markdown links."""
    return _parser._extract_relationships(body, source_id)


def determine_object_type(type_str: str) -> ObjectType:
    """Map frontmatter type string to ObjectType enum."""
    return _parser._resolve_type(type_str)


def parse_source(content: str, source_path: str) -> KnowledgeObject:
    """Parse a single OKF source file into a KnowledgeObject."""
    return _parser.parse(content, source_path)
