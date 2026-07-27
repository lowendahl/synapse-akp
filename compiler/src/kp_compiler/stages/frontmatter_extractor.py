"""Frontmatter and markdown extraction helpers for parsing."""

from __future__ import annotations

import re
from typing import Any

from kp_compiler.domain.models import Relationship, Section


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
        pattern = re.compile(r"\[([^\]]+)\]\((/[^)]+\.md)\)")
        return [
            Relationship(subject_id=source_id, predicate="references", object_id=match.group(2))
            for match in pattern.finditer(body)
        ]

    def _section(self, heading: str, level: int, lines: list[str], line_start: int) -> Section:
        return Section(
            heading=heading,
            level=level,
            content="\n".join(lines).strip(),
            source_line=line_start,
        )
