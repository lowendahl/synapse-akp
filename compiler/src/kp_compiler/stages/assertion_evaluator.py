"""Built-in outcome assertion evaluators."""

from __future__ import annotations

import random as random_module
from collections.abc import Callable
from typing import Protocol

from kp_compiler.domain.rules import AssertionKind, OutcomeAssertion
from kp_compiler.stages.outcome_validation_models import AssertionResult
from kp_compiler.stages.project.queries import (
    ExistingObjectTitlesQuery,
    ExplicitAliasLookupQuery,
    ObjectCountQuery,
    OrphanAliasQuery,
    TagCoverageQuery,
    TopAliasLookupQuery,
)


class QueryConnection(Protocol):
    """Minimal query interface for outcome assertions."""

    def execute(self, query: str, parameters: list[object] | None = None) -> object: ...


class OutcomeAssertionEvaluator:
    """Evaluates outcome assertions against a DuckDB connection."""

    def __init__(self) -> None:
        self._registry: dict[AssertionKind, Callable] = {
            AssertionKind.ALIAS_OWNER_IN_TOP_K: self._alias_owner_in_top_k,
            AssertionKind.MAX_TAG_COVERAGE: self._max_tag_coverage,
            AssertionKind.TITLE_SELF_RETRIEVAL: self._title_self_retrieval,
            AssertionKind.NO_ORPHAN_ALIASES: self._no_orphan_aliases,
        }

    def run(
        self,
        assertion: OutcomeAssertion,
        connection: QueryConnection,
    ) -> AssertionResult:
        evaluator = self._registry.get(assertion.rule)
        if evaluator is None:
            return AssertionResult(assertion.name, False, f"Unknown assertion rule: {assertion.rule}")
        result = evaluator(connection, assertion.params)
        result.name = assertion.name
        return result

    def _alias_owner_in_top_k(
        self,
        connection: QueryConnection,
        params: dict,
    ) -> AssertionResult:
        limit = params.get("k", 3)
        sample_size = params.get("sample", 20)
        rows = ExplicitAliasLookupQuery().execute(connection)
        if not rows:
            return AssertionResult("alias_owner_in_top_k", True, "No explicit aliases to check.")
        if len(rows) > sample_size:
            rows = random_module.Random(42).sample(rows, sample_size)
        failures = []
        for alias_text, owner_id in rows:
            hits = TopAliasLookupQuery(alias_text, limit).execute(connection)
            if owner_id not in [hit[0] for hit in hits]:
                failures.append(f"'{alias_text}' → owner '{owner_id}' not in top-{limit}")
        return AssertionResult(
            "alias_owner_in_top_k",
            not failures,
            f"{len(rows) - len(failures)}/{len(rows)} aliases found their owner in top-{limit}",
            len(rows),
            failures[:10],
        )

    def _max_tag_coverage(
        self,
        connection: QueryConnection,
        params: dict,
    ) -> AssertionResult:
        threshold = params.get("threshold", 0.3)
        total_row = ObjectCountQuery().execute(connection)
        total_objects = total_row[0] if total_row else 0
        if total_objects == 0:
            return AssertionResult("max_tag_coverage", True, "No objects.")
        rows = TagCoverageQuery().execute(connection)
        failures = []
        for tag, count in rows:
            coverage = count / total_objects
            if coverage > threshold:
                failures.append(
                    f"tag '{tag}' covers {count}/{total_objects} objects ({coverage:.0%} > {threshold:.0%})"
                )
        return AssertionResult(
            "max_tag_coverage",
            not failures,
            f"{len(rows)} tags checked, {len(failures)} over threshold",
            len(rows),
            failures[:10],
        )

    def _title_self_retrieval(
        self,
        connection: QueryConnection,
        params: dict,
    ) -> AssertionResult:
        limit = params.get("k", 5)
        sample_size = params.get("sample", 30)
        rows = ExistingObjectTitlesQuery().execute(connection)
        if not rows:
            return AssertionResult("title_self_retrieval", True, "No objects.")
        if len(rows) > sample_size:
            rows = random_module.Random(42).sample(rows, sample_size)
        failures = []
        for object_id, title in rows:
            hits = TopAliasLookupQuery(title, limit).execute(connection)
            if object_id not in [hit[0] for hit in hits]:
                failures.append(f"'{title}' → '{object_id}' not found via alias lookup")
        return AssertionResult(
            "title_self_retrieval",
            not failures,
            f"{len(rows) - len(failures)}/{len(rows)} titles found themselves via alias",
            len(rows),
            failures[:10],
        )

    def _no_orphan_aliases(
        self,
        connection: QueryConnection,
        _params: dict,
    ) -> AssertionResult:
        rows = OrphanAliasQuery().execute(connection)
        failures = [f"alias '{alias}' → missing object '{canonical_id}'" for alias, canonical_id in rows]
        return AssertionResult("no_orphan_aliases", not rows, f"{len(rows)} orphaned aliases found", 1, failures)
