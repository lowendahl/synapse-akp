# ADR-035: Generated Source Layers and Content Precedence

| Field | Value |
|-------|-------|
| **ID** | `ADR-035` |
| **Status** | Accepted |
| **Date** | 2026-07-26 |
| **Decision Makers** | Patrik Lowendahl |
| **Related** | ADR-018 (unified pipeline), ADR-020 (assertion confidence) |

## Context

The semantic compiler generates concept definitions, measure descriptions, and relationship maps that did not exist in the original corpus. These generated artifacts must coexist with:

1. **Authored content** — written by humans directly in the OKF corpus.
2. **Reviewed content** — generated content that has been reviewed and approved by a human.
3. **Inferred content** — machine-generated, not yet reviewed.

Without clear precedence rules:
- Generated content could overwrite human-authored definitions on recompilation.
- Reviewed corrections could be lost when the compiler re-runs.
- Users cannot distinguish authoritative definitions from machine suggestions.

### Options Evaluated

| Option | Pros | Cons |
|--------|------|------|
| **A. Single output directory, overwrite on compile** | Simple | Loses human edits; no provenance |
| **B. Separate directories with manual merge** | Safe | Poor UX; merge conflicts |
| **C. Layered source system with strict precedence (chosen)** | Clear authority; no data loss; auditable | More complex file layout |

## Decision

Content is organized into **three source layers** with strict precedence:

```
reviewed > authored > generated
```

### Layer Definitions

| Layer | Location | Written By | Authority |
|-------|----------|-----------|-----------|
| **generated** | `corpus/generated/` | Compiler | Lowest — suggestions only |
| **authored** | `corpus/` (main tree) | Humans | Middle — explicit domain knowledge |
| **reviewed** | `corpus/reviewed/` | Humans (from review queue) | Highest — corrected/approved facts |

### Precedence Rules

1. **Generated content never overwrites authored or reviewed content.**
2. **Reviewed content always wins** — if a reviewed definition exists, it overrides both authored and generated.
3. **Authored content overrides generated** — if a human writes a concept definition, the compiler does not regenerate it.
4. **Generated content is idempotent** — re-running the compiler produces the same generated files (given the same corpus input).
5. **Deleted generated files are regenerated** — they are compiler output, not human artifacts.
6. **Reviewed files are never touched by the compiler** — they are human-owned.

### File Layout

```
corpus/
├── concepts/                  # Authored by humans
│   └── delivery-coverage.md
├── generated/
│   ├── concepts/              # Compiler-generated concept files
│   │   └── unified-delivery-coverage.md
│   ├── measures/              # Compiler-generated measure definitions
│   ├── indicators/            # Compiler-generated indicator descriptions
│   └── assertions.jsonl       # All inferred assertions
├── reviewed/
│   ├── concepts/              # Human-approved/corrected concepts
│   └── assertions.jsonl       # Reviewed assertion overrides
└── config/
    └── semantic-config.yaml   # Confidence thresholds, layer behavior
```

### Front Matter Markers

Every generated file includes metadata:

```yaml
---
id: concept.unified-delivery-coverage
type: DomainConcept
source_layer: generated
generated: { by: kp-compiler, at: 2026-07-26T14:30:00Z, version: "2.1.0" }
confidence: 0.78
status: inferred
---
```

### Compilation Behavior

1. **Parse phase**: reads authored + reviewed layers as ground truth.
2. **Extraction phase**: discovers candidates from the full corpus (including generated, for relationship context).
3. **Generation phase**: writes to `corpus/generated/` only, never to `corpus/` or `corpus/reviewed/`.
4. **Conflict detection**: if a generated assertion contradicts a reviewed one, diagnostic SEM019 fires.

## Consequences

- Human work is never lost — the compiler only writes to `generated/`.
- Review workflow is clear: move items from `generated/` to `reviewed/` (or correct them).
- `git diff` on `corpus/generated/` shows exactly what changed between compilations.
- The runtime merges all three layers at query time, applying precedence.
- CI can validate that no file in `corpus/reviewed/` has been modified by automation.
