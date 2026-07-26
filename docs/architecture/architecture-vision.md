# Synapse Knowledge Platform — AKP Architecture Vision

> **Status:** Draft · v0.2
> **Owner:** Patrik Löwendahl
> **Last updated:** 2026-07-26
> **Standard:** Follows IEEE 1471 / ISO 42010 structure

---

## 1. Purpose & Scope

This document defines the architectural vision for the **Synapse Knowledge Platform**
with focus on the **Agentic Knowledge Package (AKP)** product line. AKP is the
compiled knowledge subsystem within the broader Synapse platform. It provides the
authoring, compilation, packaging, runtime, and distribution boundaries required to
serve governed knowledge to Synapse AIR and other applications.

### 1.1 In Scope

| Concern | Covered |
|---|---|
| OKF authoring contract (Markdown + YAML) | ✅ |
| AKP compiler pipeline and package assembly | ✅ |
| Compiled package structure and portability | ✅ |
| AKP Runtime retrieval contract | ✅ |
| AKP Registry distribution boundary | ✅ |
| SDK and local author workflow | ✅ |
| Explorer as compiled-pack visualization consumer | ✅ |
| Governance, provenance, composition, immutability | ✅ |

### 1.2 Out of Scope

- Planning and execution orchestration
- Agent frameworks and agent behaviors
- Domain application UX
- Business process automation
- Model training or fine-tuning
- Final answer synthesis

AKP does **not** own planners, execution engines, agents, or applications. Those
responsibilities belong to **Synapse AIR** and downstream product surfaces.

---

## 2. Stakeholders & Concerns

| Stakeholder | Key Concerns |
|---|---|
| **Knowledge Author** | Human-readable source format, reviewability, stable IDs |
| **Knowledge Engineer** | Deterministic compilation, ontology integrity, package quality |
| **Runtime Engineer** | Stable retrieval contract, composition, caching, observability |
| **Security / Compliance** | Object-level governance, provenance, immutability, revocation |
| **Application Developer** | Portable APIs, model-neutral consumption, predictable results |
| **Platform Engineer** | Registry workflows, signature verification, promotion between environments |
| **Leadership / Product Owner** | Explainability, reuse, trustworthy decision support |

---

## 3. Architectural Drivers

### 3.1 Quality Attributes

| Attribute | Target | Rationale |
|---|---|---|
| **Portability** | Packages run across local, embedded, service, and cloud deployments | Knowledge should move without rewrite |
| **Governability** | Policies and classifications survive compilation and retrieval | Enterprise trust and compliance |
| **Explainability** | Every returned object includes provenance and package identity | Evidence-grounded reasoning |
| **Composability** | Packages can be loaded independently or as a governed graph | Multi-domain intelligence scenarios |
| **Reproducibility** | Same inputs produce semantically equivalent outputs | CI/CD trust and auditability |
| **Immutability** | Released package versions are never overwritten | Safe caching, rollback, and verification |
| **Performance** | Sub-second retrieval for common runtime operations | Interactive agent loops |

### 3.2 Constraints

1. **Compiled artifact boundary** — authored OKF and deployed AKP remain separate products.
2. **Runtime neutrality** — public package and retrieval contracts cannot depend on one runtime.
3. **Model neutrality** — packages cannot require one LLM provider or embedding model.
4. **Human-authored source** — canonical knowledge remains Git-friendly Markdown with YAML metadata.
5. **Object-level governance** — protection must survive chunking, indexing, retrieval, and composition.
6. **Product boundary clarity** — AKP retrieves and serves knowledge; AIR plans and executes.

### 3.3 Principles

1. **Knowledge as code** — author, review, test, version, publish.
2. **Compile meaning, not files** — normalize knowledge into deployable machine representations.
3. **Preserve provenance** — source lineage survives every transformation.
4. **Prefer explicit knowledge** — authored content outranks inferred content.
5. **Governance is monotonic** — retrieval must not weaken protection.
6. **Keep logical and physical boundaries separate** — capabilities remain portable even when implementations differ.

---

## 4. Architectural Views

### 4.1 Context View

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                    Synapse Knowledge Platform Context                       │
│                                                                              │
│  Human / Machine Authors                                                     │
│            │                                                                 │
│            ▼                                                                 │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐  │
│  │     OKF      │──▶│ AKP Compiler │──▶│     AKP      │──▶│ AKP Runtime  │──┼──▶ Synapse AIR ──▶ Applications
│  │  MD + YAML   │   │  13+ stages  │   │ compiled pkg │   │ retrieval    │  │
│  └──────────────┘   └──────┬───────┘   └──────┬───────┘   └──────┬───────┘  │
│                             │                    │                    │        │
│                             ▼                    ▼                    ▼        │
│                      Ontology + Rules      AKP Registry         Explorer / SDK │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Boundary statement:**
- **AKP owns** knowledge packaging, runtime retrieval, governance metadata, provenance, and distribution.
- **AKP does not own** intent understanding, planning, execution, agent memory, or application behavior.

### 4.2 Functional View — Compiler Pipeline

```text
Discover
  → Parse
  → Normalize
  → Validate
  → Graph Build
  → Rules / Conflict Checks
  → Dependency / Cross-pack Resolution
  → Retrieval Corpus Build
  → Keyword Index Build
  → Vector Build or Vector Inputs
  → Governance Propagation
  → Package Assembly
  → Build Report
  → Signing / Publish
```

**Pipeline stages:**

| # | Stage | Responsibility | State |
|---|---|---|---|
| 1 | **Discover** | Find OKF sources, pack metadata, ontology, rules, dependencies | Current |
| 2 | **Parse** | Extract frontmatter, semantic units, authored relationships | Current |
| 3 | **Normalize** | Normalize identifiers, terms, references, metadata | Current |
| 4 | **Validate** | Enforce ontology, required fields, referential integrity | Current |
| 5 | **Graph Build** | Compile canonical graph from objects and relationships | Current |
| 6 | **Rules / Conflict Checks** | Apply pack rules, detect ambiguity and contradictions | Current |
| 7 | **Dependency / Cross-pack** | Resolve inter-pack references and version compatibility | Current |
| 8 | **Retrieval Corpus** | Produce retrieval units from semantic boundaries | Current |
| 9 | **Keyword Index** | Build deterministic lexical retrieval structures | Current |
| 10 | **Vector Build / Inputs** | Persist embeddings or embedding-ready inputs | Current / Evolving |
| 11 | **Governance Propagation** | Push object-level governance into all derived artifacts | Future |
| 12 | **Package Assembly** | Write manifest, objects, graph, retrieval, provenance, validation outputs | Current |
| 13 | **Build Report** | Emit quality metrics, unresolved references, coverage, diagnostics | Current |
| 14 | **Signing / Publish** | Sign package and publish to registry or file target | Future |

### 4.3 Information View — Package Contract

```text
package.akp
├── manifest.yaml
├── objects/
├── retrieval/
├── graph/
├── governance/
├── provenance/
├── validation/
└── signatures/
```

| Section | Purpose |
|---|---|
| `manifest.yaml` | Package identity, version, format, dependencies, capabilities |
| `objects/` | Canonical concepts, relationships, procedures, evidence, bindings |
| `retrieval/` | Corpus, keyword index, vectors, searchable metadata |
| `graph/` | Portable graph representation for traversal and expansion |
| `governance/` | Policies, classifications, object-level restrictions |
| `provenance/` | Lineage linking every derived object back to sources |
| `validation/` | Build report, coverage, diagnostics, quality signals |
| `signatures/` | Digest, signature, attestation, trust metadata |

### 4.4 Component View

| Component | Primary Role |
|---|---|
| **OKF** | Human-authored, machine-parseable knowledge source format |
| **AKP Compiler** | Deterministically transforms OKF into deployable packages |
| **AKP Runtime** | Loads, composes, filters, and serves knowledge via retrieval contract |
| **AKP Registry** | Stores, versions, verifies, and distributes package releases |
| **AKP SDK** | Scaffolding, local build, testing, validation, publish workflows |
| **Explorer** | Offline visualization of compiled package state |
| **Synapse AIR** | Consumes retrieval contract and performs planning / execution |

### 4.5 Deployment View

```text
                 ┌──────────────────────┐
                 │ Author / CI / SDK    │
                 │ compile, validate     │
                 └──────────┬───────────┘
                            │
                    ┌───────▼────────┐
                    │ Local Packages │
                    │ .duckdb / .akp │
                    └───┬────────┬───┘
                        │        │
          ┌─────────────▼──┐  ┌──▼──────────────┐
          │ Local MCP      │  │   AKP Registry  │
          │ Runtime        │  │ versions, trust │
          │ Python stdio   │  └──┬──────────────┘
          └───────┬────────┘     │
                  │              │
                  └──────┬───────┘
                         ▼
                 ┌───────────────┐
                 │ Synapse AIR   │
                 │ / local apps  │
                 └──────┬────────┘
                        ▼
                  End-user surfaces
```

**Key deployment properties:**
- Local development can load packages directly from the filesystem.
- The runtime surface is available over **Python SDK**, **local API**, **REST**, and **MCP**.
- Local MCP is the first deployment target for CSU-IQ-V2 integration.
- Registry-backed deployments add signature verification, promotion, deprecation, and revocation.

---

## 5. Cross-Cutting Concerns

### 5.1 Versioning & Immutability

- Package versions use semantic versioning.
- Released versions are treated as immutable artifacts.
- Format version, compiler version, ontology version, and embedding version remain distinct.

### 5.2 Governance & Security

- Governance metadata is attached to objects, not only package files.
- Composition applies the most restrictive effective policy.
- Production runtimes may reject revoked or untrusted packages.

### 5.3 Provenance & Explainability

- Retrieval results return package ID, version, object ID, and provenance chain.
- Generated and inferred content is distinguishable from authored content.
- Build outputs record source revision and transformation history.

### 5.4 Composition & Capability Resolution

- Packages may depend on other packages with explicit version constraints.
- Runtime composition resolves namespaces, retrieval scope, graph union, and policy intersection.
- Logical capabilities are declared in-package and mapped to implementations at deployment time.

### 5.5 Observability

- Compiler emits structured stage diagnostics and quality metrics.
- Runtime emits query observability, cache metrics, and provenance-aware retrieval traces.
- Registry records lineage, promotion, revocation, and trust events.

---

## 6. Key Decisions

Architectural decisions are recorded as ADRs in `docs/architecture/decisions/adr/`.

| ADR | Decision |
|---|---|
| ADR-001 | Stable IDs in frontmatter |
| ADR-002 | Formal shared ontology |
| ADR-003 | DuckDB as physical storage engine |
| ADR-004 | Two-pack topology (initial) |
| ADR-005 | Shared ontology with cross-pack references |
| ADR-006 | MCEM independence |
| ADR-007 | NetworkX as compiler graph tool |
| ADR-008 | Pydantic intermediate representation |
| ADR-009 | V1 compiler scope |
| ADR-010 | Compiler engineering principles |
| ADR-011 | Code standards and architecture conventions |
| ADR-012 | V2 compiler scope |
| ADR-013 | Ontology discovery mode |
| ADR-014 | Pack rules engine and outcome validation |
| ADR-015 | AKP runtime neutrality |
| ADR-016 | AKP model neutrality |
| ADR-017 | Object-level governance |
| ADR-018 | Provenance survives compilation |
| ADR-019 | No direct runtime mutation of packages |
| ADR-020 | Logical capabilities separated from implementations |
| ADR-021 | Hybrid retrieval support |
| ADR-022 | Portable package graph |
| ADR-023 | Immutable released package versions |
| ADR-024 | Inferred knowledge distinguishable from authored knowledge |

---

## 7. Roadmap & Evolution

### Current (v0.2)

- ✅ Clear separation of **OKF**, **Compiler**, **AKP**, **Runtime**, and **Registry**
- ✅ Compiled artifact boundary defined within the Synapse Knowledge Platform
- ✅ Retrieval contract defined for search, lookup, graph expansion, provenance, and policy-aware access
- ✅ Governance, provenance, portability, and composition established as first-class concerns

### Near-term

- [ ] Local MCP runtime for CSU-IQ-V2 context assembly
- [ ] Governance propagation through derived retrieval artifacts
- [ ] Package signing and trust verification
- [ ] Registry-backed promotion and revocation flows

### Future

- [ ] Self-describing `.akp` container format beyond single-file `.duckdb`
- [ ] Multi-environment registry channels and dependency resolution
- [ ] Expanded SDK workflows for tests, publish, and release governance
- [ ] Broader deployment adapters while preserving the stable public contract

---

## Appendix A — Glossary

| Term | Definition |
|---|---|
| **OKF** | Open Knowledge Format, the authoring/source representation |
| **AKP** | Agentic Knowledge Package, the compiled deployable knowledge artifact |
| **AKP Runtime** | The package-serving runtime that implements the retrieval contract |
| **AKP Registry** | The store and distribution boundary for versioned package releases |
| **AIR** | Synapse intelligence runtime responsible for intent, planning, and execution |
| **Logical capability** | A portable capability identifier resolved to an implementation at deployment |
| **Governance propagation** | Carrying restrictions from sources into all derived artifacts |
