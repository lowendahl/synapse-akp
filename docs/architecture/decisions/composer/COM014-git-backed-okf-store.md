# COM014: Git-Backed OKF Is the Canonical Knowledge Store

**Status:** Draft  
**Capability:** Composer  
**Date:** 2026-07-27

## Context

Composer needs a durable system of record for authored knowledge that is human-readable, diffable, reviewable and independent of the application runtime. Working databases are useful for jobs, candidates and diagnostics, but they should not become the canonical publication surface.

## Decision

Treat the Git-backed OKF repository as the canonical authored knowledge product. Composer may use a working database for candidates, temporary embeddings, review tasks, model outputs, jobs and diagnostics, but only accepted knowledge plus required provenance may enter the OKF repository. Use Git CLI initially, adopt Dulwich or pygit2 only if embedded operations become necessary, use conventional pull requests for enterprise review, and create signed tags or release manifests as the compilation boundary.

## Consequences

Composer knowledge stays portable and auditable, and the compiler can consume immutable, reviewable releases rather than mutable service state. Databases remain working stores, not the authoritative truth, which keeps Composer independent from any one persistence implementation.
