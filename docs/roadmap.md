# AKP Roadmap

This roadmap sequences the Synapse AKP product from local runtime integration to
full package distribution and developer experience. The immediate consumer is the
**CSU-IQ-V2 context assembler**, which will call the AKP Runtime locally through MCP.

---

## Phase 1: Local MCP Runtime (MVP) — Target: 2 weeks

### Goal

Deliver a local AKP Runtime that CSU-IQ-V2 can call over MCP to retrieve governed
compiled knowledge from the local filesystem.

### Deliverables

- AKP Runtime implemented as a local **Python MCP server** using **stdio** transport
- Runtime operations:
  - `search`
  - `lookup_concept`
  - `expand_graph`
  - `get_provenance`
- Direct loading of compiled `.duckdb` packs from local file paths
- Hybrid retrieval combining **BM25 + vector + graph expansion**
- Provenance returned with every result
- MCP integration path for the **CSU-IQ-V2 context assembler**

### Success Criteria

- CSU-IQ-V2 can connect to the MCP server locally without custom adapters
- Runtime can load one or more local `.duckdb` packs deterministically
- `search`, `lookup_concept`, `expand_graph`, and `get_provenance` return correct results with provenance
- Hybrid retrieval improves over lexical-only retrieval for known validation questions
- Local runtime startup and query loop are fast enough for interactive context assembly

### Dependencies

- Stable local pack schema in current `.duckdb` format
- Existing compiler outputs for at least one usable knowledge pack
- MCP contract definition for CSU-IQ-V2 integration
- BM25, vector, and graph access in the runtime implementation

---

## Phase 2: Governance + Provenance — Target: 2 weeks after P1

### Goal

Enforce object-level governance and strengthen explainability at runtime and build time.

### Deliverables

- Governance propagation across retrieval units, graph nodes, and derived artifacts
- Runtime policy evaluation and authorization filtering
- Expanded provenance chains for derived and inferred objects
- Validation coverage for governance completeness and provenance completeness
- Initial signing and trust metadata design

### Success Criteria

- Retrieved content never bypasses the most restrictive applicable policy
- Every result includes package, object, and source lineage metadata
- Governance and provenance validation failures block release-ready builds
- Runtime responses expose enough metadata for downstream explanation and audit

### Dependencies

- Phase 1 runtime contract
- Compiler support for governance propagation metadata
- Canonical provenance schema
- Security and compliance input on minimum policy fields

---

## Phase 3: Package Format Evolution (.akp container) — Target: 4 weeks after P2

### Goal

Move from implementation-centric storage toward a self-describing portable package container.

### Deliverables

- Defined `.akp` container layout
- Manifest, objects, retrieval, graph, governance, provenance, validation, and signatures sections
- Packaging and unpacking tooling
- Backward-compatible loading strategy for existing `.duckdb` packages
- Format versioning and schema migration guidance

### Success Criteria

- A runtime can load either legacy `.duckdb` or new `.akp` packages through one stable contract
- Package contents are inspectable without runtime-specific assumptions
- Package signing and validation can operate over the container boundary
- Format evolution does not break existing consuming applications

### Dependencies

- Phase 2 governance and provenance schemas
- Finalized manifest contract
- Decisions on physical serialization and packaging mechanics

---

## Phase 4: Registry + Distribution — Target: 6 weeks after P3

### Goal

Introduce controlled publication, version distribution, promotion, and revocation for AKP releases.

### Deliverables

- AKP Registry service or registry-backed distribution layer
- Publish, retrieve, list versions, dependency resolution, and trust verification flows
- Promotion channels such as development, preview, approved, production, deprecated, and revoked
- Revocation handling for centrally managed runtimes
- Registry lineage and package release audit history

### Success Criteria

- Packages can be published once and retrieved by version without overwrite
- Production runtimes can verify trust and reject revoked packages
- Dependency resolution works across approved package graphs
- Promotion between environments is visible and auditable

### Dependencies

- Phase 3 package container and signing approach
- Storage and identity decisions for registry implementation
- Environment promotion workflow and trust policy definitions

---

## Phase 5: SDK + Developer Experience — Target: ongoing

### Goal

Make AKP authoring, validation, testing, and release workflows fast and repeatable for package developers.

### Deliverables

- Project scaffolding and templates
- Local compile and validate commands
- Knowledge tests for retrieval, relationships, and policy behavior
- Publish workflow integrated with runtime and registry
- Developer documentation and examples

### Success Criteria

- New package authors can scaffold and compile a pack quickly
- Local validation catches most release-blocking issues before publication
- Tests become a standard pre-publish step
- SDK commands track the stable AKP format version

### Dependencies

- Stable compiler and runtime contracts
- Package format decisions from Phase 3
- Registry workflows from Phase 4 for end-to-end publish experience
