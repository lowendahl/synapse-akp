# Synapse Composer

## Software Design Description

**Document status:** Draft  
**System:** Synapse Composer  
**Product family:** Synapse Agentic Knowledge Platform  
**Primary output:** Open Knowledge Format Wiki  
**Downstream system:** Synapse AK Compiler  
**Target runtime:** Local-first with enterprise deployment profile  
**Architecture style:** Modular pipeline, durable workflow, human-governed knowledge composition

---

# 1. Purpose

Synapse Composer is the authoring and knowledge-engineering environment for the Synapse Agentic Knowledge Pack framework.

It accepts heterogeneous source material, including:

- PDF
- Microsoft Word
- Microsoft PowerPoint
- Markdown
- Web URLs
- Images and diagrams
- Existing OKF repositories
- Structured JSON and YAML
- Manual author input

It transforms these sources into a governed, evidence-backed, machine-readable OKF Wiki that can be validated, versioned, released, and compiled into an Agentic Knowledge Pack.

The Composer is responsible for converting information into structured knowledge.

It is not responsible for:

- Compiling the final AKP implementation
- Serving runtime retrieval
- Planning agent actions
- Executing business operations
- Replacing document-management platforms
- Acting as a general-purpose web crawler
- Automatically publishing material knowledge without governance

The core system flow is:

```
Source material
      ↓
Acquisition
      ↓
Format-aware extraction
      ↓
Canonical Document Model
      ↓
Semantic interpretation
      ↓
Candidate Knowledge Objects
      ↓
Knowledge resolution
      ↓
Human-governed review
      ↓
Git-backed OKF Wiki
      ↓
Immutable OKF release
      ↓
Synapse AK Compiler
      ↓
Agentic Knowledge Pack
```

---

# 2. Design Goals

Synapse Composer shall:

1. Preserve source fidelity and provenance.
2. Support multiple document formats through replaceable adapters.
3. Separate document extraction from semantic interpretation.
4. Separate source interpretation from existing-knowledge resolution.
5. Produce explicit and reviewable knowledge-change proposals.
6. Use stable knowledge identities independent of filenames and wording.
7. Enable human review by exception.
8. Support incremental recomposition when sources change.
9. Produce portable and version-controlled OKF repositories.
10. Compile only immutable and validated OKF releases.
11. Support local, enterprise, and hybrid deployment profiles.
12. Keep models, parsers, graph engines, and vector stores replaceable.
13. Provide reproducible and auditable composition workflows.
14. Measure quality through a versioned evaluation corpus.

---

# 3. Non-Goals

The initial implementation shall not attempt to provide:

- Autonomous publication of policies or authoritative knowledge
- General enterprise content management
- Rich collaborative document editing
- Foundation-model training
- Full enterprise search
- Broad internet crawling
- Legal or regulatory interpretation without human review
- Automatic information declassification
- Runtime RAG orchestration
- Dynamic business-process execution
- Full graph-database infrastructure
- Automatic ontology generation without governance

---

# 4. Architecture Principles

## 4.1 Preserve before interpreting

The system shall create an immutable representation of acquired source content before semantic interpretation begins.

## 4.2 Sources are evidence, not the knowledge model

Document structure may inform the OKF Wiki, but the original folder, page, or slide structure shall not automatically define the knowledge architecture.

## 4.3 Extraction and interpretation are separate concerns

Extraction answers: What content and structure exist in the source?

Interpretation answers: What knowledge does that content represent?

## 4.4 Interpretation and resolution are separate concerns

Interpretation identifies what is present in a source. Resolution determines how the proposed knowledge relates to the existing OKF knowledge space.

## 4.5 Agents propose; governed services commit

Language models and specialist agents may create proposals. Only deterministic application services may commit accepted changes to the canonical OKF repository.

## 4.6 Provenance is structural

Evidence lineage is a required part of every publishable knowledge object.

## 4.7 OKF is the canonical authored knowledge product

Databases store working state. The Git-backed OKF repository stores accepted knowledge.

## 4.8 Runtime projections are disposable

Embeddings, search indexes, graph databases, and caches are rebuildable projections.

## 4.9 Compilation is release-based

Only immutable OKF releases may be compiled into AKP artifacts.

## 4.10 Human attention is applied by materiality

The system shall prioritize review of ambiguous, conflicting, unsupported, sensitive, or high-impact knowledge.

---

# 5. System Context

External Sources (PDF, Word, PowerPoint, Markdown, Web, Git, Images) → Synapse Composer (Acquire, Extract, Interpret, Resolve, Review, Publish) → Immutable OKF Release → Synapse AK Compiler (Validate, Compile, Package, Manifest) → AKP → Synapse AIR / Domain Products

---

# 6. Primary Users and Actors

- **Domain author**: Provides source material and authors domain knowledge.
- **Knowledge curator**: Reviews duplication, terminology, source authority, contradictions, and publication quality.
- **Knowledge architect**: Defines ontology, OKF profiles, validation rules, namespaces, and knowledge architecture.
- **Reviewer**: Approves or rejects proposed changes within a defined area of responsibility.
- **Product owner**: Owns the intended purpose and quality of the resulting AKP.
- **Composition automation**: Submits sources, refreshes URLs, starts workflows, or requests recompilation.
- **Synapse AK Compiler**: Consumes immutable OKF releases and produces AKP artifacts.

---

# 7. Functional Requirements

## 7.1 Source acquisition

Register sources, preserve identity, detect duplicates, store metadata, record authority/trust/security/licensing, acquire via pluggable connectors, calculate fingerprints, retain immutable copies.

## 7.2 Extraction

Select extractor by type/policy, support multiple providers, preserve structure, produce diagnostics, assign confidence, preserve anchors, support OCR escalation, produce Canonical Document.

## 7.3 Semantic interpretation

Identify candidates, distinguish explicit/inferred, associate evidence, produce typed outputs, record versions, reject invalid outputs.

## 7.4 Knowledge resolution

Determine if candidate: creates new, extends existing, creates alias, supplies evidence, conflicts, supersedes, requires narrowing, duplicates, is irrelevant, or requires review.

## 7.5 Review

Generate items, rank by materiality, display evidence, record decisions, apply deterministically, reuse decisions, preserve audit trail.

## 7.6 OKF authoring

Create/update files, maintain identifiers/references/provenance, support namespaces, human-readable diffs, validate structure, prevent unreviewed objects in releases.

## 7.7 Release management

Create immutable releases, produce manifests/reports, record versions, produce summaries, track approval, invoke compilation, store results.

## 7.8 Incremental recomposition

Detect changes, identify affected blocks/candidates/objects, re-run impacted stages, propose revisions, preserve unaffected knowledge, produce new releases.

---

# 8. Non-Functional Requirements

- **Reliability**: Idempotent activities, resumable jobs, restart-safe state.
- **Auditability**: Every transformation records inputs, outputs, actor, timestamp, tool version, config, rationale, lineage.
- **Portability**: OKF usable without Composer.
- **Security**: Classification propagation, secret detection, model routing policies, access restrictions.
- **Performance**: Seconds to start extraction, observable progress, parallel processing, incremental updates.
- **Scalability**: Single-user to multi-user, thousands of sources, horizontal scaling.
- **Testability**: Explicit contracts for every component.
- **Explainability**: Every proposal exposes evidence, rules, confidence, affected objects, suggested action.

---

# 9. Deployment Profiles

## 9.1 Local profile

Python 3.12+, FastAPI, Typer CLI, Pydantic v2, DuckDB, SQLite/DuckDB workflow, local filesystem, Git OKF, Docling, LanceDB vectors, NetworkX graph, local/remote models.

## 9.2 Enterprise profile

Containerized Python, FastAPI, PostgreSQL, object storage, Temporal workflows, managed Git, pgvector/Qdrant, PostgreSQL/Neo4j graph, enterprise identity, Purview, OpenTelemetry.

## 9.3 Hybrid profile

Local acquisition/parsing/sensitive sources, sync approved content, managed review/release, local or enterprise compilation. Same domain contracts across all profiles.

---

# 10–44. Detailed Design

The remaining sections (10-44) cover: Logical Architecture, Component Design (API, Workspace, Source Registry, Connectors, Extraction Router, Providers), Canonical Document Model, Extraction Quality, Visual Interpretation, Model Gateway, Semantic Interpretation, Knowledge Resolution, Search/Candidate Generation, Graph Model, Vector Index, Provenance Model, Authority/Trust, Temporal/Scope, Review System, Knowledge Commit Service, OKF Repository, Validation Architecture, Durable Workflow, Specialist Agents, Security, Observability, Error Model, Concurrency, Incremental Recomposition, Compiler Integration, Release Model, Evaluation Framework, Testing Strategy, Code Structure, 6 Delivery Slices, 40 ADR Backlog items, 10 Open Decisions, 15 Acceptance Criteria, and the Final Architecture Statement.

---

# 40. Initial Delivery Slices

## Slice 1: Canonical ingestion
Workspace, Source Registry, local-file connector, Markdown connector, Docling extractor, Canonical Document Model, extraction diagnostics, DuckDB state.

## Slice 2: Candidate knowledge extraction
Model Gateway, typed interpretation contracts, concept/definition/claim/evidence candidates, provenance validation.

## Slice 3: Existing-knowledge resolution
Git-backed OKF repository, full-text search, vector candidate generation, graph projection, create/extend/alias/evidence proposals.

## Slice 4: Human review and commit
Review queue, decision model, Commit Service, Git commits, validation.

## Slice 5: Release and compile
Immutable release model, manifest, compiler adapter, compilation status, artifact checksum.

## Slice 6: Rich formats and incremental updates
DOCX/PPTX/PDF enrichment, visual interpretation, URL acquisition, source change detection, impact-based recomposition.

---

# 44. Final Architecture Statement

Synapse Composer is designed as a knowledge-engineering system rather than a document-conversion pipeline.

Its architecture establishes three stable boundaries:

- **Canonical Document Model** defines what the Composer observed.
- **OKF Knowledge Model** defines what the Composer knows.
- **Immutable Compiler Contract** defines what the Composer can publish.

Everything between these boundaries—parsers, OCR engines, language models, multimodal models, vector stores, graph projections, and workflow engines—remains replaceable.
