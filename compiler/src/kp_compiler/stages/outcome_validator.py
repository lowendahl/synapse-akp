"""Outcome validation stage facade."""

from __future__ import annotations

from pathlib import Path

import duckdb

from kp_compiler.domain.rules import OutcomeAssertion, PackRules
from kp_compiler.stages.assertion_evaluator import OutcomeAssertionEvaluator
from kp_compiler.stages.outcome_validation_models import AssertionResult, OutcomeReport


class OutcomeValidationStage:
    """Runs outcome assertions against a compiled pack."""

    def __init__(self) -> None:
        self._evaluator = OutcomeAssertionEvaluator()

    def run_assertion(self, assertion: OutcomeAssertion, connection: duckdb.DuckDBPyConnection) -> AssertionResult:
        return self._evaluator.run(assertion, connection)

    def validate_outcomes(self, pack_path: Path, rules: PackRules) -> OutcomeReport:
        if not rules.outcome_assertions:
            return OutcomeReport()
        connection = duckdb.connect(str(pack_path), read_only=True)
        results: list[AssertionResult] = []
        try:
            for assertion in rules.outcome_assertions:
                results.append(self.run_assertion(assertion, connection))
        finally:
            connection.close()
        passed_count = sum(1 for result in results if result.passed)
        pass_rate = passed_count / len(results) if results else 1.0
        return OutcomeReport(
            results=results,
            passed=pass_rate >= rules.quality_thresholds.min_assertion_pass_rate,
            pass_rate=pass_rate,
        )


_stage = OutcomeValidationStage()
run_assertion = _stage.run_assertion
validate_outcomes = _stage.validate_outcomes
__all__ = ["AssertionResult", "OutcomeReport", "OutcomeValidationStage", "run_assertion", "validate_outcomes"]
