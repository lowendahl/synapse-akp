# Synapse AKP — Repository Agent Instructions

## Identity

You are working in the **Synapse Agentic Knowledge Pack** repository. This is
a compiler and runtime for building immutable, versioned knowledge packs from
curated Markdown sources. Knowledge packs are DuckDB databases that power
agentic retrieval, evidence-grounded reasoning, and interactive exploration.

## Repository Layout

```
compiler/          Python package — the KP compiler pipeline
  src/kp_compiler/ Source modules (parse, validate, graph, enrich, write)
  tests/           pytest suite (86+ tests)
  pyproject.toml   Package definition, ruff config, pytest config
okf/               OKF v0.2 knowledge corpus (canonical Markdown sources)
  csu/             CSU domain knowledge (69 concepts)
  mcem/            MCEM domain knowledge (44 concepts)
  ontology.yaml    Shared type/predicate schema
  pack-rules.yaml  Compile-time validation rules
docs/
  architecture/    Architecture vision, ADRs
  doctrine/        Engineering principles, design philosophy
  specifications/  Knowledge Pack SDD, Knowledge Architecture
dist/              Compiled pack artifacts (git-ignored)
```

## Key Technical Decisions

1. **DuckDB** is the physical storage engine for compiled packs (ADR-003).
2. **NetworkX** builds the in-memory graph during compilation (ADR-007).
3. **Pydantic** models the intermediate representation (ADR-008).
4. **Shared ontology** (`ontology.yaml`) is the single source of truth for valid
   concept types and predicates (ADR-002, ADR-005).
5. **Immutability** — published packs are never mutated; rebuild from source.
6. **Determinism** — identical input produces identical output (no non-deterministic
   enrichment in core compile path).

## Code Standards

- **Python 3.11+**, strict typing with Pydantic models.
- **Ruff** for linting and formatting (line-length 120, rules: E, F, I, N, W, UP, ANN, B, SIM).
- **pytest** for testing; prefer property-based tests (hypothesis) for core logic.
- **Clean Architecture** — domain logic has no infrastructure dependencies.
- All modules target **<200 lines of code**; split at natural responsibility boundaries.

## Design Rules (Enforced by Automated Gates)

These are NON-NEGOTIABLE. The gates in `tests/test_design_gates.py` enforce them:

1. **Classes over functions** — every `.py` module defines at least one class.
   No utility bags of loose functions. Use DDD: bounded contexts, not scripts.
2. **SQL confinement** — SQL strings ONLY in files within `queries/` or
   `persistence/` directories. Use the query object pattern.
3. **One concept per file** — domain files hold ≤4 related classes. No model dumps.
4. **Event types in contracts** — event dataclasses are the contract between
   publisher and subscriber. They live in `contracts/events.py`, not in the bus.
5. **No abbreviations** — public identifiers use full English words.
   `connection` not `con`, `configuration` not `cfg`, `parameters` not `params`.
   Code IS the documentation.
6. **Protocol coverage** — every infrastructure class implements a protocol from
   `contracts/`. No implicit contracts.
7. **Query object pattern** — database interactions encapsulated in query classes
   with an `execute(connection)` method. No ad-hoc SQL in orchestrators.

## Working with the Compiler

```bash
cd compiler
pip install -e ".[dev]"       # Install with dev deps
pytest                        # Run full test suite
ruff check src/ tests/        # Lint
ruff format src/ tests/       # Format

kp compile ../okf/mcem        # Compile a pack (reads pack.yaml)
kp compile ../okf/csu         # Compile with auto-detected dependency
kp-explore dist/*.duckdb      # Generate 3-D explorer
```

## Working with Knowledge Sources (OKF)

- Each concept is **one Markdown file** with YAML frontmatter.
- Frontmatter must include: `id`, `title`, `type`, `domain`, `relationships[]`.
- Types and predicates must exist in `ontology.yaml`.
- Cross-pack references use qualified IDs: `mcem.stage.stage-1-listen-consult`.
- Each knowledge base has a `pack.yaml` entry point for auto-discovery.

## Development Workflow (MANDATORY)

All work follows this sequence. No step may be skipped or reordered.

```
Epic / PBI
    ↓
Planning (Planner Agent)
    ↓
Component Definition (create/update docs/components/*.md)
  - Purpose, Responsibilities, Out of Scope, Promises, Invariants
    ↓
Tests (write tests FIRST — they start RED)
  - Tests honour component promises and invariants
    ↓
Implementation (write code to turn tests GREEN)
    ↓
Epic Complete Gate:
  → Architecture Governor review
  → Quality Agent review
  → Test Coverage validation
    ↓
Human Code Review
    ↓
Commit & merge to main
```

### Rules

1. **No code without a component definition** — every module must trace to a
   `docs/components/*.md` that declares its promises and invariants.
2. **Tests before code** — tests are written against the component contract
   *before* the implementation exists. The test suite defines done.
3. **Red → Green → Refactor** — TDD cycle. Never commit red tests.
4. **Gate reviews are blocking** — architecture governor, quality, and test
   coverage agents must pass before human review is requested.
5. **Commits only to feature branches** — main is protected; PRs require passing
   gates + human approval.

## Principles (apply to all work)

1. **Knowledge as code** — version-controlled, reviewed, tested, released.
2. **Compile-time correctness** — catch errors at build, not at query time.
3. **Evidence over opinion** — every assertion traces to a source.
4. **Ontology-first** — the ontology is the contract between authors and consumers.
5. **Agentic by design** — structures optimized for machine retrieval.
