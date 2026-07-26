---
type: ADR
title: "ADR-011 — Compiler Code Standards and Architecture"
id: adr.011
status: accepted
date: 2026-07-25
decision_makers: [plwendahl]
tags: [adr, code-standards, architecture, testing, boundaries, adapters]
---

# ADR-011 — Compiler Code Standards and Architecture

## Status

**Accepted** — 2026-07-25

## Context

The Knowledge Compiler is a production system that must be maintainable, testable, and comprehensible to engineers joining the project. Without explicit code standards, systems decay into coupled, untestable, and opaque monoliths.

This ADR establishes non-negotiable engineering standards for the compiler codebase, drawn from:
- Dependency Inversion Principle (DIP)
- Separation of Concerns (SoC)
- Adapter Pattern for infrastructure abstraction
- Contract-first specification
- Rust-style strictness in a Python codebase
- TDD (test-first development)
- Convention over configuration

## Code Organization

### Top-Level Structure

```
kp_compiler/
├── contracts/                # Protocols and ABCs — NO implementations here
│   ├── __init__.py
│   ├── parser.py            # Protocol: SourceParser
│   ├── normalizer.py        # Protocol: Normalizer
│   ├── validator.py         # Protocol: Validator
│   ├── enricher.py          # Protocol: Enricher
│   ├── graph_builder.py     # Protocol: GraphBuilder
│   ├── projector.py         # Protocol: Projector
│   ├── assembler.py         # Protocol: PackAssembler
│   ├── events.py            # Domain event base types
│   └── errors.py            # Typed exception hierarchy
│
├── domain/                   # Pure domain logic — NO infrastructure imports
│   ├── __init__.py
│   ├── models.py            # Pydantic domain objects (KnowledgeObject, etc.)
│   ├── ontology.py          # Ontology loading and enforcement
│   ├── identity.py          # Stable ID generation and validation
│   ├── provenance.py        # Provenance record construction
│   ├── semantic_units.py    # Semantic unit boundary detection
│   └── diagnostics.py       # Diagnostic collection and classification
│
├── stages/                   # Pipeline stage implementations
│   ├── __init__.py
│   ├── discover.py          # Source discovery
│   ├── parse.py             # Markdown + YAML → Pydantic
│   ├── normalize.py         # Canonical forms, alias expansion
│   ├── validate.py          # Ontology + schema validation
│   ├── resolve.py           # ID resolution, reference linking
│   ├── enrich.py            # spaCy NLP, acronym extraction
│   ├── graph.py             # NetworkX graph construction + analysis
│   └── project/             # Projection builders
│       ├── __init__.py
│       ├── canonical.py     # Canonical object table
│       ├── graph_export.py  # Node/edge tables + metrics
│       ├── lexical.py       # BM25 index
│       ├── dense.py         # FastEmbed vectors
│       └── alias.py         # Alias registry
│
├── infrastructure/           # Adapter implementations — ALL IO lives here
│   ├── __init__.py
│   ├── filesystem.py        # File reading/writing adapter
│   ├── duckdb_writer.py     # DuckDB pack writer adapter
│   ├── usearch_writer.py    # USearch vector index adapter
│   ├── git_resolver.py      # Git revision resolver adapter
│   ├── spacy_adapter.py     # spaCy NLP adapter
│   ├── fastembed_adapter.py # FastEmbed embedding adapter
│   └── bm25s_adapter.py    # BM25S index adapter
│
├── pipeline/                 # Orchestration
│   ├── __init__.py
│   ├── compiler.py          # Main pipeline DAG orchestrator
│   ├── config.py            # Build configuration loading
│   └── manifest.py          # Manifest generation + hashing
│
├── events/                   # Domain events (observability)
│   ├── __init__.py
│   ├── compilation.py       # StageStarted, StageCompleted, DiagnosticEmitted
│   ├── validation.py        # OntologyViolation, OrphanDetected, CycleDetected
│   └── bus.py               # Event bus (publish/subscribe)
│
└── cli.py                    # Entry point (thin shell — delegates immediately)


tests/
├── unit/                     # Fast, isolated, no IO
│   ├── domain/
│   │   ├── test_models.py
│   │   ├── test_ontology.py
│   │   ├── test_identity.py
│   │   └── test_provenance.py
│   ├── stages/
│   │   ├── test_parse.py
│   │   ├── test_normalize.py
│   │   ├── test_validate.py
│   │   ├── test_resolve.py
│   │   ├── test_enrich.py
│   │   └── test_graph.py
│   └── projections/
│       ├── test_canonical.py
│       ├── test_lexical.py
│       └── test_dense.py
│
├── integration/              # Tests with real infrastructure (DuckDB, filesystem)
│   ├── test_duckdb_writer.py
│   ├── test_usearch_writer.py
│   ├── test_full_pipeline.py
│   └── test_pack_integrity.py
│
└── fixtures/                 # Test data (minimal OKF files)
    ├── minimal_corpus/
    ├── invalid_corpus/
    └── expected_outputs/
```

## Engineering Standards

### ES-01 — Contracts and implementations live in separate packages

`contracts/` defines **Protocol classes** (Python typing.Protocol) and **abstract base classes**. These files contain ZERO implementation logic.

`stages/` and `infrastructure/` contain implementations that satisfy those contracts.

**Rule:** No file in `domain/` or `stages/` may import from `infrastructure/`. Dependencies flow inward.

```
contracts/ ← domain/ ← stages/ ← infrastructure/
                                       ↑
                                  pipeline/ (orchestrator wires adapters to stages)
```

### ES-02 — Dependency Inversion Principle

Stages depend on **protocols**, not concrete implementations.

```python
# stages/parse.py
from kp_compiler.contracts.parser import SourceReader  # Protocol

class MarkdownParser:
    def __init__(self, reader: SourceReader):  # injected, not imported
        self._reader = reader
```

The pipeline orchestrator wires concrete adapters at composition time:

```python
# pipeline/compiler.py
parser = MarkdownParser(reader=FilesystemReader(source_path))
```

### ES-03 — Adapter pattern for all infrastructure

Every external system (filesystem, DuckDB, USearch, spaCy, FastEmbed, git) is accessed ONLY through an adapter in `infrastructure/`.

Each adapter:
- implements a Protocol from `contracts/`;
- is the ONLY file that imports the third-party library;
- is independently testable with a mock;
- can be replaced without touching domain or stage logic.

```python
# contracts/embedder.py
class Embedder(Protocol):
    def embed_passages(self, texts: list[str]) -> list[list[float]]: ...
    def embed_query(self, query: str) -> list[float]: ...

# infrastructure/fastembed_adapter.py
from fastembed import TextEmbedding
from kp_compiler.contracts.embedder import Embedder

class FastEmbedAdapter:
    """Implements Embedder protocol using FastEmbed."""
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        self._model = TextEmbedding(model_name)

    def embed_passages(self, texts: list[str]) -> list[list[float]]:
        return list(self._model.passage_embed(texts))

    def embed_query(self, query: str) -> list[float]:
        return list(self._model.query_embed(query))[0]
```

### ES-04 — Typed exceptions (no bare Exception, no string errors)

All errors are typed, domain-specific exceptions defined in `contracts/errors.py`:

```python
# contracts/errors.py
from dataclasses import dataclass

class CompilerError(Exception):
    """Base for all compiler errors."""

@dataclass
class OntologyViolation(CompilerError):
    source_file: str
    line: int | None
    object_id: str
    violation: str  # e.g., "Unknown type 'Foobar'; allowed: Framework, Metric, ..."

@dataclass
class DanglingReference(CompilerError):
    source_file: str
    reference_id: str
    expected_in: str  # "local" | "cross-pack:kp-mcem"

@dataclass
class DuplicateId(CompilerError):
    id: str
    first_file: str
    second_file: str

@dataclass
class ProvenanceMissing(CompilerError):
    object_id: str
    stage: str
```

**Rule:** Never `raise Exception("something went wrong")`. Every raise uses a typed exception with structured context.

### ES-05 — Domain events for observability

Every significant compiler action emits a domain event via the event bus:

```python
# events/compilation.py
@dataclass(frozen=True)
class StageStarted:
    stage: str
    file_count: int
    timestamp: datetime

@dataclass(frozen=True)
class StageCompleted:
    stage: str
    duration_ms: float
    objects_produced: int
    diagnostics: int

@dataclass(frozen=True)
class DiagnosticEmitted:
    severity: str  # error | warning | info
    source_file: str
    message: str
    stage: str
```

Events are logged structurally (JSON lines). No print statements.

### ES-06 — Contract-first specification

Before implementing a stage:
1. Define the Protocol in `contracts/`.
2. Write the typed input/output models in `domain/`.
3. Write failing tests against the contract.
4. Then implement.

The contract IS the specification. Implementation follows.

### ES-07 — TDD style tests

Every component is developed test-first:

1. **Unit tests** — test domain logic and stages in isolation (mocked adapters). Fast. No IO.
2. **Integration tests** — test adapters with real infrastructure (DuckDB file, filesystem). Slower.
3. **Contract tests** — verify adapters satisfy their Protocol (run same test suite against mock and real adapter).

Test naming convention: `test_{behavior}_when_{condition}_then_{expected}`.

```python
def test_parser_extracts_stable_id_when_frontmatter_has_id_field():
    ...

def test_validator_emits_error_when_type_not_in_ontology():
    ...

def test_graph_detects_cycle_when_circular_dependency_exists():
    ...
```

### ES-08 — One responsibility per file, 200 LOC extraction rule

- Each file has ONE class or ONE cohesive set of functions for ONE responsibility.
- File names describe the responsibility (not the class name).
- If a file exceeds **200 lines of code** (excluding tests, imports, docstrings): extract and encapsulate into a new file.
- No file shall contain multiple unrelated classes.

### ES-09 — Rust-style strictness in Python

- **No `Any` types** — everything is typed. Use `Protocol`, `TypeVar`, generics.
- **No optional without handling** — every `Optional[T]` has an explicit None check or `.model_dump(exclude_none=True)`.
- **No mutable default arguments** — use `Field(default_factory=list)`.
- **No bare `dict`** — use Pydantic models or TypedDict.
- **Exhaustive match** — use `match/case` with `case _: raise` or explicit enum coverage.
- **Immutable where possible** — `frozen=True` on dataclasses, `model_config = ConfigDict(frozen=True)` on Pydantic.
- **Explicit over implicit** — no magic. No metaclasses. No runtime monkeypatching.

### ES-10 — Convention over configuration

| Convention | Meaning |
|------------|---------|
| `contracts/` | All protocols live here |
| `domain/` | Pure logic, no imports from `infrastructure/` |
| `infrastructure/` | All IO, all third-party adapters |
| `stages/` | Pipeline step implementations |
| `events/` | Domain events + event bus |
| `tests/unit/` | Fast tests, mocked IO |
| `tests/integration/` | Real IO tests |
| `_adapter` suffix | File implements a Protocol for external system |
| `test_` prefix | Test file |
| `Verb + Noun` stage names | `discover`, `parse`, `normalize`, `validate`, `resolve` |

No configuration file needed to understand where things live. The folder structure IS the architecture.

### ES-11 — No infrastructure leaks outside boundaries

- `stages/graph.py` calls `self._graph_builder.build(objects)` — it does NOT import `networkx` directly.
- `stages/project/dense.py` calls `self._embedder.embed_passages(texts)` — it does NOT import `fastembed` directly.
- Only files in `infrastructure/` import third-party infrastructure libraries.

**Exception:** `pydantic` and `networkx` are considered domain libraries (they model knowledge, not IO). They may be imported in `domain/` and `stages/`.

### ES-12 — Component notes

Every major component (stage, adapter, domain model) SHALL have a docstring or accompanying `.md` file explaining:

1. **What** — what this component does
2. **Why** — why it exists as a separate component
3. **Contracts** — which protocols it implements or depends on
4. **Boundaries** — what it may NOT do (e.g., "this stage must not perform IO")
5. **Test strategy** — how it's tested (unit vs integration)

Example (top of `stages/parse.py`):

```python
"""
Parser Stage — Markdown + YAML → Pydantic Domain Objects

What: Reads OKF markdown files and produces typed KnowledgeObject instances.
Why: Separates raw file parsing from normalization, validation, and enrichment.
Contracts: Depends on SourceReader (Protocol). Produces list[KnowledgeObject].
Boundaries: Must NOT validate ontology, resolve references, or perform enrichment.
Test strategy: Unit tests with in-memory string fixtures. No filesystem access.
"""
```

## Consequences

- New engineers can navigate the codebase by folder structure alone.
- Swapping infrastructure (e.g., DuckDB → SQLite) requires changing ONE adapter file.
- All domain logic is testable without IO — fast CI.
- Typed exceptions make error handling explicit and debuggable.
- Domain events provide audit trail without coupling to a logging framework.
- The 200 LOC rule prevents god-classes from forming.
- Contract-first development prevents implementation drift from specification.

## Relationship to Other ADRs

| ADR | How This Relates |
|-----|-----------------|
| ADR-008 (Pydantic IR) | Domain models defined in `domain/models.py` |
| ADR-007 (NetworkX) | NetworkX is a domain library; graph logic in `stages/graph.py` |
| ADR-003 (DuckDB) | DuckDB access ONLY through `infrastructure/duckdb_writer.py` |
| ADR-009 (V1 Scope) | This ADR governs HOW the V1 pipeline is built |
| ADR-010 (Principles) | This ADR operationalizes those principles into code standards |
