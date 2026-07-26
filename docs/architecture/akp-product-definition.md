# Agentic Knowledge Package

## Product and Architecture Definition

**Acronym:** AKP
**Name:** Agentic Knowledge Package
**Product family:** Synapse Knowledge Platform
**Status:** Architecture definition
**Primary architecture standard:** ISO/IEC/IEEE 42010
**Normative language:** RFC 2119 terminology

---

# 1. Definition

An **Agentic Knowledge Package**, or **AKP**, is a portable, versioned, governed and machine-consumable package of domain knowledge designed for use by agentic intelligence systems.

An AKP transforms human-authored and machine-derived knowledge into a compiled artifact that can be:

* validated
* signed
* distributed
* deployed
* retrieved
* reasoned over
* governed
* audited
* upgraded
* reused across applications

An AKP is not merely a collection of documents.

It is a compiled representation of knowledge containing the semantic, structural, procedural and governance information required for an intelligence runtime to use that knowledge reliably.

The core idea is:

> Knowledge should be built, tested, versioned and deployed with the same discipline as software.

---

# 2. Purpose

The purpose of AKP is to make institutional and domain knowledge portable and operationally usable without embedding that knowledge directly into prompts, application code or proprietary databases.

An AKP provides a stable boundary between:

* knowledge authorship
* knowledge compilation
* knowledge deployment
* intelligence execution
* domain applications

This allows knowledge to be created once and reused by multiple applications and runtimes.

For example:

```text
Forecast-Doctrine.akp
```

may be used by:

* Forecast
* CSU-IQ
* a strategic planning assistant
* an acquisition analysis application
* a risk intelligence application

The knowledge package remains the same even when the application, model, runtime or deployment environment changes.

---

# 3. Architectural Role

AKP is the compiled artifact of the Synapse Knowledge Platform.

```text
Human and machine-authored knowledge
                │
                ▼
              OKF
      Open Knowledge Format
                │
                ▼
          AKP Compiler
                │
                ▼
              AKP
   Agentic Knowledge Package
                │
        ┌───────┴────────┐
        ▼                ▼
   AKP Registry      Direct deploy
        │                │
        └───────┬────────┘
                ▼
          AKP Runtime
                │
                ▼
        Retrieval contract
                │
                ▼
          Synapse AIR
                │
                ▼
       Domain applications
```

AKP sits between the authored knowledge format and the runtime that consumes knowledge.

---

# 4. Core Product Principle

An AKP is analogous to a deployable software artifact.

Useful analogies include:

* a NuGet package for knowledge
* a JAR file for knowledge
* a container image for knowledge
* a compiled semantic module
* a governed domain knowledge distribution

The analogy is not exact.

Unlike a traditional software package, an AKP contains representations intended for both deterministic and probabilistic consumption.

These may include:

* formal concepts
* natural-language explanations
* semantic relationships
* retrieval units
* embeddings
* procedures
* evidence
* policies
* source provenance

---

# 5. Goals

AKP SHALL enable the following outcomes.

## 5.1 Portability

A package SHALL be deployable across supported environments without rewriting its source knowledge.

Possible targets include:

* local workstation
* desktop application
* container
* private cloud
* public cloud
* Azure AI Foundry
* embedded runtime
* shared enterprise service

## 5.2 Reusability

Knowledge SHALL be reusable across:

* applications
* agents
* planners
* models
* users
* business units
* deployment environments

## 5.3 Governability

Every material knowledge object SHALL retain sufficient metadata to support:

* ownership
* classification
* authorization
* lineage
* retention
* geographic restrictions
* distribution restrictions
* audit

## 5.4 Explainability

Knowledge returned from an AKP SHALL retain traceability to its origin.

The runtime must be able to identify:

* which package supplied the knowledge
* which package version was used
* which source object produced it
* how it was transformed
* what governance restrictions apply

## 5.5 Deterministic compilation

Given the same:

* source content
* compiler version
* build configuration
* dependency versions

the compiler SHOULD produce semantically equivalent package output.

Where binary reproducibility is practical, the compiler SHOULD support reproducible builds.

## 5.6 Extensibility

AKP SHALL support future representations without breaking the stable external contract.

## 5.7 Independence from a specific model

AKP SHALL NOT depend on one LLM provider, embedding model or agent framework.

---

# 6. Non-Goals

AKP is not intended to be:

* a general-purpose document format
* a replacement for a content management system
* a replacement for SharePoint, Confluence or a wiki
* a vector database
* a graph database
* an agent framework
* an orchestration engine
* a workflow engine
* a business application
* a model-training format
* a universal ontology standard
* a proprietary prompt library
* an unstructured ZIP file of documents

AKP does not plan or execute business tasks.

That responsibility belongs to an intelligence runtime such as Synapse AIR.

---

# 7. Relationship Between OKF and AKP

## 7.1 OKF

The **Open Knowledge Format** is the authoring and interchange representation.

OKF is optimized for:

* humans
* source control
* review
* collaboration
* modularity
* diffing
* machine parsing
* compilation

OKF may use Markdown, YAML, JSON or other defined source formats.

## 7.2 AKP

AKP is the compiled and deployable artifact.

It is optimized for:

* runtime loading
* efficient retrieval
* dependency resolution
* semantic lookup
* policy enforcement
* integrity validation
* distribution
* versioning

The relationship is:

```text
OKF is source.

AKP is build output.
```

Applications SHOULD NOT depend directly on the internal source structure of an OKF repository.

Applications and runtimes SHOULD consume the stable AKP contract.

---

# 8. Knowledge Types

An AKP may contain several forms of knowledge.

## 8.1 Declarative knowledge

Declarative knowledge describes what is true or believed to be true within the domain.

Examples:

* definitions
* concepts
* principles
* policies
* doctrines
* taxonomies
* business rules
* metric definitions
* strategic positions

Example:

```yaml
concept:
  id: csu.unified-delivery-coverage
  name: Unified Delivery Coverage
  definition: >
    The proportion of contracted delivery demand covered
    by committed delivery capacity.
```

## 8.2 Relational knowledge

Relational knowledge describes how concepts are connected.

Examples:

* depends on
* causes
* measures
* contributes to
* contradicts
* supports
* part of
* owned by
* applies to

This representation forms the basis of the package knowledge graph.

## 8.3 Procedural knowledge

Procedural knowledge describes how an outcome should be produced.

Examples:

* analysis procedures
* calculation recipes
* diagnostic methods
* decision playbooks
* tool-use instructions
* validation procedures
* escalation patterns

Procedural knowledge is knowledge about how to act, but the AKP does not itself execute the procedure.

AIR or another runtime interprets and executes it.

## 8.4 Semantic knowledge

Semantic knowledge connects business concepts to technical representations.

Examples:

* a KPI to a semantic-model measure
* a concept to a database field
* a business term to an API property
* an ontology node to a graph query
* a metric to a DAX calculation

## 8.5 Evidential knowledge

Evidential knowledge captures material that supports or challenges claims.

Examples:

* research
* citations
* observations
* benchmarks
* historical cases
* measured results
* confidence assessments

## 8.6 Narrative knowledge

Narrative knowledge explains domain concepts in prose and may include:

* articles
* interpretations
* examples
* contextual explanations
* position papers
* strategic narratives

## 8.7 Constraint knowledge

Constraint knowledge defines:

* prohibited actions
* required conditions
* scope restrictions
* regulatory limits
* business invariants
* decision thresholds

## 8.8 Tool and capability knowledge

An AKP may describe logical capabilities available to an intelligence runtime.

Example:

```yaml
capability:
  id: csu.metrics.delivery-coverage.query
  purpose: Retrieve delivery coverage for a defined scope.
  inputs:
    - portfolio
    - customer
    - period
  outputs:
    - coverage
    - covered_hours
    - committed_hours
```

The package defines the logical capability.

It SHOULD NOT contain environment-specific credentials or hard-coded service endpoints.

---

# 9. Package Composition

An AKP is composed of logical layers.

```text
AKP
├── Manifest
├── Identity
├── Dependencies
├── Domain model
├── Concepts
├── Relationships
├── Procedures
├── Semantic bindings
├── Retrieval corpus
├── Embedding indexes
├── Evidence and provenance
├── Governance metadata
├── Policies
├── Validation reports
└── Signatures
```

Not every package must contain every representation.

A doctrine package may have no tool bindings.

A semantic package may contain mappings but limited narrative content.

The manifest SHALL state which package capabilities and sections are present.

---

# 10. Package Manifest

Every AKP SHALL contain a manifest.

The manifest is the authoritative package descriptor.

A conceptual manifest may include:

```yaml
akp:
  id: synapse.forecast.doctrines
  name: Forecast Doctrines
  version: 1.4.0
  format_version: 1.0
  description: >
    Strategic foresight doctrines used by Forecast.

  publisher:
    id: synapse
    name: Synapse

  domain:
    id: strategic-foresight
    name: Strategic Foresight

  build:
    compiler: synapse-akp-compiler
    compiler_version: 0.7.0
    timestamp: 2026-07-26T10:00:00Z
    source_revision: 86ac019

  dependencies:
    - package: synapse.forecast.core
      version: "^1.2.0"

  capabilities:
    concepts: true
    graph: true
    retrieval: true
    procedures: true
    embeddings: true
    semantic_bindings: false

  governance:
    default_classification: internal
    owner: strategy-office
    external_distribution: prohibited

  integrity:
    digest: sha256:...
    signature: signatures/package.sig
```

---

# 11. Package Identity

Each package SHALL have a globally stable logical identity.

Recommended form:

```text
<publisher>.<domain>.<package>
```

Examples:

```text
synapse.forecast.core
synapse.forecast.doctrines
synapse.forecast.mental-models
synapse.csu.mcem
synapse.csu.metrics
synapse.sweden.market-context
```

Identity and version together identify a package release.

```text
synapse.forecast.doctrines@1.4.0
```

A package name SHALL NOT be reused for unrelated knowledge.

---

# 12. Versioning

AKP SHOULD use semantic versioning.

```text
MAJOR.MINOR.PATCH
```

## Major version

Incremented for incompatible changes such as:

* removed public concepts
* changed concept meaning
* incompatible schema changes
* renamed public capabilities
* altered package contracts

## Minor version

Incremented for compatible additions such as:

* new concepts
* new procedures
* additional evidence
* new optional bindings
* expanded retrieval content

## Patch version

Incremented for compatible corrections such as:

* typo corrections
* metadata fixes
* improved descriptions
* provenance corrections
* non-semantic index rebuilds

A package may independently expose:

* package version
* AKP format version
* compiler version
* ontology version
* embedding-model version

These SHALL NOT be conflated.

---

# 13. Dependency Model

An AKP may depend on other AKPs.

Example:

```text
Forecast-Industry-Technology.akp
             │
             ├── Forecast-Core.akp
             ├── Forecast-Doctrines.akp
             └── Technology-Ontology.akp
```

Dependencies SHALL be explicitly declared.

The compiler or runtime SHALL detect:

* missing dependencies
* incompatible versions
* dependency cycles
* duplicate concept definitions
* conflicting semantic bindings
* incompatible governance constraints

Dependencies SHALL NOT silently weaken governance.

The effective governance of composed knowledge SHALL be at least as restrictive as the most restrictive applicable source.

---

# 14. Package Classes

AKP may support several package classes.

## 14.1 Core domain package

Defines the central ontology and language of a domain.

Example:

```text
Forecast-Core.akp
```

## 14.2 Doctrine package

Defines principles, positions and interpretive rules.

Example:

```text
Forecast-Doctrines.akp
```

## 14.3 Mental-model package

Defines reusable models for reasoning.

Examples:

* systems thinking
* second-order effects
* diffusion theory
* disruption models
* dynamic capabilities

## 14.4 Procedure package

Defines repeatable analytical or operational methods.

Example:

```text
Forecast-Horizon-Scanning.akp
```

## 14.5 Semantic package

Maps domain concepts to data systems.

Example:

```text
CSU-Semantic-Model.akp
```

## 14.6 Localization package

Extends a core package with geography, language or organizational context.

Examples:

```text
CSU-Sweden.akp
CSU-Belgium.akp
```

## 14.7 Evidence package

Contains curated evidence and citations for a specific topic.

## 14.8 Policy package

Defines governance, compliance or operational restrictions.

A package may combine classes, but narrow packages SHOULD be preferred when reuse and independent versioning are valuable.

---

# 15. Internal Representations

An AKP may include multiple compiled representations of the same source knowledge.

This is intentional.

Different runtime operations require different structures.

## 15.1 Canonical object store

Contains normalized knowledge objects such as:

* concepts
* definitions
* procedures
* claims
* evidence
* bindings
* policies

This is the semantic source of truth inside the package.

## 15.2 Retrieval corpus

Contains runtime-optimized retrieval units.

These may include:

* chunks
* summaries
* questions
* aliases
* synthetic descriptions
* searchable metadata

Retrieval units SHALL retain references to their canonical source objects.

## 15.3 Knowledge graph

Contains nodes and relationships compiled from canonical objects.

The graph supports:

* concept navigation
* dependency analysis
* evidence traversal
* causal reasoning
* scope expansion
* ontology resolution

The embedded graph representation SHALL NOT require Neo4j specifically.

The package may use an interoperable internal representation that can be loaded into:

* in-memory graph libraries
* Neo4j
* NetworkX
* Kùzu
* other supported graph engines

## 15.4 Vector representation

Contains embeddings or data required to build an embedding index.

AKP may support two modes:

### Precomputed embeddings

The package contains vectors produced during compilation.

Benefits:

* predictable deployment
* faster startup
* consistent retrieval behavior

Risks:

* embedding-model lock-in
* larger package size
* model lifecycle coupling

### Runtime-generated embeddings

The package contains retrieval content but vectors are generated at deployment.

Benefits:

* deployment-specific model choice
* smaller package
* easier model upgrades

Risks:

* variable retrieval behavior
* deployment cost
* delayed startup

The final mode SHALL be declared in the manifest.

## 15.5 Keyword index

A package may contain a lexical or full-text index for deterministic retrieval.

## 15.6 Semantic bindings

Bindings connect knowledge to external schemas and capabilities.

Examples:

```yaml
binding:
  concept: csu.customer
  target:
    type: dataverse.entity
    logical_name: account
```

or:

```yaml
binding:
  metric: csu.unified-delivery-coverage
  target:
    type: powerbi.measure
    logical_capability: csu.metrics.udc.query
```

Bindings SHOULD reference logical identifiers rather than environment-specific endpoints.

---

# 16. Source Provenance

Every material knowledge object SHALL retain provenance.

Minimum provenance SHOULD include:

* source identifier
* source type
* source location
* source version or revision
* author or publisher where known
* ingestion timestamp
* transformation history
* compiler build
* package version

Example:

```yaml
provenance:
  source_id: mcaps-mcem-guide
  source_type: document
  source_revision: "2026.2"
  publisher: Microsoft
  ingested_at: 2026-07-20T08:31:00Z
  transformations:
    - normalize-markdown
    - extract-concepts
    - resolve-cross-references
```

Generated content SHALL be identified as generated.

Inferred relationships SHALL be distinguished from explicitly authored relationships.

---

# 17. Governance Model

Governance is part of the knowledge object, not merely a property of the package file.

## 17.1 Governance inheritance

Governance SHALL propagate from source to:

* canonical objects
* chunks
* graph nodes
* graph edges
* embeddings
* summaries
* procedures
* evidence
* responses derived from the knowledge

## 17.2 Governance properties

Possible properties include:

* sensitivity
* classification
* owner
* steward
* audience
* legal basis
* geographic restriction
* retention
* external-sharing restriction
* citation restriction
* verbatim-output restriction
* model-use restriction
* human-review requirement

## 17.3 Monotonic protection principle

> Knowledge SHALL NOT become less protected merely because it has been compiled, embedded, retrieved, combined, summarized or transformed.

## 17.4 Purview integration

Microsoft Purview may act as a governance provider for:

* classification
* labels
* ownership
* lineage
* retention
* audit
* DLP

AKP governance SHALL remain provider-neutral.

Purview is one implementation of the governance provider contract.

## 17.5 Runtime enforcement

The AKP Runtime SHALL expose governance metadata alongside retrieved content.

The consuming runtime SHALL evaluate access before providing knowledge to planners, models or users.

---

# 18. Security

## 18.1 Package integrity

An AKP SHOULD support:

* cryptographic digest
* publisher signature
* compiler attestation
* dependency verification
* tamper detection

## 18.2 Package confidentiality

Sensitive packages SHOULD support encryption:

* at rest
* during distribution
* in registry storage
* in runtime cache

## 18.3 Trust levels

A runtime may classify packages as:

* trusted
* verified
* unverified
* blocked

Production environments SHOULD reject packages that fail required trust policies.

## 18.4 Secrets

AKPs SHALL NOT contain:

* passwords
* client secrets
* access tokens
* personal credentials
* environment-specific private keys

Packages may declare secret requirements by logical name.

Example:

```yaml
requires:
  secrets:
    - capability.csu.crm.read
```

The deployment environment resolves those requirements.

---

# 19. Compilation Lifecycle

The AKP compiler transforms source knowledge into a deployable package.

```text
Discover
   │
   ▼
Ingest
   │
   ▼
Normalize
   │
   ▼
Validate source
   │
   ▼
Resolve identity
   │
   ▼
Extract and compile semantics
   │
   ▼
Build graph
   │
   ▼
Build retrieval corpus
   │
   ▼
Generate embeddings or embedding inputs
   │
   ▼
Apply governance
   │
   ▼
Resolve dependencies
   │
   ▼
Validate package
   │
   ▼
Sign
   │
   ▼
Publish
```

---

# 20. Compiler Responsibilities

The compiler SHALL be responsible for the following.

## 20.1 Source discovery

Identify declared source files and imported dependencies.

## 20.2 Parsing

Parse supported OKF content into an intermediate representation.

## 20.3 Normalization

Normalize:

* identifiers
* terminology
* references
* metadata
* dates
* relationship types
* source paths

## 20.4 Semantic validation

Validate:

* unique identifiers
* known relation types
* required definitions
* valid references
* ontology consistency
* dependency compatibility

## 20.5 Conflict detection

Detect conflicts such as:

* two incompatible definitions of the same concept
* contradictory binding ownership
* inconsistent units
* duplicate public identifiers
* incompatible governance rules

The compiler SHOULD fail closed for material ambiguity.

## 20.6 Enrichment

The compiler may generate:

* aliases
* retrieval questions
* chunk summaries
* inferred relationships
* embeddings
* quality scores

Generated enrichments SHALL be traceable and distinguishable from authored content.

## 20.7 Graph compilation

Create the package graph from concepts and relationships.

## 20.8 Retrieval compilation

Produce retrieval units based on semantic boundaries rather than arbitrary fixed-length splitting alone.

## 20.9 Governance propagation

Apply and validate governance metadata at object level.

## 20.10 Package assembly

Produce the final package and manifest.

## 20.11 Build report

Emit a build report containing:

* warnings
* errors
* quality metrics
* unresolved references
* package contents
* dependency tree
* governance coverage
* provenance coverage
* retrieval statistics

---

# 21. Compilation Principles

## 21.1 Compile meaning, not files

The compiler should not merely package source files.

It should produce a normalized knowledge model.

## 21.2 Preserve the source

The compiler SHALL preserve references to original source material.

Where permitted, source snapshots may also be included.

## 21.3 Prefer explicit knowledge

Authored definitions and relationships take precedence over model-inferred interpretations.

## 21.4 Inference must be visible

Machine-inferred objects SHALL include:

* inference method
* model
* confidence
* source objects
* timestamp

## 21.5 Do not hide ambiguity

Ambiguous concepts SHOULD produce warnings or required review rather than being silently resolved.

## 21.6 Deterministic identifiers

Compiled object identifiers SHOULD be stable across builds when the underlying semantic object has not changed.

## 21.7 Separate source changes from index changes

A rebuild using a different embedding model SHOULD NOT appear as a semantic knowledge change unless the underlying knowledge changed.

---

# 22. Validation

An AKP SHALL pass defined validation before publication.

Validation levels may include:

## Level 1: Structural

* manifest valid
* required sections present
* schema valid
* files readable

## Level 2: Referential

* references resolve
* dependencies resolve
* identifiers are unique

## Level 3: Semantic

* concept definitions valid
* relationship types allowed
* units consistent
* required metadata present

## Level 4: Governance

* classification coverage
* owner coverage
* prohibited content checks
* policy conflicts

## Level 5: Retrieval

* expected questions retrieve expected objects
* no inaccessible object leaks through indexes
* relevance thresholds achieved

## Level 6: Domain acceptance

* reviewed by domain owner
* approved by steward
* scenario tests passed

A package may declare its achieved validation level.

---

# 23. Testing

AKPs SHOULD support knowledge tests.

## 23.1 Retrieval tests

Example:

```yaml
test:
  question: What is Unified Delivery Coverage?
  expected:
    concepts:
      - csu.unified-delivery-coverage
```

## 23.2 Relationship tests

Example:

```yaml
test:
  assertion:
    from: csu.udc
    relation: leading-indicator-of
    to: csu.contract-burn-rate
```

## 23.3 Policy tests

Example:

```yaml
test:
  actor: external-user
  request: retrieve confidential doctrine
  expected: denied
```

## 23.4 Semantic binding tests

Validate that logical bindings resolve to compatible runtime capabilities.

## 23.5 Regression tests

Package upgrades SHOULD be tested against known questions and reasoning scenarios.

---

# 24. Deployment

AKPs are deployed into an AKP Runtime.

A deployment may include:

* one package
* multiple packages
* domain overlays
* localization packages
* organization-specific extensions

Example:

```text
Forecast deployment
├── Forecast-Core.akp
├── Forecast-Doctrines.akp
├── Forecast-Mental-Models.akp
├── Technology-Industry.akp
└── Microsoft-Strategy.akp
```

The runtime SHALL resolve the final composed knowledge space.

---

# 25. Composition

Multiple AKPs may be composed at runtime.

Composition involves:

* dependency resolution
* namespace assembly
* graph union
* retrieval federation
* policy intersection
* binding resolution
* precedence rules

## 25.1 Extension over duplication

A regional or organizational package SHOULD extend a shared core package rather than duplicate it.

Example:

```text
CSU-Core.akp
     │
     ├── CSU-Sweden.akp
     └── CSU-Belgium.akp
```

## 25.2 Overlay rules

An overlay may:

* add concepts
* add examples
* add evidence
* add local terminology
* add semantic bindings
* increase restrictions

An overlay SHALL NOT silently redefine a public concept with incompatible meaning.

Material redefinition requires a new identifier or major version.

## 25.3 Conflict resolution

Conflict resolution SHALL be explicit.

Possible strategies include:

* reject
* prefer more specific package
* prefer declared overlay
* preserve both with scope
* require human resolution

The selected strategy SHALL be declared in deployment configuration.

---

# 26. AKP Runtime

The AKP Runtime loads, composes and serves knowledge packages.

Its responsibilities include:

* package loading
* signature verification
* dependency resolution
* graph initialization
* retrieval initialization
* authorization filtering
* policy evaluation
* caching
* provenance return
* query observability

The AKP Runtime is not the same as AIR.

```text
AKP Runtime:
Find and serve governed knowledge.

AIR:
Understand intent, plan and execute.
```

---

# 27. Retrieval Contract

The runtime SHALL expose a stable retrieval contract independent of internal storage technology.

It may support operations such as:

```text
search
lookup concept
expand graph
retrieve procedure
retrieve evidence
resolve terminology
resolve capability
get provenance
evaluate policy
```

A conceptual request:

```json
{
  "operation": "search",
  "query": "What is changing our confidence in this prediction?",
  "scope": {
    "packages": ["synapse.forecast.*"]
  },
  "actor": {
    "id": "user-123"
  },
  "limit": 10
}
```

A conceptual result:

```json
{
  "results": [
    {
      "object_id": "forecast.prediction-confidence-update",
      "package": "synapse.forecast.methods",
      "version": "1.2.0",
      "content": "...",
      "score": 0.91,
      "provenance": [...],
      "governance": {
        "classification": "internal"
      }
    }
  ]
}
```

The contract SHOULD be available over:

* Python SDK
* local API
* REST
* MCP

---

# 28. Retrieval Strategy

Retrieval SHOULD be hybrid.

Possible modes include:

* exact identifier lookup
* lexical search
* semantic vector search
* graph traversal
* metadata filtering
* structured query
* procedure lookup
* capability lookup

AIR or the consuming application may request a specific retrieval mode.

The AKP Runtime may also combine modes.

Example:

```text
Semantic search
      +
Graph expansion
      +
Governance filter
      +
Source ranking
      =
Context set
```

---

# 29. Context Assembly Boundary

AKP Runtime retrieves candidate knowledge.

AIR performs broader context assembly.

This boundary is important.

AKP Runtime MAY:

* retrieve related concepts
* expand graph neighborhoods
* rank evidence
* return procedures

AKP Runtime SHOULD NOT:

* determine the complete user intent
* create an execution plan
* call arbitrary business systems
* choose business actions
* synthesize the final answer

Those are AIR responsibilities.

---

# 30. Capability Resolution

AKPs may define logical capability requirements.

Example:

```text
csu.metrics.delivery-coverage.query
```

A deployment maps this to an implementation.

Sweden may map it to:

```text
Power BI dataset A
```

Belgium may map it to:

```text
Fabric semantic model B
```

The package and AIR plan remain portable because neither depends on the concrete endpoint.

---

# 31. Memory Boundary

AKP represents curated and distributable knowledge.

It is not the same as runtime memory.

## AKP contains

* approved knowledge
* packaged evidence
* reusable procedures
* stable semantic models
* governed doctrine

## Runtime memory contains

* conversation state
* execution history
* temporary observations
* user preferences
* procedural learning
* outcomes

Validated runtime learning may later be promoted into an OKF source and compiled into a new AKP version.

Runtime memory SHALL NOT silently mutate a published AKP.

---

# 32. Learning and Promotion

The recommended knowledge-learning flow is:

```text
Observation
    │
    ▼
Runtime memory
    │
    ▼
Candidate knowledge
    │
    ▼
Human or governed review
    │
    ▼
OKF source update
    │
    ▼
AKP compile
    │
    ▼
New package version
```

This maintains accountability and prevents uncontrolled self-modification.

---

# 33. Registry

An AKP Registry stores and distributes package versions.

The registry may support:

* publish
* retrieve
* list versions
* resolve dependencies
* verify signatures
* deprecate
* revoke
* promote between environments
* record lineage
* manage channels

Possible channels:

* development
* preview
* approved
* production
* deprecated
* revoked

A package registry SHOULD maintain immutable released versions.

---

# 34. Package Lifecycle

```text
Draft
  │
  ▼
Compiled
  │
  ▼
Validated
  │
  ▼
Reviewed
  │
  ▼
Signed
  │
  ▼
Published
  │
  ▼
Deployed
  │
  ▼
Observed
  │
  ├── Updated
  ├── Deprecated
  └── Revoked
```

## Revocation

A package version may be revoked due to:

* incorrect knowledge
* leaked sensitive content
* invalid license
* compromised signature
* unsafe procedure
* material governance violation

Runtimes SHOULD support package revocation checks for centrally managed deployments.

---

# 35. Technology Direction

The AKP architecture SHALL remain technology-neutral at its public boundary.

The initial implementation may use the following technologies.

## Primary language

Python

## Authoring

* Markdown
* YAML
* JSON
* Git

## Validation

* Pydantic
* JSON Schema
* custom semantic validators

## Tabular and local analytical storage

* DuckDB
* Parquet
* Apache Arrow

## Graph

Initial:

* portable graph representation
* NetworkX or Kùzu for local compilation and testing

Potential enterprise target:

* Neo4j

The package contract SHALL not require Neo4j.

## Vector storage

Candidate technologies:

* LanceDB
* Qdrant
* pgvector
* Azure AI Search

Final selection remains an architectural decision.

## Object storage

* local file system
* Azure Blob Storage
* compatible object storage

## Distribution

* OCI-compatible artifacts
* private package registry
* Azure storage-backed registry

Whether AKP adopts OCI as its formal distribution standard remains an open decision.

## Interfaces

* Python SDK
* REST
* MCP

## Security and governance

* Microsoft Entra ID
* Microsoft Purview
* managed identities
* cryptographic package signing

---

# 36. Package Format Direction

The package SHOULD be a self-describing artifact.

A conceptual physical layout:

```text
package.akp
├── manifest.yaml
├── objects/
│   ├── concepts.parquet
│   ├── relationships.parquet
│   ├── procedures.parquet
│   ├── evidence.parquet
│   └── bindings.parquet
├── retrieval/
│   ├── corpus.parquet
│   ├── keyword-index/
│   └── vectors/
├── graph/
│   └── graph.parquet
├── governance/
│   ├── policies.yaml
│   └── classifications.parquet
├── provenance/
│   └── lineage.parquet
├── validation/
│   └── build-report.json
└── signatures/
    └── package.sig
```

This is illustrative rather than final.

The logical contract is more important than the physical serialization.

---

# 37. Architecture Decisions

## ADR-AKP-001: Knowledge SHALL be packaged as a compiled artifact

**Status:** Accepted

Knowledge will not be consumed solely as loose files or prompt content.

**Rationale:**

* portability
* consistency
* versioning
* governance
* testing
* distribution

---

## ADR-AKP-002: OKF and AKP SHALL be separate

**Status:** Accepted

OKF is the editable source representation.

AKP is the immutable deployment artifact.

---

## ADR-AKP-003: AKP SHALL remain runtime-neutral

**Status:** Accepted

AKP must be usable by Synapse AIR and potentially by other compatible runtimes.

---

## ADR-AKP-004: AKP SHALL remain model-neutral

**Status:** Accepted

No package may require one proprietary LLM provider as part of its core contract.

---

## ADR-AKP-005: Governance SHALL be object-level

**Status:** Accepted

Package-level classification is insufficient.

Governance must propagate to chunks, vectors, graph objects and evidence.

---

## ADR-AKP-006: Provenance SHALL survive compilation

**Status:** Accepted

All runtime material must be traceable to package and source.

---

## ADR-AKP-007: Runtime learning SHALL NOT directly mutate packages

**Status:** Accepted

Knowledge changes must pass through source, review and compilation.

---

## ADR-AKP-008: Logical capabilities SHALL be separated from implementations

**Status:** Accepted

Packages define capability contracts, not environment-specific endpoints.

---

## ADR-AKP-009: Hybrid retrieval SHALL be supported

**Status:** Accepted

Vector retrieval alone is insufficient.

---

## ADR-AKP-010: The package graph SHALL be portable

**Status:** Accepted

Neo4j may be a deployment option but not a package-format dependency.

---

## ADR-AKP-011: Released package versions SHOULD be immutable

**Status:** Accepted

Corrections result in new package versions.

---

## ADR-AKP-012: Inferred knowledge SHALL be distinguishable from authored knowledge

**Status:** Accepted

Machine enrichment must retain method, confidence and provenance.

---

# 38. Open Decisions

The following matters require dedicated ADRs.

## Storage and format

* exact physical AKP container format
* whether to use OCI artifacts
* compression strategy
* incremental package layers
* large binary handling

## Embeddings

* precomputed versus deployment-generated vectors
* default embedding model
* support for multiple vector representations
* embedding compatibility metadata

## Vector engine

* LanceDB
* Qdrant
* pgvector
* Azure AI Search
* pluggable strategy

## Graph engine

* embedded Kùzu
* NetworkX for development
* Neo4j for shared enterprise deployment
* graph serialization format

## Registry

* build custom registry
* use OCI registry
* use Azure artifacts or blob-backed registry
* dependency-resolution protocol

## Signing

* signature format
* certificate authority
* organizational trust model
* package revocation mechanism

## Licensing

* licensing metadata
* redistribution restrictions
* source-content license propagation

## Test standards

* minimum test suite for production packages
* retrieval quality thresholds
* governance validation requirements

## Schema evolution

* forward and backward compatibility rules
* extension namespaces
* migration mechanism

---

# 39. Quality Attributes

Under ISO/IEC/IEEE 42010, the following quality concerns drive the AKP architecture.

## Portability

Packages can move between deployment environments.

## Interoperability

Packages can be consumed through stable contracts.

## Modifiability

Source knowledge can evolve without changing applications.

## Auditability

Knowledge use can be traced.

## Security

Sensitive knowledge is protected throughout its lifecycle.

## Reliability

Packages are validated before use.

## Performance

Runtime representations support efficient retrieval.

## Explainability

Retrieved content retains provenance and semantic context.

## Maintainability

Package structure, dependencies and ownership remain explicit.

## Scalability

The architecture supports both small local packages and large enterprise knowledge estates.

---

# 40. Stakeholders

## Knowledge authors

Need accessible authoring and clear validation.

## Domain experts

Need semantic accuracy and reviewability.

## Knowledge engineers

Need structured compilation and tooling.

## Application developers

Need a stable retrieval contract.

## Runtime engineers

Need efficient, portable representations.

## Security and compliance teams

Need classification, lineage and enforcement.

## Enterprise architects

Need clear boundaries and interoperability.

## Product owners

Need reusable knowledge assets.

## End users

Need trustworthy, explainable outcomes.

---

# 41. Success Criteria

AKP succeeds when:

* knowledge is authored independently of application code
* the same package can be reused by multiple applications
* package upgrades do not require application rewrites
* knowledge can be tested before release
* retrieved knowledge can be traced to its source
* governance persists through retrieval and generation
* local and cloud deployments use the same package
* domain packages can extend shared core packages
* runtime technologies can change without changing package meaning
* institutional knowledge becomes a managed product rather than unstructured content

---

# 42. Example: Forecast

A Forecast deployment may use:

```text
Forecast-Core.akp
Forecast-Doctrines.akp
Forecast-Mental-Models.akp
Forecast-Horizon-Scanning.akp
Forecast-Technology.akp
Organization-Strategy.akp
```

These packages define:

* what a signal is
* what distinguishes a weak signal from noise
* how signals relate to trends
* how evidence changes trend confidence
* how predictions are formed
* how predictions are challenged
* what doctrines guide interpretation
* which mental models should be considered
* how strategic implications are expressed

Forecast provides the application and strategic-intelligence domain experience.

AIR provides planning and execution.

AKP provides the knowledge substrate.

---

# 43. Example: CSU-IQ

A CSU-IQ deployment may use:

```text
CSU-Core.akp
MCEM.akp
CSU-Metrics.akp
CSU-Procedures.akp
CSU-Semantic-Model.akp
CSU-Sweden.akp
```

These packages define:

* customer-success terminology
* MCEM
* role responsibilities
* KPI definitions
* metric relationships
* analytical procedures
* semantic-model mappings
* country-specific context

The same core packages can be reused across markets.

Only localization and binding packages need to change.

---

# 44. Final Product Definition

An Agentic Knowledge Package is:

> A portable, versioned, governed and machine-consumable compilation of domain knowledge, semantics, procedures, evidence and policy, designed to provide stable and explainable knowledge services to agentic intelligence runtimes and applications.

Its defining properties are:

* compiled
* portable
* composable
* versioned
* governed
* traceable
* testable
* runtime-neutral
* model-neutral
* reusable

The fundamental architectural separation is:

```text
OKF authors knowledge.

AKP packages knowledge.

AKP Runtime serves knowledge.

AIR applies knowledge.

Applications provide business purpose.
```

AKP is therefore the reusable knowledge substrate of the Synapse ecosystem.
