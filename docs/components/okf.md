# Component: OKF

## Purpose
OKF is the canonical authored-knowledge boundary for Synapse AKP. It defines how human-maintained Markdown, frontmatter metadata, ontology declarations, and pack manifests become compiler inputs while remaining reviewable, diffable, and explicit.

## Modules Covered
- `okf\**\*.md` — authored knowledge objects and semantic source content
- `okf\**\pack.yaml` — pack entry points, dependencies, and compile defaults
- `okf\ontology.yaml` — shared type and predicate contract
- `okf\pack-rules.yaml` — declarative retrieval-quality and alias-quality rules

## Responsibilities
- Provide the human-authored source of truth for knowledge content
- Declare stable IDs, types, aliases, tags, and relationships explicitly
- Define ontology constraints used by compiler validation
- Define per-pack compile defaults and quality assertions

## Out of Scope
- Compilation orchestration
- Runtime retrieval and serving
- Registry publication

## Promises
- **P-OKF-001**: Source files remain Git-friendly text artifacts.
- **P-OKF-002**: Relationships are expressed in metadata or authored links rather than inferred from file layout.
- **P-OKF-003**: Ontology and rules stay externalized as authored contracts, not hidden in code.

## Invariants
- **INV-OKF-001**: Canonical authored knowledge is separate from compiled AKP artifacts.
- **INV-OKF-002**: Stable IDs, titles, and types live in frontmatter rather than generated at runtime.
- **INV-OKF-003**: Pack entry points declare dependencies explicitly.

## Dependencies
- Human authors
- Source control and review workflow

## Dependents
- `kp_compiler.stages.parse`
- `kp_compiler.stages.validate`
- `kp_compiler.stages.discover_ontology`
- `kp_compiler.infrastructure.rules_loader`
