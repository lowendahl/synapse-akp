# Synapse Composer

## Product and Architecture Vision

**Status:** Product and architecture vision
**Product family:** Synapse Agentic Knowledge Platform
**Primary output:** Open Knowledge Format Wiki
**Downstream target:** Agentic Knowledge Pack compilation
**Working category:** Agentic knowledge engineering and composition environment

---

## 1. Executive Vision

Synapse Composer is the knowledge engineering environment for the Synapse AKP framework.

It transforms heterogeneous source material—PDF documents, Microsoft Word files, Markdown, PowerPoint presentations, web pages, and manually authored knowledge—into a coherent, governed, evidence-backed OKF Wiki that can be compiled into an Agentic Knowledge Pack.

The product exists to solve a fundamental problem:

> Enterprise knowledge is stored as documents, but agents require structured, contextualized, traceable knowledge.

Documents preserve what people wrote. They do not consistently preserve what an agent needs to understand:

* Which concepts are being described
* How concepts relate to each other
* Which statements are authoritative
* What evidence supports a claim
* Whether information is descriptive, normative, procedural, or speculative
* Where contradictions or gaps exist
* Who may use the knowledge
* When the knowledge is valid
* How it should influence reasoning and action

Synapse Composer bridges this gap.

It does not merely convert files into Markdown or divide documents into chunks. It interprets source material, proposes a knowledge structure, maintains provenance, involves human authors in material decisions, and produces a machine-compilable knowledge system.

The resulting pipeline is:

```text
Documents, URLs and human input
            ↓
      Synapse Composer
            ↓
    Governed OKF Wiki
            ↓
       Synapse AK
      AKP Compiler
            ↓
 Agentic Knowledge Pack
            ↓
Local, Foundry IQ or MCP deployment
            ↓
Context assembly, planning and reasoning
```

---

# 2. Product Thesis

## 2.1 From ingestion to composition

Most knowledge ingestion systems follow a pipeline resembling:

```text
Extract → Chunk → Embed → Retrieve
```

This is useful for document search, but it does not produce a reliable knowledge product.

Synapse Composer instead follows:

```text
Acquire
→ Parse
→ Interpret
→ Decompose
→ Model
→ Reconcile
→ Curate
→ Validate
→ Publish
```

The distinction is intentional.

**Ingestion** moves content into a system.

**Composition** transforms content into an internally coherent body of knowledge.

A composer must therefore be able to answer questions such as:

* Does this source introduce a new concept?
* Is it another description of an existing concept?
* Does it provide evidence for an existing claim?
* Does it supersede or contradict previous guidance?
* Is the content a principle, policy, process, example, metric, definition, or decision?
* Which parts are authoritative, and which are interpretation?
* Which relationships should become graph edges?
* Which content belongs in the core wiki and which should remain source evidence?
* What requires human judgment before publication?

Synapse Composer is therefore not a file converter. It is an **agentic knowledge composition system**.

---

# 3. Product Purpose

Synapse Composer enables domain experts, architects, strategists, product teams, and knowledge engineers to create high-quality Agentic Knowledge Packs without manually constructing every OKF object.

Its purpose is to make knowledge packs:

* Easier to author
* Faster to update
* Structurally consistent
* Traceable to original sources
* Reviewable by humans
* Suitable for machine reasoning
* Governable across their lifecycle
* Recompilable as source material evolves

The Composer becomes the authoring and maintenance plane of Synapse AK.

Synapse AK remains responsible for defining, compiling, validating, packaging, and deploying knowledge packs.

The Composer is responsible for turning raw information into a valid and intentionally designed OKF knowledge space.

---

# 4. Product Positioning

## 4.1 Product category

Synapse Composer belongs to a new product category:

> **Agentic Knowledge Engineering Environment**

It combines capabilities normally spread across:

* Document ingestion tools
* Content management systems
* Wiki platforms
* Knowledge graphs
* Ontology editors
* AI-assisted authoring tools
* Data provenance systems
* Retrieval preparation pipelines
* Human review workflows

The product is not intended to replace all these systems. It provides the composition layer needed to turn their content into knowledge that agentic systems can use.

---

## 4.2 Product relationship within Synapse

```text
┌─────────────────────────────────────────────────────────────┐
│                    Synapse Product Family                   │
├─────────────────────────────────────────────────────────────┤
│ Synapse Composer                                            │
│ Acquires, interprets, structures and curates knowledge      │
├─────────────────────────────────────────────────────────────┤
│ Synapse AK                                                  │
│ Defines OKF, validates and compiles Agentic Knowledge Packs │
├─────────────────────────────────────────────────────────────┤
│ Synapse AIR                                                 │
│ Assembles context, plans, reasons and executes              │
├─────────────────────────────────────────────────────────────┤
│ Domain Products                                             │
│ CSU-IQ, Forecast and future intelligence applications       │
└─────────────────────────────────────────────────────────────┘
```

The separation protects the integrity of each concern:

* Composer creates and maintains knowledge.
* AK compiles and serves knowledge products.
* AIR consumes knowledge in support of reasoning and execution.
* Domain products provide purpose, workflows and user experiences.

---

# 5. Target Users

## 5.1 Domain author

A subject-matter expert who understands the domain but does not want to manually create graph structures, manifests, identifiers, provenance records, or semantic metadata.

The Composer helps the author turn existing material into structured knowledge.

## 5.2 Knowledge curator

A person responsible for quality, coherence, deduplication, source authority, terminology, and publication readiness.

The curator resolves uncertainty and governs the knowledge space.

## 5.3 Knowledge architect

A person who defines the ontology, conceptual model, information architecture, composition rules, validation policies, and compilation profile.

## 5.4 Product or system owner

A person accountable for the resulting AKP and the behavior it enables in downstream systems.

## 5.5 Reviewer or approver

A stakeholder who validates specific sections, policies, claims, or releases without needing to understand the underlying technical representation.

## 5.6 Automation agent

A machine actor that submits new sources, proposes updates, identifies contradictions, or initiates recompilation through APIs or event-driven workflows.

---

# 6. Core User Outcomes

A user should be able to:

1. Create a new OKF Wiki from a collection of mixed source formats.
2. Add new sources to an existing wiki without rebuilding it from scratch.
3. see what the Composer extracted, inferred, changed, merged, or rejected.
4. Trace every material knowledge assertion back to its source.
5. Review uncertainty, contradictions, missing evidence, and low-confidence mappings.
6. Correct the proposed structure using natural-language or structured editing.
7. Define which sources are authoritative for particular subjects.
8. Publish a validated OKF release.
9. Compile the release into an AKP.
10. Compare the new AKP with the previous release before deployment.
11. Continuously maintain the knowledge as sources evolve.

---

# 7. Experience Vision

## 7.1 The Composer workspace

The primary experience is a knowledge composition workspace rather than a conventional document editor.

The workspace contains five synchronized perspectives:

### Source view

Shows original files, pages, slides, sections, URLs, images, tables, and extraction results.

### Wiki view

Shows the human-readable OKF Wiki as a navigable body of knowledge.

### Model view

Shows concepts, relations, evidence, claims, policies, procedures, entities, and semantic models.

### Review view

Shows unresolved questions, conflicts, proposed merges, low-confidence interpretations, orphaned content, and validation failures.

### Release view

Shows compilation readiness, change impact, policy compliance, package versioning, and deployment targets.

Selecting an element in any view highlights its corresponding representation in the others.

For example:

```text
PowerPoint slide
      ↕
Extracted statement
      ↕
OKF wiki paragraph
      ↕
Concept or claim
      ↕
Evidence relationship
      ↕
Compiled AKP object
```

This creates an inspectable chain from source material to runtime knowledge.

---

## 7.2 Composition conversation

The Composer should support a conversational interface in addition to structured editing.

Examples:

* “Create a concept for Unified Delivery Coverage.”
* “This section is guidance, not policy.”
* “Treat the FY27 objectives as authoritative until June 30, 2027.”
* “Merge these two definitions but retain both source citations.”
* “Show me claims supported only by this presentation.”
* “What changed when I added the new quarterly focus document?”
* “Do not include customer-specific examples in the generic AKP.”
* “Reorganize this around sensing, seizing and transforming.”
* “Explain why these two sources conflict.”
* “Prepare this release for compilation.”

The conversation does not bypass the underlying model. Every accepted instruction must become an explicit, auditable change to the OKF workspace.

---

# 8. Core Product Capabilities

## 8.1 Multi-format source acquisition

The Composer accepts:

* PDF
* Microsoft Word
* Markdown
* PowerPoint
* HTML and web URLs
* Plain text
* Structured JSON or YAML
* Existing OKF repositories
* Existing AKP source projects
* Images containing meaningful text or diagrams
* Manual knowledge entered through the Composer
* API-submitted content

Each source is registered as a first-class object with:

* Stable source identity
* Content fingerprint
* Source type
* Original location
* Acquisition time
* Publication date where known
* Author or publisher where known
* Security classification
* Licensing or usage constraints
* Version information
* Extraction status
* Trust and authority metadata

---

## 8.2 Format-aware parsing

Each format requires a specialized parser.

The goal is not merely to extract text, but to preserve relevant structure.

### PDF parsing

The parser should attempt to preserve:

* Reading order
* Headings
* Paragraphs
* Tables
* Figures
* Captions
* Footnotes
* Page references
* Multi-column layout
* Document metadata
* Scanned text through OCR where necessary

Complex document understanding benefits from explicit layout detection and separation of text, tables, figures, and other visual elements rather than treating the page as a flat character stream. Recent research also indicates that parser choice and preprocessing materially affect downstream question-answering performance.

### Word parsing

The parser should preserve:

* Heading hierarchy
* Lists
* Tables
* Comments
* Footnotes
* Cross-references
* Tracked changes where accessible
* Embedded media
* Document properties

### PowerPoint parsing

The parser should treat the presentation as more than slide text.

It should preserve:

* Slide order
* Titles
* Body content
* Speaker notes
* Shapes and visual groupings
* Tables
* Diagrams
* Charts
* Image captions
* Repeated templates
* Relationships implied spatially
* Section boundaries

A presentation may communicate meaning through composition rather than prose. The interpretation pipeline must therefore distinguish extraction from semantic interpretation.

### Markdown parsing

Markdown is treated as a semi-structured native input.

The parser preserves:

* Heading hierarchy
* Links
* Lists
* Code blocks
* Front matter
* Tables
* Embedded diagrams
* Explicit identifiers
* Existing metadata

### Web parsing

The web acquisition service should:

* Retrieve the specified page
* Capture publication and modification metadata where available
* Remove navigation and unrelated page furniture
* Preserve headings, tables, links, images, and citations
* Record the canonical URL
* Retain a content snapshot or hash
* Detect changes on later refresh
* Respect access, robots, licensing, and policy constraints

---

## 8.3 Source normalization

All parsers produce a common intermediate document representation.

This representation should retain:

* Source hierarchy
* Content blocks
* Block types
* Reading order
* Page, slide, or section anchors
* Tables and figures
* Links and references
* Extracted metadata
* Parser confidence
* Source-level access restrictions

The normalized representation becomes the stable boundary between format-specific extraction and knowledge composition.

A parser may be replaced without changing the higher-level composition process.

---

## 8.4 Semantic decomposition

The Composer decomposes normalized content into candidate knowledge objects.

Candidate types may include:

* Concept
* Definition
* Claim
* Principle
* Doctrine
* Mental model
* Policy
* Objective
* Key result
* Measure
* Signal
* Procedure
* Capability
* Role
* Responsibility
* Process
* Decision
* Constraint
* Risk
* Assumption
* Question
* Example
* Evidence
* Source
* Entity
* Relationship
* Semantic model
* Query pattern
* Tool description

The decomposition stage must distinguish between what the source explicitly says and what the Composer infers.

Every candidate receives:

* Candidate type
* Proposed title
* Proposed identifier
* Extracted content
* Source span
* Confidence
* Interpretation rationale
* Suggested relationships
* Publication status

---

## 8.5 Concept resolution

The Composer determines whether a candidate:

* Creates a new concept
* Extends an existing concept
* Provides another definition
* Supplies evidence
* Introduces an alias
* Contradicts existing knowledge
* Supersedes previous knowledge
* Belongs to another domain
* Should be rejected as irrelevant
* Requires human resolution

Concept resolution uses a combination of:

* Exact identifiers
* Names and aliases
* Lexical similarity
* Embedding similarity
* Graph neighbourhood
* Ontology constraints
* Source authority
* Domain rules
* Language-model interpretation
* Human decisions

The model should not silently merge ambiguous concepts.

Ambiguous matches become review items.

---

## 8.6 Wiki synthesis

Once accepted, knowledge objects are assembled into an OKF Wiki.

The wiki should be:

* Human-readable
* Machine-parseable
* Modular
* Version-controlled
* Addressable through stable identifiers
* Explicit about source provenance
* Compatible with AKP compilation
* Navigable through both hierarchy and graph relationships

The Composer may propose an initial wiki architecture based on:

* Source structure
* Domain ontology
* Existing templates
* Intended AKP profile
* User instructions
* Detected concept clusters

However, the final information architecture remains an intentional product decision rather than an accidental result of source ordering.

---

## 8.7 Evidence and provenance

Every material assertion should be traceable to one or more source fragments.

The provenance model should capture:

```text
Source
  → source version
    → source location
      → extracted block
        → interpretation
          → knowledge object
            → compiled AKP artifact
```

The model should distinguish:

* Direct quotation
* Paraphrase
* Summary
* Synthesis across sources
* Derived conclusion
* Human-authored addition
* Machine-proposed inference
* Revision of an earlier object

W3C PROV provides a useful conceptual model for representing entities, activities, agents, derivation, revision, quotation, and primary sources. Synapse does not need to expose raw PROV-O to every user, but its internal provenance model should be compatible with these ideas.

---

## 8.8 Contradiction and temporal resolution

Enterprise sources frequently disagree because they were:

* Created by different teams
* Written for different audiences
* Valid in different regions
* Produced at different times
* Intended as principles rather than rules
* Superseded without explicit retirement
* Describing current state versus target state

The Composer must not resolve all disagreement by selecting one statement.

It should model:

* Source authority
* Effective date
* Expiry date
* Scope
* Jurisdiction
* Audience
* Applicability
* Supersession
* Confidence
* Known contradiction

Possible outcomes include:

* One statement supersedes another.
* Both are valid under different scopes.
* One is official and the other explanatory.
* The conflict remains unresolved.
* A human-authored synthesis reconciles them.

---

## 8.9 Human review and approval

The Composer uses human attention where judgment has the highest value.

Review queues should prioritize:

* Low-confidence interpretations
* Potential concept merges
* Contradictions
* Unsupported claims
* Missing or weak provenance
* New policies or doctrines
* Content affecting agent behaviour
* Material changes since the last release
* Security or classification conflicts
* Objects failing ontology rules
* Information proposed for deletion

Users should not need to approve every extracted paragraph.

The objective is **review by exception**.

---

## 8.10 Validation and compilation readiness

Before publication, the Composer validates the OKF project against:

* OKF schema
* Required metadata
* Identifier rules
* Link integrity
* Ontology constraints
* Provenance requirements
* Evidence requirements
* Security policies
* Content lifecycle policies
* AKP target capabilities
* Domain-specific linting rules

Validation results are divided into:

* Errors blocking compilation
* Warnings requiring review
* Recommendations
* Informational observations

Compilation is performed by Synapse AK, not by the Composer’s semantic reasoning components.

The Composer invokes the compiler using an immutable OKF release.

---

## 8.11 Incremental maintenance

The Composer should support living knowledge rather than one-time ingestion.

When a source changes, the system should:

1. Acquire the new version.
2. Compare it with the previous version.
3. Identify changed source blocks.
4. Re-evaluate only affected interpretations.
5. Calculate impact on linked knowledge objects.
6. Propose additions, revisions, supersessions, or removals.
7. Route material changes for review.
8. Publish a new OKF release.
9. Trigger AKP recompilation where approved.

This avoids rebuilding the entire wiki and reduces unwanted drift.

---

# 9. Product Principles

## 9.1 Sources are evidence, not the knowledge model

A source document informs the wiki, but its structure does not automatically become the wiki structure.

## 9.2 Preserve before interpreting

The system must retain an immutable representation of what was acquired before applying semantic transformation.

## 9.3 Separate extraction from interpretation

Extracted content and interpreted knowledge must remain distinguishable.

## 9.4 No material assertion without provenance

An assertion without a source or explicit human authorship is incomplete.

## 9.5 Human judgment governs ambiguity

The model proposes; authorized humans decide where interpretation materially affects meaning or agent behaviour.

## 9.6 Stable identity over textual similarity

Concept identifiers must survive renaming, rewriting, and source changes.

## 9.7 Incremental rather than destructive composition

New sources should update the knowledge system through explicit changes, not opaque regeneration.

## 9.8 Compilation is deterministic

Given the same valid OKF release, compiler version, and target profile, Synapse AK should produce functionally equivalent AKP artifacts.

## 9.9 Runtime concerns must not leak into authoring

The wiki describes knowledge. Deployment adapters determine how that knowledge is indexed, embedded, stored, and served.

## 9.10 Trust must be inspectable

Users must be able to understand why the system created, changed, related, or rejected a knowledge object.

---

# 10. Architecture Vision

## 10.1 Architectural style

Synapse Composer should use a modular, pipeline-oriented, event-aware architecture with explicit boundaries between:

* Acquisition
* Extraction
* Normalization
* Interpretation
* Knowledge modelling
* Human review
* Publication
* Compilation

The architecture should support both:

* A local-first desktop or developer workflow
* A managed collaborative enterprise service

The same domain contracts should be used in both deployment models.

---

## 10.2 Architecture stakeholders and concerns

The architecture description follows the stakeholder-and-concern orientation of ISO/IEC/IEEE 42010, which defines requirements for expressing architecture descriptions across software, systems, enterprises, product lines, and related entities.

| Stakeholder         | Primary concerns                                       |
| ------------------- | ------------------------------------------------------ |
| Domain author       | Ease of authoring, explainability, review workload     |
| Knowledge curator   | Coherence, duplication, quality, source authority      |
| Knowledge architect | Ontology integrity, extensibility, schema control      |
| Security owner      | Access control, data leakage, classification           |
| Product owner       | Usability, adoption, time to value                     |
| AKP compiler owner  | Valid and deterministic compilation input              |
| AIR runtime owner   | Retrieval quality, context precision, stable contracts |
| Platform engineer   | Operability, scalability, observability                |
| Compliance owner    | Provenance, retention, licensing, auditability         |
| Developer           | APIs, extensibility, testability, local development    |

---

# 11. Logical Architecture

```text
┌──────────────────────────────────────────────────────────────┐
│                       Experience Layer                       │
│ Workspace │ Conversation │ Review Queue │ Release Management │
└──────────────────────────────┬───────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────┐
│                 Composition Orchestration Layer              │
│ Jobs │ Workflows │ Policies │ Human Tasks │ Change Impact    │
└──────────────────────────────┬───────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────┐
│                    Knowledge Services Layer                  │
│ Decomposition │ Resolution │ Synthesis │ Validation          │
│ Contradictions │ Provenance │ Ontology │ Semantic Enrichment │
└───────────────┬──────────────────────────────┬───────────────┘
                │                              │
┌───────────────▼──────────────┐ ┌────────────▼────────────────┐
│ Document Intelligence Layer │ │    OKF Authoring Domain      │
│ Parsers │ OCR │ Layout       │ │ Wiki │ Graph │ Evidence     │
│ Tables │ Figures │ Metadata  │ │ Claims │ Policies │ Releases│
└───────────────┬──────────────┘ └────────────┬────────────────┘
                │                              │
┌───────────────▼──────────────────────────────▼───────────────┐
│                        Persistence Layer                     │
│ Source Store │ Normalized Docs │ OKF Repo │ Graph │ Vectors │
│ Audit Log │ Job State │ Review State │ Release Artifacts     │
└──────────────────────────────┬───────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────┐
│                      Integration Layer                       │
│ File Connectors │ Web Fetch │ Git │ Synapse AK Compiler      │
│ Purview/Policy │ Identity │ MCP/API │ Deployment Targets     │
└──────────────────────────────────────────────────────────────┘
```

---

# 12. Major Architecture Components

## 12.1 Source Registry

The Source Registry maintains the canonical identity and lifecycle of every input.

Responsibilities:

* Register sources
* Assign stable source IDs
* Track versions
* Store fingerprints
* Record acquisition metadata
* Manage authority and trust levels
* Record security classification
* Track legal or licensing restrictions
* Detect duplicate source submissions
* Link source versions to composition runs

A source and a source version are separate entities.

---

## 12.2 Connector Framework

Connectors acquire content from supported locations.

Initial connectors:

* Local filesystem
* Drag-and-drop upload
* HTTP and HTTPS URLs
* Git repositories
* SharePoint and OneDrive
* Existing OKF project
* API submission

Future connectors may include:

* Confluence
* Notion
* Azure DevOps Wiki
* Microsoft Fabric
* Dataverse
* Enterprise content repositories
* Event streams

Connectors should only acquire and register content. They should not contain domain interpretation logic.

---

## 12.3 Parser and Extraction Framework

The extraction framework selects the appropriate parser based on content type and policy.

It supports:

* Multiple parser implementations per format
* Parser fallback
* Confidence scoring
* Benchmarking
* Side-by-side extraction comparison
* Local and managed extraction providers
* OCR escalation
* Visual-model escalation for complex pages or slides

Output is the canonical normalized document model.

---

## 12.4 Normalized Document Store

The Normalized Document Store contains format-neutral representations.

A normalized document may contain:

```yaml
document:
  source_version_id: srcv-123
  title: Example
  blocks:
    - block_id: b-001
      type: heading
      level: 1
      content: Customer Success
      anchor:
        page: 4
    - block_id: b-002
      type: paragraph
      content: ...
      anchor:
        page: 4
        bounding_box: [...]
    - block_id: b-003
      type: table
      cells: [...]
```

This representation must be immutable for a particular parser run.

A new extraction creates a new normalized version rather than overwriting the previous one.

---

## 12.5 Composition Orchestrator

The Composition Orchestrator manages the end-to-end workflow.

Responsibilities:

* Start and resume composition jobs
* Select processing policies
* Coordinate deterministic tools and language models
* Track dependencies
* Parallelize safe operations
* Enforce retry and timeout policies
* Pause for human review
* Record decisions
* Emit lifecycle events
* Support incremental recomposition

The orchestrator should execute explicit workflows rather than relying on an unconstrained autonomous agent.

Agentic reasoning is used within controlled stages.

---

## 12.6 Semantic Decomposition Service

This service identifies candidate knowledge objects from normalized blocks.

It uses:

* Structural cues
* Linguistic analysis
* Domain ontology
* Existing wiki context
* Configurable extraction prompts
* Classification models
* Language models
* Deterministic patterns

It returns proposals, not published knowledge.

---

## 12.7 Entity and Concept Resolution Service

This service resolves new candidates against the existing OKF knowledge space.

It searches:

* Canonical identifiers
* Aliases
* Labels
* Definitions
* Embeddings
* Graph relationships
* Source references
* Domain namespaces

It produces a resolution recommendation:

```yaml
resolution:
  candidate_id: candidate-42
  action: extend_existing
  target_id: concept:unified-delivery-coverage
  confidence: 0.87
  rationale:
    - Name similarity
    - Matching metric definition
    - Same CSU namespace
  requires_review: true
```

---

## 12.8 Provenance Service

The Provenance Service records the lineage of all knowledge.

It should provide:

* Source-to-object traceability
* Object-to-source traceability
* Derivation chains
* Revision history
* Human and machine attribution
* Source-span citations
* Compilation lineage
* Release lineage

The provenance graph is part of the knowledge product, not merely an operational log.

---

## 12.9 Knowledge Graph Service

The graph stores relationships that are not naturally represented through wiki hierarchy alone.

Examples:

```text
Objective → measured_by → KPI
Policy → governs → Process
Concept → broader_than → Subconcept
Claim → supported_by → Evidence
Source → authored_by → Organization
Procedure → requires → Capability
Signal → affects → Trend
Trend → influences → Prediction
Knowledge object → supersedes → Knowledge object
```

The initial implementation may use a lightweight embedded graph representation or relational edge tables within DuckDB.

The architecture should permit a later adapter to Neo4j, a managed graph service, or Foundry IQ without changing OKF semantics.

---

## 12.10 Semantic Index Service

The Semantic Index supports:

* Candidate matching
* Similarity detection
* Duplicate discovery
* Related-concept suggestions
* Review prioritization
* Downstream retrieval previews

Embeddings are derived artifacts.

They must not be treated as the authoritative representation of the knowledge.

The authoritative sources remain:

* OKF objects
* Explicit relations
* Source evidence
* Human decisions

---

## 12.11 OKF Repository

The OKF Repository is the system of record for the composed wiki.

A recommended implementation is a filesystem or Git-compatible project structure containing:

```text
knowledge-pack/
├── okf.yaml
├── ontology/
├── concepts/
├── policies/
├── procedures/
├── claims/
├── evidence/
├── sources/
├── semantic-models/
├── views/
├── assets/
├── reviews/
└── releases/
```

The repository should support:

* Human-readable diffs
* Branching
* Pull-request review
* Release tags
* Offline editing
* Validation in CI
* Reproducible compilation

A database may maintain working state, but the portable OKF representation remains exportable and self-describing.

---

## 12.12 Validation Engine

The Validation Engine supports layered validation.

### Structural validation

* Schema validity
* Required fields
* Identifier syntax
* Reference integrity

### Semantic validation

* Allowed relations
* Cardinality
* Type compatibility
* Namespace rules

### Knowledge quality validation

* Missing evidence
* Missing definitions
* Duplicate concepts
* Orphaned objects
* Circular dependencies
* Unsupported claims

### Governance validation

* Source classification
* Restricted data propagation
* Approval status
* Retention
* Licensing

### Compilation validation

* Target compatibility
* Required compiler extensions
* Unsupported object types
* Missing deployment metadata

---

## 12.13 Review and Decision Service

Review is represented as durable workflow state.

A review item contains:

* Question
* Affected objects
* Source evidence
* Proposed options
* System recommendation
* Confidence
* Required reviewer role
* Decision
* Decision rationale
* Timestamp
* Resulting changes

Human decisions become reusable composition memory.

For example, if reviewers repeatedly determine that a particular publication is authoritative for definitions, the system may propose an explicit authority policy rather than asking the same question repeatedly.

---

## 12.14 Release Manager

The Release Manager converts mutable workspace state into immutable OKF releases.

A release contains:

* Version
* Included objects
* Source-version manifest
* Ontology version
* Validation report
* Approval record
* Change summary
* Compiler compatibility
* Security classification
* Release signature or checksum

Only an immutable release may be sent to the AKP compiler.

---

## 12.15 Synapse AK Compiler Adapter

The Composer invokes Synapse AK through a stable compiler contract.

Example:

```text
compile(
    okf_release,
    target_profile,
    compiler_version,
    compilation_options
) → compilation_result
```

The result includes:

* AKP artifact
* Compilation manifest
* Warnings
* Errors
* Generated indexes
* Graph statistics
* Source coverage
* Validation summary
* Artifact checksum

Compiler implementation details remain outside the Composer.

---

# 13. Canonical Domain Model

```text
Workspace
 ├── Source
 │    └── SourceVersion
 │         └── ExtractionRun
 │              └── NormalizedBlock
 │
 ├── CandidateKnowledgeObject
 │    └── ResolutionProposal
 │
 ├── KnowledgeObject
 │    ├── Concept
 │    ├── Claim
 │    ├── Policy
 │    ├── Procedure
 │    ├── Principle
 │    ├── Measure
 │    ├── Evidence
 │    └── other OKF types
 │
 ├── Relationship
 ├── ProvenanceAssertion
 ├── ReviewItem
 ├── Decision
 ├── ValidationResult
 └── Release
      └── Compilation
           └── AKPArtifact
```

---

# 14. Composition Lifecycle

## Stage 1: Create

The user creates a workspace and selects:

* Domain
* OKF profile
* Target AKP type
* Initial ontology
* Composition policies
* Security context

## Stage 2: Acquire

Sources are uploaded, linked, synchronized, or submitted through API.

## Stage 3: Normalize

Format-specific parsers produce normalized document structures.

## Stage 4: Understand

The system identifies structure, language, topics, entities, and candidate knowledge objects.

## Stage 5: Resolve

Candidates are matched against the existing ontology and wiki.

## Stage 6: Compose

The system proposes new or changed OKF content and relationships.

## Stage 7: Review

Humans resolve material ambiguity and approve governed content.

## Stage 8: Validate

The wiki is checked for structural, semantic, quality, security, and compilation readiness.

## Stage 9: Release

The approved state becomes an immutable OKF release.

## Stage 10: Compile

Synapse AK compiles the release into an AKP.

## Stage 11: Evaluate

The system measures:

* Compilation success
* Coverage
* Retrieval behaviour
* Source traceability
* Unresolved uncertainty
* Knowledge quality

## Stage 12: Maintain

Source updates trigger incremental recomposition.

---

# 15. Agentic Architecture

Synapse Composer should use agents selectively.

It should not be implemented as one general-purpose agent with unrestricted access to every operation.

Recommended specialized roles include:

## Source analyst

Understands source purpose, audience, authority, scope, and structure.

## Knowledge extractor

Identifies candidate knowledge objects and evidence spans.

## Concept librarian

Resolves concepts, aliases, duplication, and taxonomy placement.

## Ontology steward

Proposes object types and relationships while enforcing ontology constraints.

## Contradiction analyst

Identifies conflicting, superseded, scoped, or temporally incompatible assertions.

## Wiki architect

Proposes navigation, grouping, page structure, and cross-links.

## Quality reviewer

Finds unsupported claims, incomplete definitions, weak evidence, and structural defects.

## Release analyst

Summarizes changes, affected knowledge, validation state, and compilation impact.

These agents operate through deterministic tools and typed contracts.

They may propose changes, but publication authority remains governed by policy.

---

# 16. Tool and Agent Boundary

The following should be deterministic tools:

* File acquisition
* Hashing
* MIME detection
* Parser invocation
* OCR invocation
* Block extraction
* Schema validation
* Identifier generation
* Graph traversal
* Exact duplicate detection
* Repository writes
* Version control
* Release creation
* Compiler invocation
* Audit logging

Agentic reasoning is appropriate for:

* Classifying knowledge
* Interpreting meaning
* Proposing concept matches
* Synthesizing across sources
* Explaining contradictions
* Suggesting wiki organization
* Producing review questions
* Assessing source relevance
* Generating human-readable change summaries

This boundary prevents language models from becoming the system of record.

---

# 17. Trust and Authority Model

Not every source should carry equal weight.

The Composer should support an explicit source authority model.

Possible authority dimensions:

* Official versus unofficial
* Normative versus informative
* Primary versus secondary
* Current versus historical
* Global versus regional
* Approved versus draft
* Internal versus external
* Policy versus interpretation
* Named owner
* Effective period

Example:

```yaml
authority:
  level: official
  nature: normative
  scope:
    organization: CSU
    geography: global
  effective_from: 2026-07-01
  owner: CSU Leadership
```

Authority metadata influences composition proposals but does not erase conflicting evidence.

---

# 18. Security and Governance Vision

## 18.1 Security inheritance

Derived knowledge should inherit the most restrictive applicable classification of its supporting sources unless explicitly declassified through an approved process.

## 18.2 Object-level policy

Access control may need to apply at:

* Source
* Source fragment
* Knowledge object
* Wiki section
* Release
* Compiled AKP
* Retrieval response

## 18.3 Sensitive-data detection

The Composer should detect and flag:

* Personal information
* Customer-confidential information
* Credentials and secrets
* Contractual information
* Export-controlled information
* Restricted internal material

## 18.4 Governance integration

Potential integrations include:

* Microsoft Purview
* Enterprise identity providers
* Data loss prevention policies
* Retention systems
* Information protection labels
* Audit and compliance platforms

The Composer should preserve governance metadata into OKF and, where supported, into the compiled AKP.

## 18.5 Model isolation

Composition policies should control which processing may occur:

* Fully local
* Within an enterprise tenant
* Through an approved managed model
* Through no language model at all
* Using redacted content
* Using metadata only

---

# 19. Deployment Models

## 19.1 Local Composer

Suitable for:

* Individual authors
* Sensitive prototypes
* Developer workflows
* Offline composition
* Local AKP compilation

Possible components:

* Desktop or local web application
* Local filesystem
* Git repository
* DuckDB working store
* Embedded vector index
* Optional local models
* Synapse AK command-line compiler

## 19.2 Enterprise Composer

Suitable for:

* Collaborative knowledge teams
* Shared review
* Managed governance
* Scheduled source refresh
* Central deployment
* Foundry IQ integration

Possible components:

* Web application
* Containerized services
* Object storage
* Managed relational database
* Graph adapter
* Model gateway
* Queue or workflow service
* Enterprise identity
* Purview integration
* CI/CD integration
* Synapse AK compilation service

## 19.3 Hybrid Composer

Sensitive acquisition and parsing occur locally, while approved normalized or composed knowledge is synchronized to a managed workspace.

The architecture should support all three through adapters rather than product forks.

---

# 20. Storage Architecture

A pragmatic initial stack could use:

| Concern              | Initial implementation                            |
| -------------------- | ------------------------------------------------- |
| OKF system of record | Filesystem and Git                                |
| Working state        | DuckDB or PostgreSQL                              |
| Source binaries      | Filesystem or object storage                      |
| Normalized documents | JSON/Parquet/object storage                       |
| Graph                | DuckDB edge tables or embedded graph              |
| Embeddings           | LanceDB, DuckDB extension, or adapter             |
| Search               | Local full-text index                             |
| Jobs                 | Embedded queue locally; managed workflow remotely |
| Audit                | Append-only event log                             |
| Releases             | Immutable repository artifacts                    |
| Compiled AKPs        | Package registry or object storage                |

The initial implementation should prefer simplicity and portability.

A graph database should be introduced when graph scale, traversal patterns, concurrency, or operational requirements justify the additional platform.

---

# 21. Event Model

Important domain events may include:

```text
SourceRegistered
SourceVersionAcquired
ExtractionCompleted
ExtractionFailed
CandidateProposed
ConceptMatchProposed
KnowledgeObjectCreated
KnowledgeObjectRevised
ContradictionDetected
ReviewRequested
ReviewResolved
ValidationCompleted
ReleaseCreated
CompilationRequested
CompilationCompleted
AKPPublished
SourceChangeDetected
RecompositionRequested
```

Events support:

* Auditability
* Incremental processing
* Integration
* Reprocessing
* Observability
* Future automation

Event sourcing of the entire product is not required initially, but material knowledge changes and decisions should be recorded append-only.

---

# 22. Explainability Model

For every proposed change, the Composer should be able to explain:

* What changed
* Why it changed
* Which source caused the change
* Which source fragments were used
* Which rules were applied
* Which model or agent proposed it
* How confident the proposal is
* What existing knowledge is affected
* Whether human approval is required

A proposal without this explanation should not be eligible for automatic publication.

---

# 23. Quality Model

Knowledge quality should be evaluated across several dimensions.

## Structural quality

Is the OKF valid and internally connected?

## Evidentiary quality

Are claims supported by sufficient and appropriate evidence?

## Semantic quality

Are concepts clearly defined and correctly related?

## Temporal quality

Is validity over time represented correctly?

## Authority quality

Can users distinguish official guidance from commentary?

## Coverage quality

Does the wiki cover the intended domain and source corpus?

## Retrieval quality

Can downstream systems retrieve precise and relevant context?

## Operational quality

Can the knowledge be updated, validated, compiled, and deployed reliably?

A single “confidence score” should not replace these dimensions.

---

# 24. Evaluation Strategy

The Composer should be evaluated at four levels.

## Extraction evaluation

* Text accuracy
* Table fidelity
* Reading order
* Heading preservation
* Figure-caption association
* OCR quality

## Composition evaluation

* Knowledge-type classification
* Concept resolution precision
* Duplicate detection
* Evidence linkage
* Relationship accuracy
* Contradiction detection

## Human productivity evaluation

* Time to first valid wiki
* Review effort per source
* Percentage of proposals accepted
* Repeated correction rate
* Time to update an existing wiki

## Runtime outcome evaluation

* Retrieval precision
* Answer grounding
* Citation correctness
* Context efficiency
* Agent-plan quality
* Reduction in hallucinated domain claims

Runtime evaluation matters because a wiki that appears well structured may still compile into an ineffective knowledge pack.

---

# 25. Initial Product Scope

## In scope for the first product release

* PDF, Word, PowerPoint, Markdown, and URL input
* Source registry
* Format-aware parsing
* Canonical normalized document model
* Candidate extraction
* Core concept and evidence resolution
* Human review queue
* OKF Wiki generation
* Provenance tracking
* Validation
* Git-compatible OKF repository
* Immutable releases
* Synapse AK compiler invocation
* Local deployment
* API and command-line access

## Explicitly out of scope initially

* General-purpose enterprise content management
* Full document collaboration replacement
* Autonomous publication of high-impact policies
* Training foundation models
* Replacing domain experts
* Generic workflow automation unrelated to knowledge composition
* High-scale web crawling
* Automatic legal interpretation
* Automatic declassification
* Runtime business execution
* Agent planning and action execution
* AKP retrieval runtime itself

These boundaries keep Composer focused on creating trusted knowledge products.

---

# 26. Product Roadmap

## Horizon 1: Assisted composition

The system converts mixed sources into a reviewable OKF Wiki.

Focus:

* Parsing quality
* Provenance
* Basic concept resolution
* Human review
* Compilation readiness

## Horizon 2: Continuous knowledge maintenance

The system monitors known sources and proposes incremental updates.

Focus:

* Change detection
* Impact analysis
* Contradiction handling
* Reusable decisions
* Scheduled recomposition

## Horizon 3: Collaborative knowledge engineering

Multiple teams compose federated knowledge packs.

Focus:

* Shared ontology
* Namespaces
* Branching and merging
* Role-based review
* Cross-pack references
* Enterprise governance

## Horizon 4: Agentic knowledge ecosystem

Composer agents continuously curate a portfolio of knowledge packs from trusted source ecosystems.

Focus:

* Source discovery
* Policy-driven automatic updates
* Cross-AKP concept resolution
* Knowledge quality analytics
* Runtime feedback
* Self-improving composition policies

---

# 27. Key Architecture Decisions

## Decision 1: OKF is the system-of-record representation

The Composer may use databases for working state, but the authored output is an explicit, portable OKF project.

## Decision 2: Normalization precedes semantic interpretation

Format parsing must not be entangled with domain modelling.

## Decision 3: Provenance is mandatory and structural

Citations are not decorative metadata. They are part of the knowledge model.

## Decision 4: Knowledge objects have stable identities

Identity is independent of filenames, headings, and generated wording.

## Decision 5: Human review is risk-based

The system escalates material ambiguity rather than requiring review of every transformation.

## Decision 6: Agents propose; governed services commit

All persistent changes flow through validated domain commands.

## Decision 7: Compilation occurs from immutable releases

Working state is never compiled directly into a production AKP.

## Decision 8: Embeddings are replaceable derived indexes

Changing the embedding model does not change the authoritative knowledge.

## Decision 9: Local and managed deployments share contracts

The product should not maintain separate semantic implementations for local and cloud use.

## Decision 10: Incremental recomposition is a first-class capability

The Composer maintains knowledge over time rather than repeatedly regenerating it.

---

# 28. Principal Risks

## Hallucinated structure

The system may infer concepts or relationships not justified by the source.

**Mitigation:** Explicit provenance, confidence, typed proposals, validation, and human review.

## Silent information loss

Parsers may omit tables, notes, figures, or layout-dependent meaning.

**Mitigation:** Format-specific extraction, extraction reports, visual previews, and parser benchmarking.

## Over-merging

Similar but distinct concepts may be combined.

**Mitigation:** Stable identifiers, ontology rules, conservative thresholds, and review.

## Knowledge duplication

Different sources may create parallel representations of the same concept.

**Mitigation:** Resolution service, aliases, graph context, and curator workflows.

## Source poisoning

Low-quality or malicious sources may influence authoritative knowledge.

**Mitigation:** Trust policies, source registration, restricted automation, and approval requirements.

## Temporal confusion

Outdated material may be presented as current guidance.

**Mitigation:** Effective dates, supersession, authority and source-version tracking.

## Excessive review burden

Human reviewers may become the bottleneck.

**Mitigation:** Review by exception, confidence thresholds, reusable decisions, and materiality policies.

## Model dependency

Composition quality may become tied to one model provider.

**Mitigation:** Typed model gateway, evaluation suite, model-independent domain contracts, and deterministic validation.

---

# 29. Success Measures

The product is successful when:

* A domain expert can create a useful first OKF Wiki without becoming a knowledge-graph engineer.
* Every important assertion can be traced to its source or named human author.
* New source versions produce understandable, incremental change proposals.
* Reviewers focus on material decisions rather than mechanical cleanup.
* The same OKF release produces reproducible AKP builds.
* Compiled knowledge improves the accuracy, grounding, and efficiency of downstream agentic systems.
* Knowledge packs remain maintainable after their original authors move on.
* Organizations can treat knowledge as an engineered product rather than a folder of documents.

---

# 30. Final Product Narrative

Organizations already possess much of the knowledge their agents need.

The problem is that the knowledge is scattered across documents, presentations, websites, diagrams, policies, notes, and the minds of experts. Each source captures fragments of meaning, but none of them alone provides the coherent knowledge environment required for reliable agentic reasoning.

Synapse Composer is the refinery between information and intelligence.

It acquires raw material without losing its origin. It interprets without hiding its reasoning. It structures without pretending ambiguity does not exist. It uses machines for scale and humans for judgment. It turns fragmented content into a governed OKF Wiki and turns that wiki into a release that Synapse AK can compile into an Agentic Knowledge Pack.

The result is not simply better search.

It is a durable, traceable and evolvable knowledge system that agents can understand, reason with, and ultimately act from.

> **Synapse Composer transforms what an organization has written into what its agents can responsibly know.**
