"""Models for outcome validation reports."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AssertionResult:
    name: str
    passed: bool
    detail: str = ""
    checked: int = 0
    failures: list[str] = field(default_factory=list)


@dataclass
class OutcomeReport:
    results: list[AssertionResult] = field(default_factory=list)
    passed: bool = True
    pass_rate: float = 1.0
