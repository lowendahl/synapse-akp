---
type: ADR
title: "ADR-010 — Knowledge Compiler Engineering Principles"
id: adr.010
status: accepted
date: 2026-07-25
decision_makers: [plwendahl]
tags: [adr, compiler, engineering, principles, design]
---

# ADR-010 — Knowledge Compiler Engineering Principles

## Status

**Accepted** — 2026-07-25

## Context

The Knowledge Pack SDD defines WHAT the compiler must produce. This ADR defines HOW the compiler itself must be engineered — the design principles that govern its construction, testability, extensibility, and operational behavior.

A Knowledge Compiler is not a one-shot script. It is a production system that:
- runs repeatedly as canonical sources evolve;
- must produce reproducible output;
- must fail visibly and diagnostically;
- must be testable at every stage;
- must be extensible without rewriting.

## Engineering Principles

### CP-01 — Each stage is an independent, testable function

Every compilation stage (parse, normalize, validate, resolve, enrich, project, assemble) SHALL be implementable and testable in isolation.

A stage:
- receives typed input (Pydantic model or NetworkX graph);
- produces typed output;
- declares its dependencies explicitly;
- can be unit-tested without running the full pipeline.

No stage shall depend on global state or side effects from another stage.

### CP-02 — The pipeline is a directed acyclic graph of stages

Stages execute in dependency order. The compiler SHALL model the pipeline as a DAG, not a linear script.

This enables:
- parallel execution of independent stages;
- incremental rebuild (only re-run stages whose inputs changed);
- clear visualization of the build process;
- isolated failure (one stage fails, others remain valid).

### CP-03 — Every stage emits structured diagnostics

A stage SHALL NOT:
- silently skip invalid input;
- log errors only to stdout;
- raise untyped exceptions.

A stage SHALL:
- emit diagnostics as structured objects (Pydantic models);
- classify each diagnostic as `error`, `warning`, or `info`;
- include source location (file, line, section) in every diagnostic;
- continue processing where possible (collect all errors, don't stop at first).

### CP-04 — Configuration is explicit and versioned

The compiler SHALL read all configuration from explicit sources:
- `ontology.yaml` (types, predicates, constraints);
- `build.yaml` (source paths, pack ID, version, feature flags);
- environment variables for secrets only (API keys for enrichment models).

No behavior shall be governed by implicit convention, hidden defaults, or framework magic. Every configuration value SHALL have a declared default or be required.

Configuration version is recorded in the manifest.

### CP-05 — Deterministic stages produce identical output

Given the same source revision and compiler version, deterministic stages (parse, normalize, validate, resolve, extract) SHALL produce byte-for-byte identical output.

This means:
- no reliance on dict ordering (use sorted output);
- no timestamps in deterministic output (timestamps go in manifest only);
- no random IDs (use deterministic hashing);
- reproducibility is tested in CI.

### CP-06 — Nondeterministic stages are isolated and recorded

Model-assisted stages (LLM enrichment, embedding generation) SHALL:
- run AFTER all deterministic stages;
- record model ID, version, parameters, and input hash;
- never overwrite deterministic output;
- produce output marked with `origin: inferred` or `origin: generated`;
- be skippable via build configuration (deterministic-only builds must work).

### CP-07 — The compiler is stateless between runs

The compiler SHALL NOT maintain state between invocations. Every run starts from:
- canonical sources (files on disk);
- configuration (yaml);
- optionally, a prior manifest (for incremental builds).

No database, cache, or state file is required for a clean build. Caches are optimization, not correctness.

### CP-08 — Fail fast, fail loud, fail with context

The compiler SHALL halt publication when:
- any `error`-level diagnostic exists;
- the manifest cannot be assembled;
- content hashes don't validate;
- required projections are missing.

Failure output SHALL include:
- all diagnostics (not just the first);
- the stage that failed;
- the source file(s) involved;
- a human-readable explanation.

A partial or invalid pack SHALL NEVER be published.

### CP-09 — Every output is traceable to source

Every row in DuckDB, every node in the graph, every vector in the index SHALL carry or reference:
- the source file path;
- the source revision (git SHA);
- the compiler version;
- the stage that produced it;
- the origin classification (authored / derived / inferred / generated).

This is non-negotiable. If provenance is missing, the build fails.

### CP-10 — The compiler is the ontology enforcer

The compiler SHALL validate:
- every `type` field against `ontology.yaml` allowed types;
- every relationship predicate against allowed predicates;
- required frontmatter fields per type;
- cardinality constraints;
- ID format conventions.

Unknown types or predicates SHALL produce an `error` diagnostic. The compiler does not guess.

### CP-11 — Projections are independent and rebuildable

Each projection (canonical objects, graph, lexical, dense vectors, alias registry) SHALL be:
- buildable independently from the normalized model;
- deletable without affecting other projections;
- rebuildable without re-running earlier stages (given cached intermediate output).

This enables:
- embedding model upgrades (rebuild vectors only);
- lexical tuning (rebuild BM25 only);
- graph predicate changes (rebuild graph only).

### CP-12 — The compiler separates IO from logic

All file reading, network calls, and database writes SHALL be isolated in adapter layers.

Core compilation logic (validation, graph building, enrichment) SHALL operate on in-memory Pydantic models and NetworkX graphs — never on file handles, HTTP responses, or database cursors directly.

This enables:
- unit testing without filesystem;
- mocking external services;
- swapping storage backends.

### CP-13 — Build time is bounded and observable

The compiler SHALL:
- report progress per stage (files processed, time elapsed);
- emit timing metrics per stage;
- support a `--dry-run` mode (validate without writing output);
- support a `--profile` mode (emit detailed timing);
- target <60 seconds for a full clean build of ~130 files.

If a stage exceeds its time budget, it logs a warning.

### CP-14 — The compiler is its own first user

The compiler's diagnostic output (orphans, dangling refs, type errors, cycles) SHALL be used to validate the canonical OKF corpus in CI.

Running `kp-compile --validate-only` SHALL be a CI gate on the OKF repository. Authors get immediate feedback when their changes violate the ontology or break references.

### CP-15 — Extension points are explicit, not framework-inherited

New object types, predicates, enrichment methods, or projection formats SHALL be added through:
- ontology.yaml changes (new types/predicates);
- new Pydantic models (new object schemas);
- new projection builders (registered in build config);
- new enrichment plugins (declared in configuration).

No inheritance hierarchies, no plugin autodiscovery, no metaclass registration. Explicit over implicit.

## Consequences

- The compiler is testable, reproducible, and diagnosable.
- Each stage can be developed, tested, and optimized independently.
- Authors get fast CI feedback on ontology violations.
- Changing one projection (e.g., vectors) doesn't require rebuilding everything.
- The compiler remains understandable to a new engineer reading the code.
- No framework lock-in — every library is behind an adapter.

## Relationship to Other ADRs

| ADR | How This Relates |
|-----|-----------------|
| ADR-002 (Ontology) | CP-10 — compiler enforces the ontology |
| ADR-003 (DuckDB) | CP-12 — DuckDB is behind an IO adapter |
| ADR-007 (NetworkX) | CP-01 — NetworkX stages are testable functions |
| ADR-008 (Pydantic) | CP-01 — typed inputs/outputs per stage |
| ADR-009 (V1 Scope) | Principles govern HOW the V1 pipeline is built |
