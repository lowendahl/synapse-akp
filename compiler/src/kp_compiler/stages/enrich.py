"""Enrichment stage facade."""

from __future__ import annotations

from kp_compiler.domain.models import KnowledgeObject
from kp_compiler.domain.rules import AliasRules, PackRules
from kp_compiler.stages.alias_expander import AliasExpander
from kp_compiler.stages.duplicate_detector import FuzzyDuplicateDetector
from kp_compiler.stages.enrichment_models import EnrichmentResult


class CorpusEnricher:
    """Runs deterministic enrichment passes over a corpus."""

    def __init__(self) -> None:
        self._alias_expander = AliasExpander()
        self._duplicate_detector = FuzzyDuplicateDetector()

    def enrich_corpus(
        self,
        objects: list[KnowledgeObject],
        rules: PackRules | None = None,
    ) -> EnrichmentResult:
        enriched: list[KnowledgeObject] = []
        diagnostics = []
        aliases_added = 0
        acronyms_resolved = 0
        alias_rules = rules.alias_rules if rules else None
        for obj in objects:
            if not obj.id:
                enriched.append(obj)
                continue
            new_aliases, count, gate_diagnostics = self._alias_expander.expand_aliases(obj, alias_rules)
            aliases_added += count
            diagnostics.extend(gate_diagnostics)
            acronyms_resolved += sum(1 for alias in new_aliases if alias.upper() == alias and len(alias) <= 6)
            if new_aliases:
                obj.aliases = list(obj.aliases) + new_aliases
            enriched.append(obj)
        diagnostics.extend(self._duplicate_detector.detect(enriched))
        return EnrichmentResult(
            objects=enriched,
            diagnostics=diagnostics,
            aliases_added=aliases_added,
            acronyms_resolved=acronyms_resolved,
        )

    def expand_aliases(
        self,
        obj: KnowledgeObject,
        rules: AliasRules | None = None,
    ) -> tuple[list[str], int, list]:
        return self._alias_expander.expand_aliases(obj, rules)

    def extract_acronyms_from_text(self, text: str) -> list[str]:
        return self._alias_expander.extract_acronyms_from_text(text)

    def detect_fuzzy_duplicates(
        self,
        objects: list[KnowledgeObject],
        threshold: int = 85,
    ) -> list:
        return self._duplicate_detector.detect(objects, threshold)


_enricher = CorpusEnricher()
enrich_corpus = _enricher.enrich_corpus
expand_aliases = _enricher.expand_aliases
extract_acronyms_from_text = _enricher.extract_acronyms_from_text
detect_fuzzy_duplicates = _enricher.detect_fuzzy_duplicates
