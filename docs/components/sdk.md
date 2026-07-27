# Component: AKP SDK

## Purpose
The SDK component defines the authoring-time developer experience around AKP: scaffolding, local feedback loops, validation, and publish readiness. In this repository it is primarily an architectural boundary expressed through compiler and consumer entry points rather than a dedicated implementation package.

## Modules Covered
- _No repository source modules implement a separate SDK package yet; current SDK behavior is composed from compiler and consumer entry surfaces._

## Responsibilities
- Define the expected workflow for authors and knowledge engineers
- Provide the architectural home for scaffolding, local build, and validation tooling
- Keep publish-time checks upstream of registry distribution

## Out of Scope
- Runtime hosting
- Business application logic
- Registry storage internals

## Promises
- **P-SDK-001**: Local author workflows are expected to compile and validate before publish.
- **P-SDK-002**: The SDK boundary targets the stable AKP format rather than ad hoc pack layouts.
- **P-SDK-003**: Author tooling remains distinct from runtime hosting.

## Invariants
- **INV-SDK-001**: Publish readiness depends on validation gates, not manual inspection alone.
- **INV-SDK-002**: Authoring workflows consume the same compiler and consumer contracts used by automation.
- **INV-SDK-003**: SDK concerns remain upstream of registry and runtime boundaries.

## Dependencies
- Compiler and consumer entry surfaces
- Architecture doctrine for workflow and governance

## Dependents
- Knowledge authors
- CI pipelines enforcing build readiness
- Future scaffolding and publish tools
