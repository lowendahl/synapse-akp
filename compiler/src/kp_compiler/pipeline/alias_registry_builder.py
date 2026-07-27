"""Alias registry helpers for the compiler pipeline."""

from __future__ import annotations

from kp_compiler.domain.models import KnowledgeObject


class AliasRegistryBuilder:
    """Builds searchable aliases from knowledge objects."""

    def build(self, objects: list[KnowledgeObject], pack_id: str = "") -> list[tuple[str, str, str]]:
        domain_tag = pack_id.removeprefix("kp-").lower() if pack_id else ""
        aliases: list[tuple[str, str, str]] = []
        for obj in objects:
            if not obj.id:
                continue
            aliases.append((obj.title, obj.id, "title"))
            aliases.extend((alias, obj.id, "explicit") for alias in obj.aliases)
            aliases.extend((tag, obj.id, "tag") for tag in obj.tags if tag.lower() != domain_tag)
        return aliases


_builder = AliasRegistryBuilder()
build_alias_registry = _builder.build
