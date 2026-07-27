"""Alias expansion strategies for enrichment."""

from __future__ import annotations

import re

from kp_compiler.contracts.protocols import Diagnostic, Severity
from kp_compiler.domain.models import KnowledgeObject
from kp_compiler.domain.rules import AliasRules
from kp_compiler.stages.enrichment_models import KnownAcronymCatalog


class AliasExpander:
    """Generates deterministic alias expansions."""

    def extract_acronyms_from_text(self, text: str) -> list[tuple[str, str]]:
        pattern = re.compile(r"([A-Z][a-zA-Z\s&-]+?)\s*\(([A-Z]{2,6})\)")
        found: list[tuple[str, str]] = []
        for match in pattern.finditer(text):
            full_name = match.group(1).strip()
            if len(full_name) > 3:
                found.append((match.group(2), full_name))
        return found

    def expand_aliases(
        self,
        obj: KnowledgeObject,
        alias_rules: AliasRules | None = None,
    ) -> tuple[list[str], int, list[Diagnostic]]:
        aliases: list[str] = []
        diagnostics: list[Diagnostic] = []
        existing = {alias.lower() for alias in obj.aliases}
        existing.add(obj.title.lower())
        count = 0

        def allow(alias: str, source: str) -> bool:
            if alias_rules is None:
                return True
            blocked, reason = alias_rules.is_blocked(alias)
            if blocked:
                diagnostics.append(
                    Diagnostic(
                        severity=Severity.INFO,
                        source_file="",
                        message=f"Alias '{alias}' rejected ({reason}) on {obj.title} [{source}]",
                        stage="enrich",
                        object_id=obj.id,
                    )
                )
            return not blocked

        for acronym, expansion in KnownAcronymCatalog.VALUES.items():
            # Match acronym only as whole word in title (not substring of another word)
            title_match = bool(re.search(r"\b" + re.escape(acronym) + r"\b", obj.title, re.IGNORECASE))
            if title_match or acronym.lower() in existing:
                for alias, source in ((expansion, "acronym-expansion"), (acronym, "acronym")):
                    if alias.lower() not in existing and allow(alias, source):
                        aliases.append(alias)
                        existing.add(alias.lower())
                        count += 1

        # Body-text acronym mentions are NOT aliases — they represent references
        # to other concepts. These are handled separately as edge discovery.
        return aliases, count, diagnostics
        return aliases, count, diagnostics
