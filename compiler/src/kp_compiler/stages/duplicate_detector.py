"""Fuzzy duplicate detection for enrichment."""

from __future__ import annotations

from rapidfuzz import fuzz

from kp_compiler.contracts.protocols import Diagnostic, Severity
from kp_compiler.domain.models import KnowledgeObject


class FuzzyDuplicateDetector:
    """Detects near-duplicate titles in a corpus."""

    def detect(self, objects: list[KnowledgeObject], threshold: int = 85) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []
        titles = [(obj.id, obj.title) for obj in objects if obj.id and obj.title]
        for index, (left_id, left_title) in enumerate(titles):
            for right_id, right_title in titles[index + 1 :]:
                if left_id == right_id:
                    continue
                score = fuzz.ratio(left_title.lower(), right_title.lower())
                if score >= threshold and left_title.lower() != right_title.lower():
                    diagnostics.append(
                        Diagnostic(
                            severity=Severity.WARNING,
                            source_file="",
                            message=f"Fuzzy duplicate ({score}%): '{left_title}' ~ '{right_title}'",
                            stage="enrich",
                            object_id=left_id,
                        )
                    )
        return diagnostics
