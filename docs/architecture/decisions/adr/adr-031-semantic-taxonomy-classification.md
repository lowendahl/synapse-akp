# ADR-031: Semantic Taxonomy as Configurable Classification System

| Field | Value |
|-------|-------|
| **ID** | `ADR-031` |
| **Status** | Accepted |
| **Date** | 2026-07-26 |
| **Decision Makers** | Patrik Lowendahl |
| **Related** | ADR-016 (domain-agnostic), ADR-018 (unified pipeline) |

## Context

The semantic pipeline must classify extracted candidates into entity types (DomainConcept, Measure, Indicator, KPI, etc.). Two questions arise:

1. **Where does the type system live?** Hardcoded in Python code (violates ADR-016) or in external configuration?
2. **How specific should types be?** A flat list of 5 types vs. a hierarchical taxonomy with subtypes?

### Requirements

- Types must be **extensible per corpus** — a financial corpus may need "Asset", "Liability" subtypes that a healthcare corpus does not.
- Types must be **machine-readable** — the LLM adapter needs them as classification labels.
- Types must be **stable across compilations** — adding a subtype must not reclassify existing entities.
- The framework must ship with a **default taxonomy** that works for any knowledge corpus.

### Options Evaluated

| Option | Pros | Cons |
|--------|------|------|
| **A. Hardcoded Python enum** | Type-safe, IDE autocomplete | Violates ADR-016; requires code changes to extend |
| **B. Flat YAML list** | Simple, extensible | No hierarchy; no subtype reasoning |
| **C. Hierarchical YAML taxonomy (chosen)** | Extensible, hierarchical, domain-agnostic | Slightly more complex to parse |

## Decision

Entity classification uses a **hierarchical YAML taxonomy file** (`semantic-taxonomy.yaml`) that is:

1. **Shipped as a default** — the framework provides a base taxonomy.
2. **Overridable per corpus** — OKF libraries can provide their own taxonomy that extends or replaces the default.
3. **Used by the LLM adapter** — taxonomy labels and descriptions are injected into classification prompts.
4. **Versioned** — taxonomy changes produce a new version; entities retain their classification version.

### Default Taxonomy Structure

```yaml
entity_types:
  - id: DomainConcept
    description: "A named concept within the domain vocabulary"
    subtypes:
      - id: Process
      - id: Outcome
      - id: Role
      - id: Artifact
      - id: State
      - id: Event

  - id: Measure
    description: "A quantifiable property that can be observed or calculated"
    subtypes:
      - id: BaseMeasure
      - id: DerivedMeasure
      - id: CalculatedMeasure

  - id: Indicator
    description: "A measure used to indicate, evaluate, or predict a state"
    subtypes:
      - id: LeadingIndicator
      - id: LaggingIndicator
      - id: DiagnosticIndicator

  - id: KPI
    description: "A governed indicator with target, owner, and cadence"

  - id: Objective
    description: "A desired outcome or goal"

  - id: Target
    description: "A quantified threshold for a KPI"

  - id: Dimension
    description: "A categorical axis for slicing measures"
```

### Configuration Loading

1. Compiler loads `compiler/config/semantic-taxonomy.yaml` as the base.
2. If the OKF corpus contains `corpus/config/semantic-taxonomy.yaml`, it is merged (corpus entries override base).
3. The merged taxonomy is passed to all stages that need classification labels.

## Consequences

- No entity type is hardcoded in Python — all types come from YAML configuration.
- LLM classification prompts are dynamically built from the taxonomy (no prompt drift when types change).
- Corpus authors can extend the taxonomy for their domain without touching framework code.
- Classification results store the taxonomy version for reproducibility.
- The stoplist (`semantic-stoplist.yaml`) prevents common false-positive terms from being classified.
