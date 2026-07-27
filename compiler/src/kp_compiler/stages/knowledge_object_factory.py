"""Knowledge object construction for the parser stage."""

from __future__ import annotations

from typing import Any

from kp_compiler.contracts.errors import OntologyViolation
from kp_compiler.domain.models import KnowledgeObject, MetricObject, ObjectType, Provenance, Relationship
from kp_compiler.stages.frontmatter_extractor import FrontmatterExtractor


class KnowledgeObjectFactory:
    """Builds domain objects from parsed frontmatter and markdown."""

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

    def __init__(self, extractor: FrontmatterExtractor | None = None) -> None:
        self._extractor = extractor or FrontmatterExtractor()

    def parse(self, content: str, source_path: str) -> KnowledgeObject:
        frontmatter, body = self._extractor.extract(content)
        obj_type = self.resolve_type(frontmatter.get("type", "")) if frontmatter.get("type") else ObjectType.PROCESS
        common = {
            "id": frontmatter.get("id", ""),
            "type": obj_type,
            "title": frontmatter.get("title", ""),
            "description": frontmatter.get("description", ""),
            "aliases": frontmatter.get("aliases", []) or [],
            "source_aliases": list(frontmatter.get("aliases", []) or []),
            "tags": frontmatter.get("tags", []) or [],
            "domain": self.infer_domain(source_path),
            "status": frontmatter.get("status", "stable"),
            "source_path": source_path,
            "provenance": Provenance(source_file=source_path, stage="parse"),
            "relationships": self._relationships(body, frontmatter, frontmatter.get("id", "")),
            "sections": self._extractor.extract_sections(body),
            "raw_body": body,
        }
        if obj_type in (ObjectType.METRIC, ObjectType.KPI):
            return MetricObject(
                **common,
                formula=frontmatter.get("formula"),
                classification=frontmatter.get("classification"),
                measurement_paradigm=frontmatter.get("measurement_paradigm"),
            )
        return KnowledgeObject(**common)

    def resolve_type(self, type_name: str) -> ObjectType:
        result = self._TYPE_MAP.get(type_name)
        if result is None:
            raise OntologyViolation(
                source_file="",
                object_id="",
                violation=f"Unknown type '{type_name}' — not in type map",
            )
        return result

    def infer_domain(self, source_path: str) -> str:
        normalized = source_path.replace("\\", "/")
        if "/mcem/" in normalized or normalized.startswith("mcem/"):
            return "mcem"
        if "/csu/" in normalized or normalized.startswith("csu/"):
            return "csu"
        return ""

    def _relationships(self, body: str, frontmatter: dict[str, Any], object_id: str) -> list[Relationship]:
        return self._extractor.extract_relationships(body, object_id) + self._frontmatter_relationships(
            frontmatter, object_id
        )

    def _frontmatter_relationships(self, frontmatter: dict[str, Any], object_id: str) -> list[Relationship]:
        relationships: list[Relationship] = []
        for relationship in frontmatter.get("relationships") or []:
            if isinstance(relationship, dict) and "predicate" in relationship:
                target = relationship.get("object") or relationship.get("object_id") or ""
                if target:
                    relationships.append(
                        Relationship(
                            subject_id=object_id,
                            predicate=relationship["predicate"],
                            object_id=target,
                        )
                    )
        return relationships
