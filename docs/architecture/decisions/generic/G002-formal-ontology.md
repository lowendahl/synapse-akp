---
type: ADR
title: "ADR-002 — Formal Ontology Extracted from Corpus"
id: adr.002
status: accepted
date: 2026-07-25
decision_makers: [plwendahl]
tags: [adr, ontology, validation, schema]
---

# ADR-002 — Formal Ontology Extracted from Corpus

## Status

**Accepted** — 2026-07-25

## Context

The SDD (§8.8, KP-13, ADR-KP-005) requires an explicit ontology that defines allowed object types, predicates, required fields, and constraints. The compiler must reject unknown types or predicates.

Our OKF corpus currently uses ~15 distinct `type` values in frontmatter (Framework, Metric, Role, Process, Evidence Source, Doctrine, Program, Index, Stage, Organization, Risk, Planning, Outcome, ADR, etc.). These emerged organically during authoring. There is no formal schema governing them.

## Decision

1. A formal `ontology.yaml` SHALL be created at `okf/ontology.yaml`.
2. The ontology SHALL be extracted from the current corpus types (codifying existing practice).
3. The ontology SHALL define:
   - allowed object types and their required/optional frontmatter fields;
   - allowed relationship predicates (e.g., `references`, `measures`, `belongs_to`, `depends_on`, `causes`);
   - cardinality constraints where applicable;
   - the ontology version (semver).
4. The Knowledge Compiler SHALL validate every source file against the ontology before compilation proceeds.
5. Unknown types or predicates SHALL fail the build (not silently accepted).
6. The ontology is versioned independently of pack versions.

## Consequences

- A one-time extraction pass produces `ontology.yaml` from current corpus types.
- Any future type addition requires an ontology update (governed change).
- Both MCEM and CSU packs compile against the SAME ontology (shared contract).
- Build failures surface immediately when authors use invalid types.
- The ontology becomes a prerequisite dependency for both pack builds.

## Ontology Scope (Initial)

Object types (expected initial set):

```
Framework, Stage, Methodology, Organization, Role, Process,
Metric, Doctrine, Program, Outcome, Evidence Source, Risk,
Planning, Index, ADR, Log
```

Predicate types (expected initial set):

```
references, measures, belongs_to, depends_on, causes,
operationalizes, extends, contains, supersedes, causal_signal
```

## Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| No formal ontology — free-form types | Violates KP-13; no validation possible |
| Ontology per pack | Fragments type system; cross-pack refs break |
| Schema-on-read (validate at query time) | Violates KP-12 (silent failures); defects propagate |
