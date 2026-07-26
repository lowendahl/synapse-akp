# Code Design Gates

## Purpose

Automated enforcement of architectural quality. These gates run as part of the
test suite and CI pipeline. They prevent drift back into god objects, loose
function files, embedded SQL, and other violations identified in code review.

---

## Gate 1: Module Size (max 200 LoC of logic)

No single `.py` file may exceed 200 lines of non-blank, non-comment, non-docstring
code. Files exceeding this are god objects or mixing concerns.

**Measured**: Lines containing executable Python statements.
**Excluded**: `__init__.py`, test files, generated code.

---

## Gate 2: No Loose-Function Modules

Every `.py` file in `src/` (excluding `__init__.py`, `__main__.py`) MUST define
at least one class. Pure function files indicate missing DDD design.

**Exception**: Type alias files, re-export modules.
**Rationale**: Functions belong to a class that owns the responsibility.

---

## Gate 3: SQL Confinement

SQL strings (containing SELECT, INSERT, CREATE, ALTER, DROP, UPDATE, DELETE)
MUST only appear in files within a `queries/` or `persistence/` directory,
or in files whose name contains `query`, `writer`, or `migration`.

**Rationale**: SQL scattered across the codebase makes refactoring impossible
and violates single responsibility.

---

## Gate 4: No Abbreviations in Public API

All public identifiers (classes, functions, methods not prefixed with `_`)
MUST use full English words. Single-letter variables are only allowed in
comprehensions and lambdas.

**Violations**: `_ENV_PREFIX`, `_BOOL_TRUTHY`, `cfg`, `con`, `params`, `impl`
**Correct**: `ENVIRONMENT_VARIABLE_PREFIX`, `TRUTHY_VALUES`, `configuration`,
`connection`, `parameters`, `implementation`

**Excluded**: Well-established acronyms in our domain: `RRF`, `BM25`, `MCP`,
`DDD`, `BFS`, `SQL`, `ID`, `URL`, `API`.

---

## Gate 5: Event Contract Separation

Event type definitions (dataclasses/models representing events) MUST reside
in `contracts/` (they ARE the contract between publisher and subscriber).

Event bus implementations MUST reside in `infrastructure/` or `events/`.

A single file MUST NOT contain both event definitions and bus implementation.

---

## Gate 6: Query Object Pattern

Every database query MUST be encapsulated in a class that implements the
`PackQuery` protocol (or equivalent). The query class:
- Holds its parameters as constructor arguments
- Exposes an `execute(connection)` method
- Contains the SQL string as a class-level constant
- Returns typed domain objects

No ad-hoc SQL execution through raw connection objects outside query classes.

---

## Gate 7: One Concept Per Domain File

Files in `domain/` MUST contain models for a SINGLE bounded concept.
A file named `models.py` with 5+ unrelated dataclasses is a violation.

**Correct**: `search_hit.py`, `graph_edge.py`, `provenance_step.py`
**Violation**: `models.py` with SearchHit + GraphEdgeHit + ProvenanceStep + PackMetadata

---

## Gate 8: Protocol Coverage

Every class in `infrastructure/` MUST implement at least one protocol defined
in `contracts/protocols.py` (or a sub-module of contracts).

Infrastructure without a protocol means the contract is implicit — a violation
of our "explicit over implicit" principle.

---

## Gate 9: Test-to-Promise Traceability

Every test file MUST have a module docstring referencing which component
promises (P-*) and invariants (INV-*) it validates.

Every promise in `docs/components/*.md` MUST have at least one corresponding
test (verified by scanning test docstrings for promise IDs).

---

## Enforcement

These gates are implemented as pytest tests in:
- `tests/test_design_gates.py` (Gates 1-7)
- `tests/test_contract_gates.py` (Gate 8)
- `tests/test_architecture.py` (existing boundary tests)

They run in CI on every push and are BLOCKING for merge.
