"""Enrichment Stage — deterministic NLP enrichment via spaCy + rapidfuzz.

What: Expands aliases, extracts acronyms, detects entities, finds fuzzy duplicates.
Why: Improves retrieval recall by surfacing implicit synonyms and naming variants.
Contracts: Receives list[KnowledgeObject]. Returns enriched copies + diagnostics.
Boundaries: Must NOT modify graph or perform validation. Pure object enrichment.
Test strategy: Unit tests with crafted objects; verify alias/entity expansion.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from rapidfuzz import fuzz

from kp_compiler.contracts.protocols import Diagnostic, Severity
from kp_compiler.domain.models import KnowledgeObject
from kp_compiler.domain.rules import AliasRules, PackRules


@dataclass
class EnrichmentResult:
    """Output of the enrichment stage."""

    objects: list[KnowledgeObject] = field(default_factory=list)
    diagnostics: list[Diagnostic] = field(default_factory=list)
    aliases_added: int = 0
    entities_found: int = 0
    acronyms_resolved: int = 0


# Common CSU/MCEM acronyms that should always be expanded
KNOWN_ACRONYMS: dict[str, str] = {
    "C2C": "Commit to Complete",
    "UDC": "Unified Delivery Coverage",
    "UCR": "Unified Consumed Revenue",
    "NNR": "Net New Revenue",
    "IQC": "In-Quarter Create",
    "ECIF": "Enterprise Customer Investment Fund",
    "CSP": "Customer Success Plan",
    "CSA": "Customer Success Architect",
    "CSAM": "Customer Success Account Manager",
    "MCEM": "Microsoft Customer Engagement Methodology",
    "MACC": "Microsoft Azure Consumption Commitment",
    "ACR": "Azure Consumed Revenue",
    "ATU": "Account Technology Unit",
    "STU": "Specialist Technology Unit",
    "CSU": "Customer Success Unit",
    "DSAT": "Customer Dissatisfaction",
    "MAU": "Monthly Active Users",
    "PAU": "Productive Active Users",
    "PRU": "Productive Recurring User",
    "PCI": "Pipeline Coverage Index",
    "FRA": "Forecast Recommendation",
    "AIRF": "AI Revenue Forecast",
    "QBR": "Quarterly Business Review",
    "CSDR": "Customer Success Delivery Review",
    "ICP": "Integrated Customer Planning",
    "TMM": "Technical Maturity Model",
    "MDM": "Master Data Management",
    "GRM": "Global Resource Management",
    "MSXi": "MSX Insights",
    "CMF": "Cloud Migration Factory",
    "MIRP": "Microsoft Internal Revenue Plan",
    "ESA": "Enterprise Skills Assessment",
    "SES": "Success Enablement Services",
    "UFP": "Unified for Partners",
    "EDE": "Enhanced Delivery Engagements",
    "STA": "Strategic Technical Assessments",
    "OKF": "Open Knowledge Format",
}


def extract_acronyms_from_text(text: str) -> list[tuple[str, str]]:
    """Extract acronym definitions from text patterns like 'Full Name (ACRONYM)'."""
    pattern = re.compile(r"([A-Z][a-zA-Z\s&-]+?)\s*\(([A-Z]{2,6})\)")
    found: list[tuple[str, str]] = []
    for match in pattern.finditer(text):
        full_name = match.group(1).strip()
        acronym = match.group(2)
        if len(full_name) > 3:
            found.append((acronym, full_name))
    return found


def expand_aliases(
    obj: KnowledgeObject,
    alias_rules: AliasRules | None = None,
) -> tuple[list[str], int, list[Diagnostic]]:
    """Generate additional aliases from title, acronyms, and known mappings.

    Returns (new_aliases, count_added, diagnostics).
    """
    new_aliases: list[str] = []
    diagnostics: list[Diagnostic] = []
    existing = {a.lower() for a in obj.aliases}
    existing.add(obj.title.lower())
    count = 0

    def _gate(alias: str, source: str) -> bool:
        """Return True if alias passes the quality gate."""
        if alias_rules is None:
            return True
        blocked, reason = alias_rules.is_blocked(alias)
        if blocked:
            diagnostics.append(Diagnostic(
                severity=Severity.INFO,
                source_file="",
                message=f"Alias '{alias}' rejected ({reason}) on {obj.title} [{source}]",
                stage="enrich",
                object_id=obj.id,
            ))
            return False
        return True

    # Check title for known acronyms
    for acronym, expansion in KNOWN_ACRONYMS.items():
        if acronym.lower() in obj.title.lower() or acronym.lower() in existing:
            if expansion.lower() not in existing and _gate(expansion, "acronym-expansion"):
                new_aliases.append(expansion)
                existing.add(expansion.lower())
                count += 1
            if acronym.lower() not in existing and _gate(acronym, "acronym"):
                new_aliases.append(acronym)
                existing.add(acronym.lower())
                count += 1

    # Extract acronyms defined in the document body
    body_acronyms = extract_acronyms_from_text(obj.raw_body)
    for acronym, expansion in body_acronyms:
        if acronym.lower() not in existing and _gate(acronym, "body-acronym"):
            new_aliases.append(acronym)
            existing.add(acronym.lower())
            count += 1
        if expansion.lower() not in existing and _gate(expansion, "body-expansion"):
            new_aliases.append(expansion)
            existing.add(expansion.lower())
            count += 1

    return new_aliases, count, diagnostics


def detect_fuzzy_duplicates(
    objects: list[KnowledgeObject],
    threshold: int = 85,
) -> list[Diagnostic]:
    """Detect near-duplicate titles using fuzzy string matching."""
    diagnostics: list[Diagnostic] = []
    titles = [(obj.id, obj.title) for obj in objects if obj.id and obj.title]

    for i, (id_a, title_a) in enumerate(titles):
        for id_b, title_b in titles[i + 1 :]:
            if id_a == id_b:
                continue
            score = fuzz.ratio(title_a.lower(), title_b.lower())
            if score >= threshold and title_a.lower() != title_b.lower():
                diagnostics.append(Diagnostic(
                    severity=Severity.WARNING,
                    source_file="",
                    message=f"Fuzzy duplicate ({score}%): '{title_a}' ~ '{title_b}'",
                    stage="enrich",
                    object_id=id_a,
                ))
    return diagnostics


def enrich_corpus(
    objects: list[KnowledgeObject],
    rules: PackRules | None = None,
) -> EnrichmentResult:
    """Run all enrichment passes over the corpus."""
    enriched: list[KnowledgeObject] = []
    diagnostics: list[Diagnostic] = []
    total_aliases = 0
    total_acronyms = 0
    alias_rules = rules.alias_rules if rules else None

    for obj in objects:
        if not obj.id:
            enriched.append(obj)
            continue

        new_aliases, alias_count, gate_diags = expand_aliases(obj, alias_rules)
        total_aliases += alias_count
        diagnostics.extend(gate_diags)

        # Count acronyms resolved
        for alias in new_aliases:
            if alias.upper() == alias and len(alias) <= 6:
                total_acronyms += 1

        # Create enriched copy with expanded aliases
        if new_aliases:
            obj.aliases = list(obj.aliases) + new_aliases

        enriched.append(obj)

    # Fuzzy duplicate detection
    diagnostics.extend(detect_fuzzy_duplicates(enriched))

    return EnrichmentResult(
        objects=enriched,
        diagnostics=diagnostics,
        aliases_added=total_aliases,
        acronyms_resolved=total_acronyms,
    )
