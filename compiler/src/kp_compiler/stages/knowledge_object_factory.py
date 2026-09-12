"""Knowledge object construction for the parser stage."""

from __future__ import annotations

import re
from pathlib import PurePosixPath
from typing import Any

from kp_compiler.contracts.errors import OntologyViolation
from kp_compiler.domain.models import KnowledgeObject, MetricObject, Provenance, Relationship
from kp_compiler.domain.ontology import Ontology
from kp_compiler.stages.frontmatter_extractor import FrontmatterExtractor

_DEFAULT_TYPE = "Process"
_FALLBACK_MEASUREMENT_TYPES = frozenset({"Metric", "KPI"})
_RESERVED_TYPES = {"index.md": "Index", "log.md": "Log"}
_NON_SLUG = re.compile(r"[^a-z0-9]+")


class KnowledgeObjectFactory:
    """Builds domain objects from parsed frontmatter and markdown.

    Object types are resolved and validated against the injected ontology — the
    ontology (not a hardcoded table) is the single source of truth for the type
    vocabulary, so new domains onboard by declaring their types in ontology.yaml.
    """

    def __init__(
        self,
        extractor: FrontmatterExtractor | None = None,
        ontology: Ontology | None = None,
        domain: str = "",
    ) -> None:
        self._extractor = extractor or FrontmatterExtractor()
        self._ontology = ontology
        self._domain = domain

    def parse(self, content: str, source_path: str) -> KnowledgeObject:
        frontmatter, body = self._extractor.extract(content)
        obj_type = self._object_type(frontmatter.get("type", ""), source_path)
        common = {
            "id": frontmatter.get("id") or self._derive_id(source_path),
            "type": obj_type,
            "title": frontmatter.get("title", ""),
            "description": frontmatter.get("description", ""),
            "aliases": frontmatter.get("aliases", []) or [],
            "source_aliases": list(frontmatter.get("aliases", []) or []),
            "tags": frontmatter.get("tags", []) or [],
            "domain": self._domain or self.infer_domain(source_path),
            "status": frontmatter.get("status", "stable"),
            "source_path": source_path,
            "provenance": Provenance(source_file=source_path, stage="parse"),
            "relationships": self._relationships(body, frontmatter, frontmatter.get("id", "")),
            "sections": self._extractor.extract_sections(body),
            "raw_body": body,
        }
        if self._is_measurement(obj_type):
            return MetricObject(
                **common,
                formula=frontmatter.get("formula"),
                classification=frontmatter.get("classification"),
                measurement_paradigm=frontmatter.get("measurement_paradigm"),
            )
        return KnowledgeObject(**common)

    def resolve_type(self, type_name: str) -> str:
        """Resolve a raw frontmatter type to its canonical ontology type.

        Without an ontology (e.g. isolated parsing) the raw name passes through;
        the validate stage remains the ontology-driven gate either way.
        """
        if self._ontology is None:
            return type_name
        canonical = self._ontology.resolve_type(type_name)
        if canonical is None:
            raise OntologyViolation(
                source_file="",
                object_id="",
                violation=f"Unknown type '{type_name}' — not in ontology",
            )
        return canonical

    def _object_type(self, raw_type: str, source_path: str) -> str:
        if raw_type:
            return self.resolve_type(raw_type)
        return _RESERVED_TYPES.get(PurePosixPath(source_path).name, _DEFAULT_TYPE)

    @staticmethod
    def _derive_id(source_path: str) -> str:
        """Path-derived stable id for corpora that omit `id` (OKF identity is
        path-based). Lowercase slug of the relative path without extension."""
        stem = PurePosixPath(source_path.replace("\\", "/")).with_suffix("")
        return _NON_SLUG.sub("-", str(stem).lower()).strip("-")

    def _is_measurement(self, canonical_type: str) -> bool:
        if self._ontology is not None:
            return self._ontology.is_measurement(canonical_type)
        return canonical_type in _FALLBACK_MEASUREMENT_TYPES

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
