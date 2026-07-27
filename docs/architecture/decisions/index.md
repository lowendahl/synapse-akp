---
type: Index
title: Architecture Decisions
description: Capability-scoped architecture decision records for the Synapse AKP architecture
tags: [adr, architecture, decisions]
generated: { by: human:plwendahl, at: 2026-07-27T15:43:35+02:00 }
status: stable
---

# Architecture Decisions

## Generic

Cross-cutting framework decisions that apply across capabilities.

- [G001 Stable IDs in Frontmatter](./generic/G001-stable-ids-in-frontmatter.md)
- [G002 Formal Ontology](./generic/G002-formal-ontology.md)
- [G003 Two-Pack Topology](./generic/G003-two-pack-topology.md)
- [G004 Shared Ontology Cross-Pack References](./generic/G004-shared-ontology-cross-pack-refs.md)
- [G005 MCEM Independence](./generic/G005-mcem-independence.md)
- [G006 Compiler Engineering Principles](./generic/G006-compiler-engineering-principles.md)
- [G007 Code Standards Architecture](./generic/G007-code-standards-architecture.md)
- [G008 AKP Runtime Neutral](./generic/G008-akp-runtime-neutral.md)
- [G009 AKP Model Neutral](./generic/G009-akp-model-neutral.md)
- [G010 Object-Level Governance](./generic/G010-object-level-governance.md)
- [G011 Provenance Survives Compilation](./generic/G011-provenance-survives-compilation.md)
- [G012 No Runtime Mutation](./generic/G012-no-runtime-mutation.md)
- [G013 Logical Capability Separation](./generic/G013-logical-capability-separation.md)
- [G014 Immutable Releases](./generic/G014-immutable-releases.md)
- [G015 Inferred vs Authored](./generic/G015-inferred-vs-authored.md)
- [G016 Pack Format Specification](./generic/G016-pack-format-specification.md)
- [G017 Domain Agnostic Framework](./generic/G017-domain-agnostic-framework.md)
- [G018 LLM Protocol Copilot Provider](./generic/G018-llm-protocol-copilot-provider.md)
- [G019 Generated Source Layers](./generic/G019-generated-source-layers.md)
- [G020 Semantic Reasoning Protocol](./generic/G020-semantic-reasoning-protocol.md)
- [G021 Framework Content Separation](./generic/G021-framework-content-separation.md)
- [Generic ADR Legacy Index](./generic/index.md)

## Compiler

Compiler-pipeline decisions and open compiler ADRs.

- [CMP001 DuckDB Physical Engine](./compiler/CMP001-duckdb-physical-engine.md)
- [CMP002 Graph DuckDB NetworkX](./compiler/CMP002-graph-duckdb-networkx.md)
- [CMP003 Pydantic Intermediate Representation](./compiler/CMP003-pydantic-intermediate-representation.md)
- [CMP004 V1 Compiler Scope](./compiler/CMP004-v1-compiler-scope.md)
- [CMP005 V2 Compiler Scope](./compiler/CMP005-v2-compiler-scope.md)
- [CMP006 Ontology Discovery](./compiler/CMP006-ontology-discovery.md)
- [CMP007 Pack Rules Engine](./compiler/CMP007-pack-rules-engine.md)
- [CMP008 Acronym Discovery](./compiler/CMP008-acronym-discovery.md)
- [CMP009 Unified Semantic Pipeline](./compiler/CMP009-unified-semantic-pipeline.md)
- [CMP010 Semantic Taxonomy Classification](./compiler/CMP010-semantic-taxonomy-classification.md)
- [CMP011 Assertion Level Confidence](./compiler/CMP011-assertion-level-confidence.md)
- [CMP012 Measure Indicator KPI Chain](./compiler/CMP012-measure-indicator-kpi-chain.md)
- [CMP013 Formula Extraction Dependency Graphs](./compiler/CMP013-formula-extraction-dependency-graphs.md)
- [CMP014 Semantic DuckDB Schema](./compiler/CMP014-semantic-duckdb-schema.md)
- [CMP015 Vector Engine](./compiler/CMP015-vector-engine.md)
- [CMP016 Embedding Model](./compiler/CMP016-embedding-model.md)
- [Semantic Pipeline Index](./compiler/semantic-pipeline-index.md)

## Runtime

Runtime and MCP decisions.

- [RTM001 Hybrid Retrieval](./runtime/RTM001-hybrid-retrieval.md)
- [RTM002 Portable Graph](./runtime/RTM002-portable-graph.md)
- [RTM003 MCP stdio Transport](./runtime/RTM003-mcp-stdio-transport.md)
- [RTM004 Explain Operation](./runtime/RTM004-explain-operation.md)
- [RTM005 Concept Centric Resolution](./runtime/RTM005-concept-centric-resolution.md)

## Composer

Composer-specific decisions will be added here from draft ADRs.
