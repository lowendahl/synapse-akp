# Component: Pipeline

## Purpose
The pipeline component is the orchestration and composition root for both compile-time and runtime flows. It is where stage ordering, adapter wiring, failure gates, lifecycle ownership, and shutdown guarantees are centralized so domain and infrastructure code remain decoupled.

## Modules Covered
- `kp_compiler.pipeline.__init__` — compiler pipeline package marker
- `kp_compiler.pipeline.compiler` — compilation orchestration, semantic-unit and alias projection assembly, and stage/event sequencing
- `akp_runtime.pipeline.__init__` — runtime pipeline package marker
- `akp_runtime.pipeline.bootstrap` — runtime lifecycle context, signal handling, startup delegation, and guaranteed shutdown path

## Responsibilities
- Instantiate concrete compiler adapters and invoke stages in order
- Enforce fail-before-write behavior when diagnostics contain errors
- Assemble semantic units, alias registry entries, and pack manifest metadata
- Emit compile-time and runtime lifecycle events
- Own runtime startup and cleanup semantics through `RuntimeContext`

## Out of Scope
- Implementing stage internals
- Defining domain models or transport contracts
- Authoring source knowledge
- Embedding inline SQL outside designated infrastructure boundaries

## Promises
- **P-PIPE-001**: Compiler stage execution order is fixed and deterministic for the same inputs.
- **P-PIPE-002**: Pack writing occurs only after the diagnostics error gate passes.
- **P-PIPE-003**: The compiler pipeline is the only place concrete compiler adapters are instantiated.
- **P-PIPE-004**: `RuntimeContext.__exit__` guarantees shutdown emission when the context was entered successfully.
- **P-PIPE-005**: Runtime bootstrap installs `SIGTERM` and `SIGINT` handlers before serving.

## Invariants
- **INV-PIPE-001**: Pipeline modules orchestrate existing components rather than owning domain logic.
- **INV-PIPE-002**: Compilation preserves a single fail-fast gate before artifact mutation.
- **INV-PIPE-003**: Runtime lifecycle ownership is centralized in `RuntimeContext` rather than scattered across consumers.

## Dependencies
- Compiler stages, events, and infrastructure adapters
- Runtime events and infrastructure adapters
- Standard library lifecycle and signal utilities

## Dependents
- Compiler CLI
- Runtime consumer entry surfaces
- Integration tests exercising end-to-end flows
