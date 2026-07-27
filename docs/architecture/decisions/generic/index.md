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
| [ADR-025](./adr-025-pack-format-specification.md) | Pack Format Specification (Schema 2.0.0) | 2026-07-26 |
| [ADR-026](./adr-026-mcp-stdio-transport.md) | MCP stdio Transport for Runtime | 2026-07-26 |
| [ADR-027](./adr-027-acronym-discovery.md) | Acronym Discovery Pipeline | 2026-07-26 |
| [ADR-028](./adr-028-domain-agnostic-framework.md) | Domain-Agnostic Framework Design | 2026-07-26 |
| [ADR-029](./adr-029-llm-protocol-copilot-provider.md) | LLM Protocol & Copilot Provider | 2026-07-26 |
| [ADR-030](./adr-030-unified-semantic-pipeline.md) | Unified Semantic Compilation Pipeline | 2026-07-26 |
| [ADR-031](./adr-031-semantic-taxonomy-classification.md) | Semantic Taxonomy Classification | 2026-07-26 |
| [ADR-032](./adr-032-assertion-level-confidence.md) | Assertion-Level Confidence Scoring | 2026-07-26 |
| [ADR-033](./adr-033-measure-indicator-kpi-chain.md) | Measure → Indicator → KPI Chain | 2026-07-26 |
| [ADR-034](./adr-034-formula-extraction-dependency-graphs.md) | Formula Extraction & Dependency Graphs | 2026-07-26 |
| [ADR-035](./adr-035-generated-source-layers.md) | Generated vs Authored Source Layers | 2026-07-26 |
| [ADR-036](./adr-036-semantic-reasoning-protocol.md) | Semantic Reasoning Protocol | 2026-07-26 |
| [ADR-037](./adr-037-semantic-duckdb-schema.md) | Semantic DuckDB Schema Extension | 2026-07-26 |
| [ADR-038](./adr-038-explain-operation.md) | Explain Operation — Human-Readable Concept Explanation | 2026-07-27 |
| [ADR-039](./adr-039-concept-centric-resolution.md) | Concept-Centric Resolution and Multi-Faceted Explanation | 2026-07-27 |

## Open

| OADR | Title |
|------|-------|
| [OADR-001](./oadr-001-vector-engine.md) | Vector Engine Selection |
| [OADR-002](./oadr-002-embedding-model.md) | Default Embedding Model |
