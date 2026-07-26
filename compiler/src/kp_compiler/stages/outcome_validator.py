"""Outcome Validator — post-compilation assertion runner (Stage 13).

What: Opens the compiled DuckDB pack and runs declarative outcome assertions
      defined in pack-rules.yaml.
Why: Validates retrieval quality, not just structural correctness (ADR-014).
Contracts: Receives pack path + PackRules. Returns AssertionReport.
Boundaries: Read-only access to the compiled pack. No mutations.
Test strategy: Unit tests with in-memory DuckDB packs and crafted rules.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from pathlib import Path

import duckdb

from kp_compiler.domain.rules import AssertionKind, OutcomeAssertion, PackRules


@dataclass
class AssertionResult:
    """Result of a single outcome assertion."""

    name: str
    passed: bool
    detail: str = ""
    checked: int = 0
    failures: list[str] = field(default_factory=list)


@dataclass
class OutcomeReport:
    """Aggregated outcome validation report."""

    results: list[AssertionResult] = field(default_factory=list)
    passed: bool = True
    pass_rate: float = 1.0


# ── Built-in assertion functions ────────────────────────────────────────────


def _assert_alias_owner_in_top_k(
    con: duckdb.DuckDBPyConnection,
    params: dict,
) -> AssertionResult:
    """Check that explicit aliases return their owner in the top-K alias results."""
    k = params.get("k", 3)
    sample_size = params.get("sample", 20)

    # Get all explicit aliases with their owning object
    rows = con.execute(
        "SELECT alias, canonical_id FROM aliases WHERE alias_type = 'explicit'"
    ).fetchall()

    if not rows:
        return AssertionResult(
            name="alias_owner_in_top_k",
            passed=True,
            detail="No explicit aliases to check.",
        )

    # Sample
    if len(rows) > sample_size:
        rows = random.sample(rows, sample_size)

    failures: list[str] = []
    for alias_text, owner_id in rows:
        # Search aliases for this text
        hits = con.execute(
            "SELECT canonical_id FROM aliases WHERE lower(alias) = lower(?) LIMIT ?",
            [alias_text, k],
        ).fetchall()
        hit_ids = [h[0] for h in hits]
        if owner_id not in hit_ids:
            failures.append(f"'{alias_text}' → owner '{owner_id}' not in top-{k}")

    passed = len(failures) == 0
    return AssertionResult(
        name="alias_owner_in_top_k",
        passed=passed,
        detail=f"{len(rows) - len(failures)}/{len(rows)} aliases found their owner in top-{k}",
        checked=len(rows),
        failures=failures[:10],
    )


def _assert_max_tag_coverage(
    con: duckdb.DuckDBPyConnection,
    params: dict,
) -> AssertionResult:
    """Check that no single tag alias covers more than threshold% of objects."""
    threshold = params.get("threshold", 0.3)

    total_objects = con.execute("SELECT count(*) FROM objects").fetchone()[0]
    if total_objects == 0:
        return AssertionResult(
            name="max_tag_coverage", passed=True, detail="No objects."
        )

    # Count how many distinct objects each tag alias maps to
    tag_counts = con.execute("""
        SELECT alias, count(DISTINCT canonical_id) as cnt
        FROM aliases
        WHERE alias_type = 'tag'
        GROUP BY alias
        ORDER BY cnt DESC
    """).fetchall()

    failures: list[str] = []
    for tag, cnt in tag_counts:
        coverage = cnt / total_objects
        if coverage > threshold:
            failures.append(
                f"tag '{tag}' covers {cnt}/{total_objects} objects ({coverage:.0%} > {threshold:.0%})"
            )

    passed = len(failures) == 0
    return AssertionResult(
        name="max_tag_coverage",
        passed=passed,
        detail=f"{len(tag_counts)} tags checked, {len(failures)} over threshold",
        checked=len(tag_counts),
        failures=failures[:10],
    )


def _assert_title_self_retrieval(
    con: duckdb.DuckDBPyConnection,
    params: dict,
) -> AssertionResult:
    """Check that searching an object's title via alias lookup returns itself."""
    k = params.get("k", 5)
    sample_size = params.get("sample", 30)

    rows = con.execute("SELECT id, title FROM objects WHERE title IS NOT NULL").fetchall()
    if not rows:
        return AssertionResult(
            name="title_self_retrieval", passed=True, detail="No objects."
        )

    if len(rows) > sample_size:
        rows = random.sample(rows, sample_size)

    failures: list[str] = []
    for obj_id, title in rows:
        # Check if the title exists as an alias pointing back to this object
        hits = con.execute(
            "SELECT canonical_id FROM aliases WHERE lower(alias) = lower(?) LIMIT ?",
            [title, k],
        ).fetchall()
        hit_ids = [h[0] for h in hits]
        if obj_id not in hit_ids:
            failures.append(f"'{title}' → '{obj_id}' not found via alias lookup")

    passed = len(failures) == 0
    return AssertionResult(
        name="title_self_retrieval",
        passed=passed,
        detail=f"{len(rows) - len(failures)}/{len(rows)} titles found themselves via alias",
        checked=len(rows),
        failures=failures[:10],
    )


def _assert_no_orphan_aliases(
    con: duckdb.DuckDBPyConnection,
    params: dict,
) -> AssertionResult:
    """Check that all alias canonical_ids reference existing objects."""
    orphans = con.execute("""
        SELECT a.alias, a.canonical_id
        FROM aliases a
        LEFT JOIN objects o ON a.canonical_id = o.id
        WHERE o.id IS NULL
        LIMIT 20
    """).fetchall()

    failures = [f"alias '{a}' → missing object '{cid}'" for a, cid in orphans]
    return AssertionResult(
        name="no_orphan_aliases",
        passed=len(orphans) == 0,
        detail=f"{len(orphans)} orphaned aliases found",
        checked=1,
        failures=failures,
    )


# ── Assertion dispatcher ───────────────────────────────────────────────────

_ASSERTION_REGISTRY: dict[AssertionKind, callable] = {
    AssertionKind.ALIAS_OWNER_IN_TOP_K: _assert_alias_owner_in_top_k,
    AssertionKind.MAX_TAG_COVERAGE: _assert_max_tag_coverage,
    AssertionKind.TITLE_SELF_RETRIEVAL: _assert_title_self_retrieval,
    AssertionKind.NO_ORPHAN_ALIASES: _assert_no_orphan_aliases,
}


def run_assertion(
    assertion: OutcomeAssertion,
    con: duckdb.DuckDBPyConnection,
) -> AssertionResult:
    """Run a single outcome assertion."""
    fn = _ASSERTION_REGISTRY.get(assertion.rule)
    if fn is None:
        return AssertionResult(
            name=assertion.name,
            passed=False,
            detail=f"Unknown assertion rule: {assertion.rule}",
        )
    result = fn(con, assertion.params)
    result.name = assertion.name
    return result


# ── Public API ──────────────────────────────────────────────────────────────


def validate_outcomes(
    pack_path: Path,
    rules: PackRules,
) -> OutcomeReport:
    """Run all outcome assertions against a compiled pack.

    Returns OutcomeReport with per-assertion results and overall pass/fail.
    """
    if not rules.outcome_assertions:
        return OutcomeReport()

    con = duckdb.connect(str(pack_path), read_only=True)
    results: list[AssertionResult] = []

    try:
        for assertion in rules.outcome_assertions:
            result = run_assertion(assertion, con)
            results.append(result)
    finally:
        con.close()

    passed_count = sum(1 for r in results if r.passed)
    total = len(results)
    pass_rate = passed_count / total if total > 0 else 1.0

    threshold = rules.quality_thresholds.min_assertion_pass_rate
    overall_passed = pass_rate >= threshold

    return OutcomeReport(
        results=results,
        passed=overall_passed,
        pass_rate=pass_rate,
    )
