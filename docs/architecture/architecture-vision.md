# Synapse Agentic Knowledge Pack — Architecture Vision

> **Status:** Draft · v0.1
> **Owner:** Patrik Löwendahl
> **Last updated:** 2026-07-26
> **Standard:** Loosely follows IEEE 1471 / ISO 42010 structure

---

## 1. Purpose & Scope

This document defines the architectural vision for **Synapse AKP** — a
compiler and runtime that transforms curated Markdown knowledge sources into
immutable, versioned **knowledge packs** that power agentic reasoning, retrieval,
and evidence-grounded decision support.

### 1.1 In Scope

| Concern | Covered |
|---|---|
| Knowledge-pack compilation pipeline | ✅ |
| OKF v0.2 canonical source format | ✅ |
| Physical storage engine (DuckDB) | ✅ |
| Cross-pack reference resolution | ✅ |
| Ontology-driven validation & enrichment | ✅ |
| 3-D interactive exploration (explorer) | ✅ |
| Agentic retrieval interface (future) | ✅ |
| Domain corpus content authoring guidance | ✅ |

### 1.2 Out of Scope

- Chat / conversational UI (consumer responsibility)
- LLM fine-tuning or model training
- Hosting infrastructure and deployment topology

---

## 2. Stakeholders & Concerns

| Stakeholder | Key Concerns |
|---|---|
| **Knowledge Architect** | Ontology fidelity, relationship completeness, zero duplication |
| **Domain Expert** | Accuracy of domain concepts, evidence traceability |
| **Agent Developer** | Deterministic retrieval, grounded citations, structured access |
| **Platform Engineer** | Build reproducibility, immutable artifacts, CI integration |
| **Leadership** | Trustworthy decision-support, auditability, governance |

---

## 3. Architectural Drivers

### 3.1 Quality Attributes

| Attribute | Target | Rationale |
|---|---|---|
| **Reproducibility** | Identical input → identical pack (bit-level) | Auditability, CI/CD trust |
| **Immutability** | Compiled packs are read-only versioned artifacts | No runtime drift; cache-safe |
| **Composability** | Packs can be loaded independently or together | Multi-domain agents pick subsets |
| **Traceability** | Every fact links back to a canonical source section | Evidence-grounded reasoning |
| **Extensibility** | New concept types via ontology, not code changes | Domain teams self-serve |
| **Performance** | Sub-second retrieval for 10K+ concepts | Real-time agentic loops |

### 3.2 Constraints

1. **Single-file output** — each pack compiles to one DuckDB file for portability.
2. **No runtime dependencies** — packs are self-contained; consumers need only a DuckDB driver.
3. **Human-readable sources** — canonical knowledge lives in Markdown with YAML frontmatter.
4. **Deterministic pipeline** — no non-deterministic enrichment in the core compile path.

### 3.3 Principles

1. **Knowledge as code** — version-controlled, reviewed, tested, released.
2. **Ontology-first** — the shared ontology is the contract between authors and consumers.
3. **Compile-time correctness** — catch errors at build, not at query time.
4. **Evidence over opinion** — every assertion traces to a source system or document.
5. **Agentic by design** — structures optimized for machine retrieval, not just human browsing.

---

## 4. Architectural Views

### 4.1 Context View

```
┌──────────────────────────────────────────────────────┐
│                   Synapse AKP                        │
│                                                      │
│  ┌──────────┐   ┌───────────┐   ┌────────────────┐  │
│  │ Canonical │──▶│ Compiler  │──▶│ Knowledge Pack │  │
│  │ Sources   │   │ Pipeline  │   │ (.duckdb)      │  │
│  │ (MD+YAML) │   └───────────┘   └───────┬────────┘  │
│  └──────────┘         │                  │           │
│       ▲               │                  ▼           │
│       │          ┌────┴─────┐    ┌──────────────┐   │
│  Domain SMEs     │ Ontology │    │  Consumers   │   │
│  & Architects    │ + Rules  │    │  (Agents,    │   │
│                  └──────────┘    │   Explorer)  │   │
│                                  └──────────────┘   │
└──────────────────────────────────────────────────────┘
```

### 4.2 Functional View — Compiler Pipeline

```
Source MD ──▶ Parse ──▶ Validate ──▶ Graph Build ──▶ Enrich ──▶ Write DuckDB
                │           │            │              │
                ▼           ▼            ▼              ▼
           Frontmatter  Ontology     NetworkX       BM25 index
           extraction   conformance  (nodes/edges)  Semantic units
                                                    Cross-pack refs
```

**Pipeline stages (in order):**

| # | Stage | Responsibility |
|---|---|---|
| 1 | **Parse** | Extract frontmatter, heading tree, semantic units from Markdown |
| 2 | **Validate** | Check ontology conformance, required fields, relationship targets |
| 3 | **Graph** | Build a directed graph (NetworkX) from objects + relationships |
| 4 | **Rules** | Apply pack-rules.yaml (cardinality, naming, required predicates) |
| 5 | **Cross-pack** | Resolve inter-pack references against dependency packs |
| 6 | **BM25** | Tokenize and build BM25 search index |
| 7 | **Write** | Serialize to DuckDB with canonical schema |

### 4.3 Information View — DuckDB Schema

| Table | Purpose |
|---|---|
| `manifest` | Pack metadata: id, version, compiled_at, ontology hash |
| `objects` | Canonical concepts: id, title, type, domain, description |
| `edges` | Intra-pack relationships: subject → predicate → object |
| `cross_pack_refs` | Inter-pack references with predicate and resolution status |
| `semantic_units` | Heading-scoped content chunks for retrieval |
| `aliases` | Alternate names / acronyms mapped to canonical IDs |
| `bm25_tokens` | Pre-tokenized BM25 index for keyword search |
| `vector_metadata` | Embedding coordinates for semantic search (optional) |

### 4.4 Deployment View

```
                    ┌─────────────────┐
                    │  CI / Local CLI  │
                    │  kp compile ...  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  .duckdb files  │
                    │  (immutable)    │
                    └───┬─────────┬───┘
                        │         │
               ┌────────▼──┐  ┌──▼──────────┐
               │  Agent     │  │  Explorer   │
               │  Runtime   │  │  (3-D HTML) │
               │  (DuckDB   │  │             │
               │   driver)  │  │             │
               └────────────┘  └─────────────┘
```

**Key deployment properties:**
- Packs are **portable files** — copy to any machine with a DuckDB driver.
- No server process required; consumer opens the file directly.
- Explorer is a **self-contained HTML** file (vendor JS inlined).

---

## 5. Cross-Cutting Concerns

### 5.1 Versioning

- Packs carry a `version` field in their manifest (semver).
- Source changes produce a new pack version; old versions remain immutable.
- `pack.yaml` in each knowledge base root declares the canonical version.

### 5.2 Extensibility

- **New concept types** — add to `ontology.yaml`; no compiler code changes needed.
- **New predicates** — extend the ontology predicate list; compiler validates automatically.
- **New packs** — create a directory with `pack.yaml` + Markdown sources; compile.
- **New rules** — add to `pack-rules.yaml`; the rules engine enforces at compile time.

### 5.3 Observability

- Compiler emits structured logs per stage with timing and counts.
- Explorer shows node/edge/pack statistics in the header bar.
- Pack manifest stores compile timestamp and source hashes for provenance.

### 5.4 Security & Trust

- Packs are **read-only artifacts** — no mutation after compilation.
- Source content is reviewed via standard PR workflows (knowledge as code).
- No secrets or PII stored in packs; content is organizational knowledge only.

---

## 6. Key Decisions

Architectural decisions are recorded as ADRs in `docs/architecture/decisions/`.

| ADR | Decision |
|---|---|
| ADR-001 | Stable IDs in frontmatter (human-authored, not generated) |
| ADR-002 | Formal shared ontology (YAML, single source of truth) |
| ADR-003 | DuckDB as physical storage engine |
| ADR-004 | Two-pack topology (CSU + MCEM initially) |
| ADR-005 | Shared ontology with cross-pack references |
| ADR-006 | MCEM independence (no CSU dependency) |
| ADR-007 | NetworkX for in-memory graph construction |
| ADR-008 | Pydantic intermediate representation |
| ADR-009 | V1 compiler scope |
| ADR-010 | Engineering principles (determinism, reproducibility) |
| ADR-011 | Code standards and architecture conventions |
| ADR-012 | V2 compiler scope (BM25, enrichment, cross-pack) |
| ADR-013 | Ontology discovery (auto-detect types/predicates) |
| ADR-014 | Pack rules engine (cardinality, naming, required predicates) |

---

## 7. Roadmap & Evolution

### Current (v0.2)

- ✅ Multi-stage compiler pipeline with validation
- ✅ Cross-pack reference resolution with bidirectional linking
- ✅ BM25 keyword search index
- ✅ 3-D explorer with galaxy nebulae visualization
- ✅ `pack.yaml` auto-discovery and dependency resolution

### Near-term (v0.3)

- [ ] Agentic retrieval API (structured query interface for agents)
- [ ] Embedding-based semantic search (vector index in pack)
- [ ] Dynamic knowledge packs (live data sources at query time)
- [ ] Delta compilation (incremental rebuilds)

### Future

- [ ] Pack federation (query across distributed packs without co-location)
- [ ] Provenance chains (trace from agent answer → semantic unit → source commit)
- [ ] Multi-tenant pack registry (versioned distribution)

---

## Appendix A — Glossary

| Term | Definition |
|---|---|
| **Knowledge Pack** | An immutable DuckDB file containing compiled domain knowledge |
| **Canonical Source** | A Markdown file with YAML frontmatter that defines one concept |
| **Ontology** | YAML schema defining valid concept types and predicates |
| **Semantic Unit** | A heading-scoped content chunk within a canonical source |
| **Cross-pack Ref** | A relationship whose target lives in a different pack |
| **Pack Rules** | Compile-time constraints (cardinality, naming, required links) |
| **OKF** | Open Knowledge Format — the specification governing source layout |
