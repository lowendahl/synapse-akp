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

## Principles (apply to all work)

1. **Knowledge as code** — version-controlled, reviewed, tested, released.
2. **Compile-time correctness** — catch errors at build, not at query time.
3. **Evidence over opinion** — every assertion traces to a source.
4. **Ontology-first** — the ontology is the contract between authors and consumers.
5. **Agentic by design** — structures optimized for machine retrieval.
