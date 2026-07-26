# AKP Compiler

## Purpose

Transform OKF sources into deployable AKP artifacts.

## Responsibilities

- Parse source files into a compiler representation
- Validate structure, references, and semantics
- Enrich retrieval content where configured
- Build the package graph
- Build the retrieval corpus
- Generate embeddings or embedding inputs
- Propagate governance metadata
- Assemble the package artifact
- Produce a build report

## Out of Scope

- Serving knowledge
- Executing business logic
- Runtime queries

## Promises

- Deterministic compilation
- Fail-fast behavior on material errors
- Traceable enrichments and derivations

## Invariants

- Same input produces semantically equivalent output
- No artifact is published on validation failure
- Authored knowledge takes precedence over inferred knowledge
