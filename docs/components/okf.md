# OKF

## Purpose

Human-authored, machine-parseable knowledge source format.

## Responsibilities

- Define the canonical source structure for authored knowledge
- Support diffing, review, and collaboration in source control
- Declare metadata, relationships, and authored semantics explicitly

## Out of Scope

- Compilation
- Deployment
- Runtime serving

## Promises

- Stable authoring contract
- Git-friendly structure
- Human-readable source files

## Invariants

- Every source file has frontmatter with `id`, `type`, and `title`
- Relationships are explicit rather than inferred by file layout
