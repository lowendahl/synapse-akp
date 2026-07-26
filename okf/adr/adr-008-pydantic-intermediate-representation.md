---
type: ADR
title: "ADR-008 — Pydantic Domain Objects as Compiler Intermediate Representation"
id: adr.008
status: accepted
date: 2026-07-25
decision_makers: [plwendahl]
tags: [adr, pydantic, compiler, intermediate-representation, typing]
---

# ADR-008 — Pydantic Domain Objects as Compiler Intermediate Representation

## Status

**Accepted** — 2026-07-25

## Context

The compiler pipeline needs a typed, validated intermediate representation between raw Markdown parsing and graph construction. The SDD (§11.3, OADR-KP-014) identifies the need for a "normalized compiler model" — the canonical intermediate representation that all downstream stages consume.

Without a formal IR:
- Parser output is untyped dicts/strings — runtime errors surface late
- Ontology validation requires ad-hoc field checks
- NetworkX node properties are unstructured — no IDE support, no autocomplete
- Serialization/deserialization is manual and fragile
- Testing individual pipeline stages is difficult

## Decision

The compiler SHALL use **Pydantic v2 models** as the canonical intermediate representation.

### Full Pipeline

```
Markdown + YAML frontmatter
        │
        ▼
     Parser
        │  (extracts frontmatter, headings, links, body)
        ▼
  Pydantic Domain Objects
        │  (typed, validated, schema-enforced)
        ▼
  NetworkX Property Graph
        │
        ├── Graph validation
        ├── Ontology validation
        ├── Relationship inference
        ├── Orphan detection
        ├── Cycle detection
        └── Semantic enrichment
        │
        ▼
  Graph Projection
        │
        ├── Node table (DuckDB)
        ├── Edge table (DuckDB)
        ├── GraphML (optional export)
        ├── Neo4j export (optional)
        └── JSON (optional export)
        │
        ▼
  Knowledge Pack (.duckdb)
```

### Pydantic Models (representative)

```python
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class ObjectType(str, Enum):
    FRAMEWORK = "Framework"
    METRIC = "Metric"
    ROLE = "Role"
    PROCESS = "Process"
    DOCTRINE = "Doctrine"
    PROGRAM = "Program"
    EVIDENCE_SOURCE = "Evidence Source"
    STAGE = "Stage"
    ORGANIZATION = "Organization"
    RISK = "Risk"
    PLANNING = "Planning"
    OUTCOME = "Outcome"
    ADR = "ADR"
    INDEX = "Index"
    LOG = "Log"

class Origin(str, Enum):
    AUTHORED = "authored"
    DERIVED = "derived"
    INFERRED = "inferred"
    GENERATED = "generated"

class Relationship(BaseModel):
    subject_id: str
    predicate: str
    object_id: str
    origin: Origin
    confidence: Optional[float] = None
    source_document: Optional[str] = None

class KnowledgeObject(BaseModel):
    id: str                          # stable canonical ID
    type: ObjectType
    title: str
    description: Optional[str] = None
    aliases: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    domain: str                      # "csu" or "mcem"
    status: str = "stable"
    source_path: str                 # OKF file path (provenance)
    source_revision: Optional[str] = None
    relationships: list[Relationship] = Field(default_factory=list)
    body_sections: list["Section"] = Field(default_factory=list)
    properties: dict = Field(default_factory=dict)  # type-specific fields

class Section(BaseModel):
    heading: str
    level: int
    content: str
    semantic_unit_id: Optional[str] = None

class MetricObject(KnowledgeObject):
    """Extended model for Metric type objects."""
    formula: Optional[str] = None
    classification: Optional[str] = None  # leading | lagging | diagnostic
    thresholds: Optional[dict] = None
    measurement_paradigm: Optional[str] = None  # snapshot | realtime
    evidence_sources: list[str] = Field(default_factory=list)

class EvidenceSourceObject(KnowledgeObject):
    """Extended model for Evidence Source type objects."""
    platform: Optional[str] = None
    access_pattern: Optional[str] = None
    artifact_ids: list[str] = Field(default_factory=list)
```

### What Pydantic Provides

| Capability | How It Helps |
|------------|--------------|
| **Type validation** | Invalid frontmatter fails immediately with clear error |
| **Schema enforcement** | Required fields caught at parse time, not graph time |
| **Serialization** | `.model_dump()` → JSON/dict for DuckDB insertion |
| **IDE support** | Autocomplete, type checking in compiler code |
| **Discriminated unions** | Different models for Metric vs Role vs Framework |
| **Custom validators** | ID format, predicate allowlist, alias uniqueness |
| **Testability** | Unit test each model independently |
| **Documentation** | Schema is self-documenting via model definitions |

### Relationship to NetworkX

Once Pydantic objects are validated, they are loaded into NetworkX:

```python
G = nx.DiGraph()

for obj in parsed_objects:
    G.add_node(obj.id, **obj.model_dump(exclude={"relationships", "body_sections"}))

for obj in parsed_objects:
    for rel in obj.relationships:
        G.add_edge(rel.subject_id, rel.object_id,
                   predicate=rel.predicate,
                   origin=rel.origin,
                   confidence=rel.confidence)
```

NetworkX then operates on the validated, typed data — no raw strings, no missing fields, no surprises.

## Consequences

- **Parse errors surface early** — malformed frontmatter fails at Pydantic validation, not during graph construction.
- **Ontology is code** — the `ObjectType` and predicate enums ARE the ontology (derived from `ontology.yaml`).
- **Type-specific logic is clean** — `MetricObject` has formula/thresholds; `EvidenceSourceObject` has platform/artifact_ids.
- **Compiler is testable** — each stage operates on well-typed inputs/outputs.
- **Schema evolution is explicit** — adding a field to a Pydantic model is a visible, reviewable change.
- **Serialization is free** — `.model_dump()` produces the exact dict for DuckDB insertion.
- **Pydantic v2 is fast** — Rust-backed validation; handles our corpus in <1 second.

## Alternatives Considered

| Alternative | Why Not Selected |
|-------------|-----------------|
| Plain dicts | No validation; runtime KeyError; no IDE support |
| dataclasses | No built-in validation; no serialization; weaker schema |
| attrs | Good but less ecosystem; no JSON Schema generation |
| TypedDict | Type hints only; no runtime validation |
| Custom IR classes | Reinventing Pydantic without the ecosystem |
| Skip IR — parse directly to NetworkX | Loses typed validation layer; harder to test/debug |
