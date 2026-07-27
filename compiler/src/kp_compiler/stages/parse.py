"""Parser stage facade."""

from __future__ import annotations

from typing import Any

from kp_compiler.domain.models import KnowledgeObject, ObjectType, Relationship, Section
from kp_compiler.stages.frontmatter_extractor import FrontmatterExtractor
from kp_compiler.stages.knowledge_object_factory import KnowledgeObjectFactory


class ParseStage:
    """Facade around parser helpers for backward compatibility."""

    def __init__(self) -> None:
        self._extractor = FrontmatterExtractor()
        self._factory = KnowledgeObjectFactory(self._extractor)

    def parse_frontmatter(self, content: str) -> tuple[dict[str, Any], str]:
        return self._extractor.extract(content)

    def extract_sections(self, body: str) -> list[Section]:
        return self._extractor.extract_sections(body)

    def extract_relationships(self, body: str, source_id: str) -> list[Relationship]:
        return self._extractor.extract_relationships(body, source_id)

    def determine_object_type(self, type_name: str) -> ObjectType:
        return self._factory.resolve_type(type_name)

    def parse_source(self, content: str, source_path: str) -> KnowledgeObject:
        return self._factory.parse(content, source_path)


_stage = ParseStage()
parse_frontmatter = _stage.parse_frontmatter
extract_sections = _stage.extract_sections
extract_relationships = _stage.extract_relationships
determine_object_type = _stage.determine_object_type
parse_source = _stage.parse_source
