"""Pack Rules — declarative quality configuration for the compiler.

What: AliasRules, QualityThresholds, PackRules — the root config model.
Why: Pack authors configure compiler quality constraints via YAML, not code (ADR-014).
Contracts: Loaded once by the orchestrator, passed as a dependency to stages.
Boundaries: Pure domain models — must NOT import infrastructure or perform IO.
"""

from __future__ import annotations

import re

from pydantic import BaseModel, ConfigDict, Field, field_validator

from kp_compiler.domain.assertions import AssertionKind, OutcomeAssertion


class AliasRules(BaseModel):
    """Compile-time alias quality gate configuration."""

    model_config = ConfigDict(frozen=True)

    stopwords: frozenset[str] = Field(
        default_factory=lambda: frozenset(
            {
                "this",
                "the",
                "a",
                "an",
                "it",
                "is",
                "are",
                "was",
                "were",
                "that",
                "with",
                "for",
                "from",
                "into",
                "also",
                "but",
                "not",
                "can",
                "will",
                "has",
                "had",
                "have",
                "been",
                "does",
                "do",
                "each",
                "every",
                "all",
                "any",
                "some",
                "more",
                "most",
                "much",
                "such",
                "than",
                "then",
                "when",
                "how",
                "what",
                "which",
                "who",
                "its",
                "our",
                "you",
                "your",
                "they",
                "them",
                "we",
                "us",
                "be",
                "by",
                "on",
                "at",
                "to",
                "in",
                "of",
                "or",
                "no",
                "so",
                "if",
                "up",
                "out",
                "off",
                "own",
                "too",
                "very",
                "just",
            }
        ),
        description="Aliases matching these tokens are rejected silently.",
    )
    min_length: int = Field(
        default=2,
        ge=1,
        description="Aliases shorter than this are rejected.",
    )
    max_tag_fanout: int = Field(
        default=15,
        ge=1,
        description="A tag alias applied to more than N objects triggers a WARNING.",
    )
    max_explicit_fanout: int = Field(
        default=8,
        ge=1,
        description="An explicit alias on more than N objects triggers a WARNING.",
    )
    blocked_patterns: list[str] = Field(
        default_factory=lambda: [r"^\d+$", r"^[a-z]$"],
        description="Regex patterns — aliases matching any pattern are rejected.",
    )

    @field_validator("blocked_patterns", mode="after")
    @classmethod
    def _compile_patterns(cls, v: list[str]) -> list[str]:
        for p in v:
            try:
                re.compile(p)
            except re.error as exc:
                raise ValueError(f"Invalid blocked pattern: {p}") from exc
        return v

    def is_blocked(self, alias: str) -> tuple[bool, str]:
        """Check if an alias should be rejected. Returns (blocked, reason)."""
        normed = alias.strip().lower()

        if len(normed) < self.min_length:
            return True, f"too short ({len(normed)} < {self.min_length})"

        if normed in self.stopwords:
            return True, f"stopword '{normed}'"

        for pattern in self.blocked_patterns:
            if re.match(pattern, normed):
                return True, f"blocked pattern '{pattern}'"

        return False, ""


class QualityThresholds(BaseModel):
    """Build-level quality thresholds."""

    model_config = ConfigDict(frozen=True)

    min_assertion_pass_rate: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Minimum fraction of assertions that must pass (0.0–1.0).",
    )
    fail_on_error: bool = Field(
        default=True,
        description="If True, the build fails when pass rate is below threshold.",
    )


class PackRules(BaseModel):
    """Root model for pack-rules.yaml — the compiler's declarative config."""

    model_config = ConfigDict(frozen=True)

    version: str = Field(default="1.0", description="Rules schema version.")
    alias_rules: AliasRules = Field(default_factory=AliasRules)
    outcome_assertions: list[OutcomeAssertion] = Field(
        default_factory=lambda: [
            OutcomeAssertion(
                name="explicit-alias-precision",
                rule=AssertionKind.ALIAS_OWNER_IN_TOP_K,
                params={"k": 3, "sample": 20},
                description="Searching an explicit alias returns its owner in top-3.",
            ),
            OutcomeAssertion(
                name="tag-fanout-limit",
                rule=AssertionKind.MAX_TAG_COVERAGE,
                params={"threshold": 0.3},
                description="No single tag aliases more than 30% of objects.",
            ),
            OutcomeAssertion(
                name="bm25-self-retrieval",
                rule=AssertionKind.TITLE_SELF_RETRIEVAL,
                params={"k": 5, "sample": 30},
                description="Object title as query returns itself in BM25 top-5.",
            ),
        ],
    )
    quality_thresholds: QualityThresholds = Field(default_factory=QualityThresholds)

    @classmethod
    def default(cls) -> PackRules:
        """Return a PackRules instance with all defaults populated."""
        return cls()
