# Component: Stages

## Purpose
The stages component is the compiler's transformation pipeline below orchestration. Each stage owns one bounded transformation or validation concern—parsing, ontology enforcement, enrichment, graph construction, lexical indexing, embeddings, cross-pack validation, ontology discovery, or post-build outcome validation.

## Modules Covered
- `kp_compiler.stages.__init__` — stages package marker
- `kp_compiler.stages.alias_expander` — alias enrichment policy helpers
- `kp_compiler.stages.assertion_evaluator` — built-in outcome assertion evaluators
- `kp_compiler.stages.parse` — Markdown and frontmatter parsing into typed objects
- `kp_compiler.stages.duplicate_detector` — duplicate-detection stage helpers
- `kp_compiler.stages.enrichment_models` — enrichment-stage support models
- `kp_compiler.stages.frontmatter_extractor` — frontmatter extraction helper for parser flows
- `kp_compiler.stages.validate` — ontology and corpus validation diagnostics
- `kp_compiler.stages.enrich` — deterministic alias expansion and fuzzy-duplicate detection
- `kp_compiler.stages.graph` — graph construction, cycle detection, orphan detection, and metrics
- `kp_compiler.stages.bm25` — lexical corpus tokenization and BM25 indexing
- `kp_compiler.stages.embed` — semantic-unit embedding and USearch sidecar serialization
- `kp_compiler.stages.cross_pack` — cross-pack reference validation
- `kp_compiler.stages.knowledge_object_factory` — parser helper for typed knowledge-object creation
- `kp_compiler.stages.discover_ontology` — frontmatter-only ontology discovery and YAML generation
- `kp_compiler.stages.ontology_discovery_models` — ontology discovery support models
- `kp_compiler.stages.ontology_document_renderer` — ontology YAML document rendering
- `kp_compiler.stages.ontology_scanner` — ontology frontmatter scanner
- `kp_compiler.stages.outcome_validation_models` — outcome assertion result models
- `kp_compiler.stages.outcome_validator` — post-build quality assertions against the compiled pack
- `kp_compiler.stages.project.__init__` — reserved marker for project-specific stage extensions
- `kp_compiler.stages.project.queries.__init__` — project-stage query package facade
- `kp_compiler.stages.project.queries.pack_queries` — dependency-pack stage query objects
- `kp_compiler.stages.project.queries.outcome_queries` — outcome-validation stage query objects

## Responsibilities
- Convert authored Markdown into typed compiler IR
- Emit diagnostics for ontology, ID, predicate, and duplicate violations
- Enrich retrieval aliases without altering authored semantics
- Compile object relationships into graph projections and graph diagnostics
- Produce lexical and semantic retrieval projections
- Validate inter-pack references and retrieval-quality outcomes
- Discover and regenerate ontology declarations from corpus structure when requested

## Out of Scope
- CLI parsing
- Global lifecycle orchestration
- DuckDB pack writing
- Runtime search serving

## Promises
- **P-STAGE-001**: Parser stage separates frontmatter, sections, and authored relationships into typed objects.
- **P-STAGE-002**: Validation emits diagnostics without mutating the corpus.
- **P-STAGE-003**: Enrichment adds aliases only when they pass alias-quality gates.
- **P-STAGE-004**: Graph stage ignores unresolved markdown-path references when building graph edges.
- **P-STAGE-005**: BM25 indexing preserves semantic-unit order through `unit_ids`.
- **P-STAGE-006**: Embedding stage records input hashes alongside vectors for provenance.
- **P-STAGE-007**: Cross-pack validation checks only foreign-domain qualified IDs against dependency manifests.
- **P-STAGE-008**: Outcome validation sampling is deterministic through a fixed random seed.

## Invariants
- **INV-STAGE-001**: Stage modules expose typed inputs and outputs rather than raw ad hoc payloads.
- **INV-STAGE-002**: No stage writes the compiled DuckDB pack directly; projection persistence belongs to infrastructure.
- **INV-STAGE-003**: Ontology discovery performs a frontmatter scan rather than a full mutation of source content.

## Dependencies
- Compiler domain models
- Compiler contracts and diagnostics
- `networkx`, `bm25s`, `fastembed`, `usearch`, `rapidfuzz`, and YAML parsing libraries as needed by individual stages

## Dependents
- `kp_compiler.pipeline.compiler`
- Compiler integration and property-based tests
