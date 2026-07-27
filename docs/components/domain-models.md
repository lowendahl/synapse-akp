# Component: Domain Models

## Purpose
The domain-models component defines the immutable and validated knowledge structures that move through the compiler and runtime. It captures authored object structure, ontology rules, retrieval-quality rules, pack metadata, provenance, and result value objects without mixing in storage or transport concerns.

## Modules Covered
- `kp_compiler.domain.__init__` — domain package marker
- `kp_compiler.domain.models` — compatibility facade for canonical compiler domain types
- `kp_compiler.domain.core_models` — relationships, sections, provenance, and semantic units
- `kp_compiler.domain.enumerations` — compiler vocabularies such as `ObjectType` and `Origin`
- `kp_compiler.domain.knowledge_objects` — canonical compiler intermediate-representation objects
- `kp_compiler.domain.ontology` — ontology specification and validation helpers
- `kp_compiler.domain.rules` — alias rules, quality thresholds, and pack rules
- `kp_compiler.domain.assertions` — declarative outcome assertion models
- `akp_runtime.domain.__init__` — domain package marker
- `akp_runtime.domain.models` — compatibility facade for canonical runtime domain types
- `akp_runtime.domain.pack_metadata` — validated pack manifest value object
- `akp_runtime.domain.search_results` — immutable search-hit, unit, and graph-edge results
- `akp_runtime.domain.provenance_models` — immutable provenance-step and metadata-freezing primitives
- `akp_runtime.domain.provenance` — provenance chain assembly helpers

## Responsibilities
- Represent compiled knowledge objects and semantic units with explicit typing
- Represent ontology rules and field requirements as in-memory specifications
- Represent retrieval-quality and alias-quality assertions as declarative models
- Represent runtime pack identity, provenance, and retrieval results as immutable value objects
- Provide compatibility facades so callers can import stable names while canonical modules remain focused

## Out of Scope
- Filesystem access
- DuckDB reads or writes
- Search fusion mathematics
- MCP transport concerns

## Promises
- **P-DOMAIN-001**: Compiler `KnowledgeObject` models forbid undeclared fields.
- **P-DOMAIN-002**: Core compiler structures (`Relationship`, `Section`, `Provenance`, `SemanticUnit`) are frozen value objects.
- **P-DOMAIN-003**: `Ontology.from_dict(...)` constructs all type and predicate specifications from parsed YAML data without performing IO.
- **P-DOMAIN-004**: `PackRules.default()` returns a fully populated deterministic default ruleset.
- **P-DOMAIN-005**: Runtime provenance metadata is frozen into immutable mappings, with list values normalized to tuples.
- **P-DOMAIN-006**: Runtime search and graph results carry typed provenance rather than unstructured dictionaries.

## Invariants
- **INV-DOMAIN-001**: Domain modules do not read files, open databases, or start transports.
- **INV-DOMAIN-002**: Compatibility facades only re-export canonical types; they do not redefine business structure.
- **INV-DOMAIN-003**: Ontology, rules, and provenance logic remain in the domain layer, not infrastructure.

## Dependencies
- `pydantic`
- Standard library dataclasses, enums, regex, and typing

## Dependents
- Compiler stages
- Runtime operations
- Contracts and infrastructure adapters
