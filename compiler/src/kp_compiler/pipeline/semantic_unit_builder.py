"""Semantic unit creation helpers for the compiler pipeline."""

from __future__ import annotations

from kp_compiler.domain.models import KnowledgeObject, SemanticUnit


class SemanticUnitBuilder:
    """Builds semantic retrieval units from knowledge objects."""

    def build(self, objects: list[KnowledgeObject]) -> list[SemanticUnit]:
        units: list[SemanticUnit] = []
        for obj in objects:
            if not obj.id:
                continue
            units.extend(self._section_units(obj))
            if obj.description:
                units.append(self._definition_unit(obj))
        return units

    def _section_units(self, obj: KnowledgeObject) -> list[SemanticUnit]:
        units: list[SemanticUnit] = []
        for index, section in enumerate(obj.sections):
            if section.content.strip():
                units.append(
                    SemanticUnit(
                        id=f"su:{obj.id}:{index}",
                        source_object_id=obj.id,
                        heading_path=section.heading,
                        content=section.content,
                        context=self._context(obj, section.heading),
                        object_type=obj.type.value,
                        domain=obj.domain,
                    )
                )
        return units

    def _definition_unit(self, obj: KnowledgeObject) -> SemanticUnit:
        return SemanticUnit(
            id=f"su:{obj.id}:def",
            source_object_id=obj.id,
            heading_path="Definition",
            content=f"{obj.title}: {obj.description}",
            context=self._context(obj, "Definition"),
            object_type=obj.type.value,
            domain=obj.domain,
        )

    def _context(self, obj: KnowledgeObject, heading: str) -> str:
        context = f"Domain: {obj.domain}\nType: {obj.type.value}\nDocument: {obj.title}\nSection: {heading}\n"
        return context + (f"Aliases: {', '.join(obj.aliases)}\n" if obj.aliases else "")


_builder = SemanticUnitBuilder()
build_semantic_units = _builder.build
