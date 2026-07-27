# Synapse Composer: Architectural Framework Decisions

The central architectural decision is that **Composer must not be built around one ingestion library or one LLM agent**.

A world-class Composer needs a layered pipeline where each source passes through increasingly semantic stages:

```text
Source acquisition
        ↓
Format-native extraction
        ↓
Canonical document representation
        ↓
Semantic interpretation
        ↓
Knowledge-object proposals
        ↓
Concept and evidence resolution
        ↓
Human-governed commit
        ↓
OKF repository
        ↓
AKP compiler
```

The tools should be replaceable behind contracts. The **canonical intermediate model and OKF model**, not Docling, Azure Document Intelligence, an LLM, or a vector database, must define the architecture.

---

# 1. Recommended Reference Stack

## Default stack at a glance

| Architectural concern        | Recommended default                     | Secondary or escalation path        |
| ---------------------------- | --------------------------------------- | ----------------------------------- |
| Language                     | Python 3.12+                            | —                                   |
| Domain contracts             | Pydantic v2                             | JSON Schema export                  |
| API                          | FastAPI                                 | CLI through Typer                   |
| Document parsing             | Docling                                 | Format-native parsers               |
| Difficult PDFs/OCR           | Azure AI Document Intelligence          | Docling OCR/local OCR               |
| Lightweight conversion       | MarkItDown                              | Convenience only                    |
| Parser fallback/benchmark    | Unstructured                            | Not canonical                       |
| DOCX deep extraction         | `python-docx` + OOXML inspection        | LibreOffice conversion              |
| PPTX deep extraction         | `python-pptx` + OOXML inspection        | LibreOffice rendering               |
| PDF inspection               | PyMuPDF                                 | pypdf for metadata/basic operations |
| Web acquisition              | HTTPX                                   | Playwright escalation               |
| Web content extraction       | Trafilatura                             | DOM-aware custom extractor          |
| Image/diagram interpretation | Multimodal model gateway                | Human review                        |
| Workflow orchestration       | Explicit state machine initially        | Temporal at enterprise scale        |
| Semantic interpretation      | Model gateway + structured outputs      | Multiple model providers            |
| Agent implementation         | Small typed domain agents               | No autonomous super-agent           |
| Working store, local         | DuckDB                                  | SQLite for workflow state           |
| Working store, service       | PostgreSQL                              | pgvector optional                   |
| Canonical knowledge          | Git-backed OKF files                    | Object storage for releases         |
| Source binaries              | Filesystem/object storage               | Immutable content-addressed store   |
| Graph working model          | Relational edge tables + NetworkX       | Neo4j when justified                |
| Vector matching              | Qdrant or pgvector service-side         | LanceDB/local adapter               |
| Full-text search             | PostgreSQL/OpenSearch enterprise        | DuckDB FTS locally                  |
| Provenance                   | Native Synapse provenance model         | W3C PROV-compatible export          |
| Validation                   | Pydantic + JSON Schema + custom linter  | SHACL-like semantic constraints     |
| Observability                | OpenTelemetry                           | Application-specific audit events   |
| Evaluation                   | Golden corpus + parser/model benchmarks | Human acceptance metrics            |
| AKP build                    | Synapse AK compiler                     | Never compiled directly by Composer |

---

# 2. Decision: Use Docling as the Primary Extraction Framework

## Recommendation

Use **Docling as the default document-conversion engine**, particularly for:

* PDF
* DOCX
* PPTX
* HTML
* Images
* Markdown

Docling provides a unified, richly structured document representation and includes layout analysis, reading-order handling, OCR, table extraction, and multiple-format conversion. Its `DocumentConverter` supports both individual and batch conversion and returns a structured `DoclingDocument`, making it a strong primary extraction adapter. ([Docling Project][1])

## Where it sits

```text
PDF / DOCX / PPTX / HTML
           ↓
    Docling adapter
           ↓
  DoclingDocument
           ↓
Synapse Normalized Document
```

## Important constraint

**Do not expose `DoclingDocument` beyond the extraction boundary.**

Docling is an implementation dependency. Synapse must map its output into its own canonical representation.

Otherwise:

* Docling upgrades become domain-model migrations.
* Switching parsers becomes difficult.
* OKF composition becomes coupled to parser-specific concepts.
* Provenance anchors become unstable.

## ADR

**ADR: Adopt Docling as the default multi-format extraction provider, behind the Synapse Document Extractor contract.**

---

# 3. Decision: Use Format-Native Parsers for Fidelity, Not as the Main Pipeline

Docling gives breadth. Format-native libraries give precision.

A world-class system should use both.

## DOCX

Use:

* `python-docx` for document hierarchy, paragraphs, styles, tables and relationships.
* Direct OOXML inspection for features `python-docx` does not expose well, such as comments, tracked revisions, custom XML, some fields and complex relationships.
* LibreOffice headless conversion only as a compatibility fallback for older `.doc` formats or rendering.

### Why

A domain document may encode meaning through:

* Heading styles
* Tables
* Footnotes
* Comments
* Tracked changes
* Content controls
* Hyperlinks
* Embedded diagrams

A generic Markdown conversion often loses some of these signals.

## PPTX

Use:

* `python-pptx` for slides, shapes, text, tables, notes and relationships.
* Direct OOXML inspection for unsupported objects.
* LibreOffice or Microsoft rendering services to produce slide images.
* A multimodal interpretation step for visual semantics.

A PowerPoint slide is often a **visual argument**, not a document page.

```text
Native structure extraction
        +
Rendered slide image
        +
Speaker notes
        ↓
Slide interpretation object
```

## PDF

Use:

* Docling for layout-aware primary extraction.
* PyMuPDF for page rendering, coordinates, annotations, image extraction and forensic inspection.
* `pypdf` only for lightweight metadata, page operations and low-complexity extraction.

## ADR

**ADR: Supplement the default extractor with format-native enrichment adapters where source semantics or fidelity require it.**

---

# 4. Decision: Azure Document Intelligence Is an Escalation Tier

Use Azure AI Document Intelligence for:

* Scanned documents
* Difficult reading order
* Complex tables
* Forms
* Handwritten or low-quality source material
* Cases where local extraction confidence falls below a threshold
* Enterprise workloads where managed support and operational SLAs matter

The Azure layout model extracts text, tables, selection marks and document structure using OCR and deep-learning-based analysis. Microsoft’s current documentation also describes broader processing models for OCR, layout and custom extraction. ([Microsoft Learn][2])

## Do not make it mandatory

Composer should remain capable of:

* Fully local operation
* Offline composition
* Restricted-data operation
* Low-cost bulk conversion
* Provider-independent testing

## Recommended routing policy

```text
Attempt local extraction
        ↓
Run quality assessment
        ↓
┌───────────────────────┐
│ Extraction acceptable │──→ Continue
└───────────────────────┘
        ↓ no
Azure Document Intelligence
        ↓
Compare extraction quality
        ↓
Select or merge result
```

## ADR

**ADR: Use managed document intelligence as a policy-controlled extraction escalation, not the universal ingestion path.**

---

# 5. Decision: MarkItDown Is a Convenience Adapter, Not a Canonical Parser

Microsoft MarkItDown supports conversion of PDF, Word, PowerPoint, Excel, HTML, images and several additional formats to Markdown. ([GitHub][3])

Use it for:

* Rapid import
* Simple documents
* Developer convenience
* Preview
* Source formats with no dedicated adapter
* Low-fidelity fallback
* Creating human-readable diagnostic output

Do not use it as:

* The canonical normalized representation
* The provenance foundation
* The only PowerPoint interpreter
* The source of graph relationships
* The authoritative table extraction engine

Markdown is a useful view, but it is **too lossy to serve as the internal document model**.

## ADR

**ADR: Support MarkItDown as a lightweight conversion and fallback adapter, but prohibit Markdown-only normalization for rich sources.**

---

# 6. Decision: Keep Unstructured as a Benchmark and Fallback Provider

Unstructured supports broad file-type partitioning and routes documents to format-specific partition functions. Its element model is useful for comparison, fallback and format coverage. ([Unstructured][4])

Use it for:

* Unsupported or unusual formats
* Parser comparison
* Regression testing
* Fallback extraction
* Email formats such as `.eml` and `.msg`
* A second opinion on semantic element boundaries

Do not make both Docling and Unstructured first-class domain dependencies.

They should implement the same interface:

```python
class DocumentExtractor(Protocol):
    def supports(self, source: SourceDescriptor) -> bool: ...

    async def extract(
        self,
        source: AcquiredSource,
        options: ExtractionOptions,
    ) -> ExtractionResult: ...
```

## ADR

**ADR: Permit multiple extraction providers under a common contract and maintain parser-selection policies rather than committing the platform to one parser.**

---

# 7. Decision: Define a Synapse Canonical Document Model

This is the most important ADR.

The normalized representation should preserve document structure before any semantic interpretation occurs.

## Core model

```text
NormalizedDocument
├── metadata
├── source_version
├── content_tree
├── blocks
├── assets
├── links
├── annotations
├── extraction_diagnostics
└── provenance_anchors
```

## Block types

```text
Heading
Paragraph
List
ListItem
Table
TableCell
Figure
Image
Caption
CodeBlock
Quote
Footnote
Slide
SpeakerNote
Diagram
Chart
Formula
Header
Footer
PageBreak
UnknownRegion
```

## Every block should have

* Stable block ID
* Parent ID
* Ordering
* Original text
* Normalized text
* Page or slide anchor
* Bounding box where available
* Parser identity and version
* Extraction confidence
* Source hash
* Style and hierarchy metadata
* Asset references
* Security metadata

## Why this matters

The canonical model becomes the “airlock” between two worlds:

```text
Document world             Knowledge world
pages, slides, shapes  →   concepts, claims, policies
```

Without this boundary, semantic composition becomes inseparable from extraction.

## ADR

**ADR: Establish the Synapse Canonical Document Model as the only accepted input to semantic composition.**

---

# 8. Decision: Use Two Separate AI Stages

Do not ask one model to read a source and directly write the final OKF Wiki.

Use two explicit AI stages.

## Stage A: Source interpretation

Produces evidence-grounded observations:

* Candidate concepts
* Candidate claims
* Definitions
* Policies
* Procedures
* Metrics
* Relationships
* Source purpose
* Source authority
* Temporal scope

Output:

```text
Candidate Knowledge Objects
```

## Stage B: Knowledge resolution

Compares candidates against the existing OKF knowledge space and proposes:

* Create
* Extend
* Merge
* Alias
* Contradict
* Supersede
* Scope
* Ignore
* Escalate for review

Output:

```text
Knowledge Change Proposal
```

## Why

The first stage asks:

> What is present in this source?

The second asks:

> What does this mean in the existing knowledge system?

Those are different reasoning problems and require different context.

## ADR

**ADR: Separate source-grounded extraction from knowledge-space resolution and prohibit direct source-to-published-OKF generation.**

---

# 9. Decision: Use Typed Model Calls, Not Free-Form Agent Responses

Use Pydantic v2 models as the authoritative contracts for model inputs and outputs. Pydantic can generate JSON Schema from models, enabling validation and provider-neutral structured-output contracts. ([Pydantic][5])

Example:

```python
class CandidateClaim(BaseModel):
    candidate_id: str
    statement: str
    source_block_ids: list[str]
    claim_type: ClaimType
    confidence: float
    explicit_in_source: bool
    interpretation_notes: list[str]
```

Every model response should go through:

1. Provider-side structured output where supported
2. Pydantic validation
3. Semantic validation
4. Evidence-anchor validation
5. Retry or rejection

## Model gateway

Create a Synapse abstraction over:

* Azure OpenAI / Foundry models
* OpenAI
* Local models
* Potential future providers

The gateway owns:

* Model selection
* Structured output
* Retry policies
* Token budgets
* Redaction
* Logging
* Prompt versions
* Model versions
* Evaluation traces

Avoid making a framework such as LangChain or LlamaIndex a core architectural dependency. They may be useful inside adapters, but Synapse should own its contracts and orchestration.

## ADR

**ADR: All model interactions must use versioned, typed Pydantic contracts through a provider-neutral model gateway.**

---

# 10. Decision: Use Specialist Agents, but a Deterministic Workflow

The Composer benefits from specialist reasoning roles:

* Source analyst
* Claim extractor
* Concept librarian
* Ontology steward
* Contradiction analyst
* Wiki architect
* Quality reviewer

But these should be invoked by an explicit workflow:

```text
extract
→ assess quality
→ interpret
→ resolve
→ validate
→ request review
→ commit
```

Not:

```text
“Here are some tools; build a wiki.”
```

## Why

An unconstrained agent will be difficult to:

* Resume
* Test
* Audit
* Reproduce
* Version
* Secure
* Evaluate
* Explain

Agents should produce **proposals**. Domain services should apply state changes.

## ADR

**ADR: Use deterministic workflow orchestration with bounded agentic reasoning activities; agents may propose but cannot directly commit knowledge.**

---

# 11. Decision: Start with an Explicit Persistent State Machine; Introduce Temporal When Required

## Initial implementation

Build the first Composer around:

* Python application services
* Persistent job and step records
* Idempotent activities
* Explicit workflow states
* Retry policies
* Review gates
* Append-only events

For the local Composer, this can run with DuckDB or SQLite-backed job state.

## Enterprise implementation

Temporal becomes valuable when workflows:

* Run for hours or days
* Pause for human review
* Survive process restarts
* Call unreliable external services
* Fan out across many documents
* Need retries and compensation
* Require horizontal workers

Temporal is explicitly designed for durable workflows that resume after crashes, network failures or infrastructure outages. ([docs.temporal.io][6])

## Recommendation

Design the workflow activities so they can later become Temporal activities, but do not require Temporal for the local MVP.

## ADR

**ADR: Model composition as a durable state machine from day one, with Temporal as the enterprise orchestration target rather than an MVP dependency.**

---

# 12. Decision: Web Acquisition Uses HTTP First, Browser Second

## Primary path

Use:

* HTTPX for retrieval
* Redirect and canonical URL handling
* ETag and Last-Modified support
* Content hashing
* Response-header capture
* Raw HTML snapshotting

## Extraction

Use Trafilatura to extract the primary content, metadata, links and tables from static HTML. Its API supports main-content extraction, metadata and structured extraction options. ([trafilatura.readthedocs.io][7])

## Escalation

Use Playwright when:

* Content requires JavaScript rendering
* Authentication is required
* The visible DOM differs materially from initial HTML
* Content is loaded dynamically
* A print or reader view must be generated

Playwright provides browser automation across Chromium, Firefox and WebKit through synchronous and asynchronous Python APIs. ([Playwright][8])

## Store both

```text
URL record
├── HTTP response
├── raw HTML
├── rendered DOM, when used
├── screenshot or PDF, when relevant
├── extracted content
├── canonical URL
└── content fingerprint
```

## ADR

**ADR: Use deterministic HTTP acquisition and extraction by default, with Playwright as a controlled rendering escalation.**

---

# 13. Decision: Visual Interpretation Is Separate from Text Extraction

Especially for PowerPoint and PDFs, visual meaning may include:

* Arrows
* Relative placement
* Colour coding
* Swim lanes
* Quadrants
* Maturity curves
* Architecture layers
* Diagram topology
* Chart trends

A text parser cannot reliably reconstruct all of this.

## Pipeline

```text
Structural extraction
       +
Page/slide rendering
       ↓
Visual relevance classifier
       ↓
Multimodal interpretation
       ↓
Typed diagram or visual proposition
       ↓
Human review where material
```

The multimodal model should produce structures such as:

```yaml
visual:
  type: layered_architecture
  elements:
    - id: layer-1
      label: Knowledge plane
  relationships:
    - from: layer-1
      to: layer-2
      type: feeds
  interpretation_confidence: 0.76
  source_asset_id: asset-219
```

Do not flatten the visual description into prose and discard the original asset.

## ADR

**ADR: Treat visual interpretation as an enrichment stage with retained source imagery, not as ordinary text extraction.**

---

# 14. Decision: Git-Backed OKF Is the Canonical Knowledge Store

Use Git-compatible files for the authoritative OKF Wiki.

Benefits:

* Human-readable
* Portable
* Diffable
* Branchable
* Reviewable
* CI-validatable
* Reproducible
* Independent from the Composer application
* Suitable for Codex and other engineering agents

## Working state versus authoritative state

```text
Composer working database
        ↓ accepted changes
Git-backed OKF repository
        ↓ immutable tag/release
Synapse AK compiler
```

The working database may contain:

* Candidates
* Temporary embeddings
* Review tasks
* Model outputs
* Jobs
* Diagnostics

The OKF repository contains only accepted knowledge and required provenance.

## Tool recommendation

Use:

* Git CLI initially
* Dulwich or pygit2 if embedded Git operations become necessary
* Conventional pull requests for enterprise review
* Signed tags or release manifests for compilation

## ADR

**ADR: Treat the Git-backed OKF repository as the canonical authored knowledge product; databases hold working state only.**

---

# 15. Decision: DuckDB Locally, PostgreSQL for Shared Composer State

## Local Composer

Use DuckDB for:

* Source manifest
* Normalized block metadata
* Candidates
* Relations
* Evaluation results
* Search analytics
* Local composition state

DuckDB works well with nested data, analytics and Parquet-based artifacts.

Use SQLite only where transactional workflow semantics are simpler or libraries require it.

## Enterprise Composer

Use PostgreSQL for:

* Concurrent workspaces
* Reviews
* Job state
* Identity and authorization
* Composition proposals
* Audit records
* Workspace metadata

Use object storage for:

* Source files
* Rendered pages
* Normalized JSON/Parquet
* Model artifacts
* Release packages

## ADR

**ADR: Use DuckDB as the local composition workbench and PostgreSQL plus object storage for collaborative enterprise operation.**

---

# 16. Decision: Do Not Introduce Neo4j Initially

The Composer needs a graph model, but not necessarily a graph database.

Initially represent the graph as:

```text
knowledge_nodes
knowledge_edges
aliases
source_links
provenance_edges
```

Use:

* DuckDB/PostgreSQL edge tables for persistence
* NetworkX for in-process analysis, validation and graph algorithms
* OKF relations as the canonical representation

Introduce Neo4j when there is proven need for:

* Large cross-AKP graph traversal
* High concurrency
* Complex interactive graph exploration
* Deep path querying
* Graph-native operational APIs
* Enterprise graph governance

The graph database should remain a projection, not the source of truth.

## ADR

**ADR: Persist graph semantics in OKF and relational edge structures initially; defer a dedicated graph database until measurable graph requirements justify it.**

---

# 17. Decision: Use Vectors Only for Candidate Generation

Vectors should support:

* Potential duplicate detection
* Similar-concept discovery
* Candidate-to-existing-object matching
* Related-source detection
* Review prioritization
* Clustering

They should not decide:

* Whether two concepts are identical
* Which source is authoritative
* Whether a policy supersedes another
* Whether a claim is true
* Which relation should be committed

## Recommended deployment

### Local

Use a replaceable adapter around:

* LanceDB, or
* a lightweight local vector index

### Enterprise

Use:

* pgvector when scale and query patterns remain moderate, or
* Qdrant when semantic search becomes a distinct operational service

The vector index is fully rebuildable.

## ADR

**ADR: Treat embeddings and vector indexes as disposable candidate-generation projections, never as authoritative knowledge.**

---

# 18. Decision: Provenance Must Be Native, Not Added Afterward

Provenance should be attached at the moment a candidate is created.

Every candidate should reference:

```text
source ID
source version
extraction run
block IDs
page/slide
character or spatial span
interpretation run
prompt version
model version
human decisions
```

The internal model can align conceptually with W3C PROV entities, activities and agents, but should use a domain-specific Synapse schema optimized for composition.

## ADR

**ADR: Capture provenance at every transformation boundary and make evidence lineage a mandatory part of all publishable knowledge objects.**

---

# 19. Decision: Validation Is Layered

Use four validators.

## 1. Contract validation

Tools:

* Pydantic
* JSON Schema

Checks shapes and required fields.

## 2. Repository validation

Custom OKF linter:

* IDs
* references
* namespaces
* file layout
* front matter
* links
* source anchors

## 3. Semantic validation

Rules such as:

* A claim must have evidence or explicit human authorship.
* A supersession relation must include temporal metadata.
* A metric must define its unit.
* A policy must define scope or inherit it.
* A concept cannot alias itself.
* Published objects cannot reference candidates.

## 4. Quality evaluation

Model-assisted and deterministic checks:

* Duplicate concepts
* Conflicting definitions
* Missing context
* Weak source authority
* Unsupported synthesis
* Overly broad pages

## ADR

**ADR: Separate structural, repository, semantic and quality validation; only the first three should produce deterministic compilation blockers.**

---

# 20. Decision: Build an Evaluation Harness Before Optimizing Models

A world-class Composer is defined by measured composition quality, not by the prestige of its model.

Create a golden corpus containing:

* Simple PDF
* Complex multi-column PDF
* Scanned PDF
* Policy document
* DOCX with tables and tracked changes
* PowerPoint with notes
* Diagram-heavy presentation
* Markdown wiki
* Static web page
* JavaScript-rendered web page
* Contradictory sources
* Updated version of an existing source

Measure:

### Extraction

* Block recall
* Reading order
* Heading hierarchy
* Table correctness
* Image association
* Citation-anchor accuracy

### Interpretation

* Knowledge-type precision
* Evidence-link precision
* Unsupported inference rate
* Concept-resolution accuracy
* Contradiction detection

### Composition

* Human acceptance rate
* Correction rate
* Time to publish
* Unnecessary review count
* Knowledge duplication
* AKP retrieval quality

The Docling technical work itself emphasizes structured document conversion and specialized layout and table models; production research also indicates that OCR and document-processing stages can dominate latency and require separate scaling strategies. ([arXiv][9])

## ADR

**ADR: Parser and model selection must be governed by a versioned Composer benchmark suite rather than fixed vendor preference.**

---

# 21. Recommended Architecture Shape

```text
┌──────────────────────────────────────────────────────────┐
│                     Composer UI                          │
│ Sources │ Wiki │ Graph │ Review │ Release │ Evaluation  │
└──────────────────────────┬───────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────┐
│                Composer Application API                 │
│                  FastAPI + Pydantic                     │
└──────────────────────────┬───────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────┐
│               Composition State Machine                 │
│ Acquire → Extract → Interpret → Resolve → Review        │
│          → Validate → Commit → Release                  │
└───────┬──────────────────┬───────────────────────┬───────┘
        │                  │                       │
┌───────▼────────┐ ┌───────▼──────────┐ ┌─────────▼────────┐
│ Source         │ │ Document         │ │ Model Gateway    │
│ Connectors     │ │ Intelligence     │ │ Typed outputs    │
│ HTTPX          │ │ Docling          │ │ Azure/OpenAI/    │
│ Playwright     │ │ Native parsers   │ │ local providers  │
│ Git/files      │ │ Azure DI         │ │                 │
└───────┬────────┘ └───────┬──────────┘ └─────────┬────────┘
        │                  │                      │
        └──────────────────▼──────────────────────┘
                  Canonical Document Model
                           │
                  Candidate Knowledge Model
                           │
                  Change Proposal Service
                           │
                    Review and Commit
                           │
┌──────────────────────────▼───────────────────────────────┐
│                 Git-backed OKF Repository               │
│ Concepts │ Claims │ Evidence │ Policies │ Sources       │
└──────────────────────────┬───────────────────────────────┘
                           │
                    Immutable release
                           │
┌──────────────────────────▼───────────────────────────────┐
│                 Synapse AK Compiler                     │
└──────────────────────────┬───────────────────────────────┘
                           │
                          AKP
```

---

# 22. The First ADR Set

I would draft these ADRs first, in this order:

1. **Canonical Document Model**
2. **OKF as the Composer system of record**
3. **Git-backed knowledge repository**
4. **Multi-provider extraction architecture**
5. **Docling as default extraction provider**
6. **Format-native enrichment adapters**
7. **Managed document-intelligence escalation**
8. **Separation of extraction, interpretation and resolution**
9. **Typed model gateway using Pydantic contracts**
10. **Deterministic workflow with bounded specialist agents**
11. **Human-governed knowledge commit**
12. **Native provenance and evidence lineage**
13. **Local and enterprise persistence profiles**
14. **Graph as a projection, not initial graph-database dependency**
15. **Vectors as disposable candidate-generation indexes**
16. **Layered OKF validation**
17. **Immutable releases as the AKP compilation boundary**
18. **Golden-corpus-driven parser and model selection**

The most foundational three are:

> **The canonical document model defines what Composer can understand.
> OKF defines what Composer can know.
> The compiler contract defines what Composer can publish.**

Everything else should remain replaceable.

[1]: https://docling-project.github.io/docling/?utm_source=chatgpt.com "Documentation - Docling"
[2]: https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/model-overview?view=doc-intel-4.0.0&utm_source=chatgpt.com "Document Processing Models - Document Intelligence"
[3]: https://github.com/microsoft/markitdown?utm_source=chatgpt.com "microsoft/markitdown: Python tool for converting files ..."
[4]: https://docs.unstructured.io/open-source/introduction/supported-file-types?utm_source=chatgpt.com "Supported file types"
[5]: https://pydantic.dev/docs/validation/2.5/concepts/json_schema/?utm_source=chatgpt.com "Json schema | Pydantic Docs"
[6]: https://docs.temporal.io/?utm_source=chatgpt.com "Temporal Docs | Temporal Platform Documentation"
[7]: https://trafilatura.readthedocs.io/en/stable/index.html?utm_source=chatgpt.com "A Python package & command-line tool to gather text on the Web — Trafilatura 2.1.0 documentation"
[8]: https://playwright.dev/python/docs/intro?utm_source=chatgpt.com "Installation | Playwright Python"
[9]: https://arxiv.org/abs/2408.09869?utm_source=chatgpt.com "Docling Technical Report"
