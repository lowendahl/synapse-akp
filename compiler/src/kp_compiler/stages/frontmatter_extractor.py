"""Frontmatter and markdown extraction helpers for parsing."""

from __future__ import annotations

import re
from typing import Any

from kp_compiler.domain.models import Relationship, Section

# A markdown link to another .md file: absolute (/knowledge/a.md) or relative (../a.md), not a URL.
_MD_LINK = re.compile(r"\[[^\]]+\]\(((?![a-zA-Z][a-zA-Z0-9+.-]*:)[^)\s]+?\.md(?:#[^)\s]*)?)\)")


class FrontmatterExtractor:
    """Extracts YAML frontmatter and markdown structure."""

    def extract(self, content: str) -> tuple[dict[str, Any], str]:
        from ruamel.yaml import YAML

        match = re.match(r"^---\s*\n(.+?)\n---\s*\n?(.*)", content, re.DOTALL)
        if not match:
            return {}, content
        yaml = YAML(typ="safe")
        return yaml.load(match.group(1)) or {}, match.group(2)

    def extract_sections(self, body: str) -> list[Section]:
        sections: list[Section] = []
        heading = ""
        level = 0
        lines: list[str] = []
        line_start = 0
        for index, line in enumerate(body.split("\n"), start=1):
            match = re.match(r"^(#{1,6})\s+(.+)$", line)
            if match:
                if heading or lines:
                    sections.append(self._section(heading, level, lines, line_start))
                heading = match.group(2).strip()
                level = len(match.group(1))
                lines = []
                line_start = index
                continue
            lines.append(line)
        if heading or lines:
            sections.append(self._section(heading, level, lines, line_start))
        return sections

    def extract_relationships(self, body: str, source_id: str) -> list[Relationship]:
        return [
            Relationship(subject_id=source_id, predicate="references", object_id=match.group(1))
            for match in _MD_LINK.finditer(body)
        ]

    def extract_source_references(self, frontmatter: dict[str, Any], source_id: str) -> list[Relationship]:
        """`references` for front-matter `sources` entries that name a markdown record, either as a
        plain path string or as a mapping with a `resource` path."""
        paths = [
            entry.get("resource", "") if isinstance(entry, dict) else entry
            for entry in frontmatter.get("sources") or []
        ]
        return [
            Relationship(subject_id=source_id, predicate="references", object_id=path)
            for path in paths
            if isinstance(path, str) and path.split("#", 1)[0].endswith(".md") and "://" not in path
        ]

    def _section(self, heading: str, level: int, lines: list[str], line_start: int) -> Section:
        return Section(
            heading=heading,
            level=level,
            content="\n".join(lines).strip(),
            source_line=line_start,
        )
