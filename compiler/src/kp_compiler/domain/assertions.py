"""Outcome assertion models — declarative quality gates for compiled packs."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AssertionKind(StrEnum):
    """Built-in assertion function identifiers."""

    ALIAS_OWNER_IN_TOP_K = "alias_owner_in_top_k"
    MAX_TAG_COVERAGE = "max_tag_coverage"
    TITLE_SELF_RETRIEVAL = "title_self_retrieval"
    NO_ORPHAN_ALIASES = "no_orphan_aliases"


class OutcomeAssertion(BaseModel):
    """A single declarative outcome assertion."""

    model_config = ConfigDict(frozen=True)

    name: str = Field(
        ...,
        description="Human-readable assertion name (used in reports).",
    )
    rule: AssertionKind = Field(
        ...,
        description="Built-in assertion function to execute.",
    )
    params: dict[str, Any] = Field(
        default_factory=dict,
        description="Parameters forwarded to the assertion function.",
    )
    description: str = Field(
        default="",
        description="Optional human-readable description of what this checks.",
    )
