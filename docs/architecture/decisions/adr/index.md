---
type: Index
title: Architecture Decision Records
description: Accepted and open ADRs for the Synapse AKP architecture
tags: [adr, architecture, decisions]
generated: { by: human:plwendahl, at: 2026-07-26T13:27:44Z }
status: stable
---

# Architecture Decision Records

## Accepted

| ADR | Title | Date |
|-----|-------|------|
| [ADR-001](./adr-001-stable-ids-in-frontmatter.md) | Stable IDs in OKF Frontmatter | 2026-07-25 |
| [ADR-002](./adr-002-formal-ontology.md) | Formal Ontology Extracted from Corpus | 2026-07-25 |
| [ADR-003](./adr-003-duckdb-physical-engine.md) | DuckDB as Physical Metadata Engine | 2026-07-25 |
| [ADR-004](./adr-004-two-pack-topology.md) | Two-Pack Topology (MCEM + CSU) | 2026-07-25 |
| [ADR-005](./adr-005-shared-ontology-cross-pack-refs.md) | Shared Ontology and Cross-Pack References | 2026-07-25 |
| [ADR-006](./adr-006-mcem-independence.md) | MCEM Pack Compiles Independently | 2026-07-25 |
| [ADR-007](./adr-007-graph-duckdb-networkx.md) | Graph: DuckDB Storage, NetworkX as Compiler Tool | 2026-07-25 |
| [ADR-008](./adr-008-pydantic-intermediate-representation.md) | Pydantic Domain Objects as Compiler IR | 2026-07-25 |
| [ADR-009](./adr-009-v1-compiler-scope.md) | V1 Compiler Scope and Dependency Stack | 2026-07-25 |
| [ADR-010](./adr-010-compiler-engineering-principles.md) | Knowledge Compiler Engineering Principles | 2026-07-25 |
| [ADR-011](./adr-011-code-standards-architecture.md) | Compiler Code Standards and Architecture | 2026-07-25 |
| [ADR-012](./adr-012-v2-compiler-scope.md) | V2 Compiler Scope (BM25, Enrichment, Cross-Pack) | 2026-07-25 |
| [ADR-013](./adr-013-ontology-discovery.md) | Ontology Discovery Mode | 2026-07-25 |
| [ADR-014](./adr-014-pack-rules-engine.md) | Pack Rules Engine & Outcome Validator | 2026-07-25 |
| [ADR-015](./adr-015-akp-runtime-neutral.md) | AKP SHALL Remain Runtime-Neutral | 2026-07-26 |
| [ADR-016](./adr-016-akp-model-neutral.md) | AKP SHALL Remain Model-Neutral | 2026-07-26 |
| [ADR-017](./adr-017-object-level-governance.md) | Governance SHALL Be Object-Level | 2026-07-26 |
| [ADR-018](./adr-018-provenance-survives-compilation.md) | Provenance SHALL Survive Compilation | 2026-07-26 |
| [ADR-019](./adr-019-no-runtime-mutation.md) | Runtime Learning SHALL NOT Directly Mutate Packages | 2026-07-26 |
| [ADR-020](./adr-020-logical-capability-separation.md) | Logical Capabilities SHALL Be Separated from Implementations | 2026-07-26 |
| [ADR-021](./adr-021-hybrid-retrieval.md) | Hybrid Retrieval SHALL Be Supported | 2026-07-26 |
| [ADR-022](./adr-022-portable-graph.md) | The Package Graph SHALL Be Portable | 2026-07-26 |
| [ADR-023](./adr-023-immutable-releases.md) | Released Package Versions SHOULD Be Immutable | 2026-07-26 |
| [ADR-024](./adr-024-inferred-vs-authored.md) | Inferred Knowledge SHALL Be Distinguishable from Authored Knowledge | 2026-07-26 |

## Open

| OADR | Title |
|------|-------|
| [OADR-001](./oadr-001-vector-engine.md) | Vector Engine Selection |
| [OADR-002](./oadr-002-embedding-model.md) | Default Embedding Model |
