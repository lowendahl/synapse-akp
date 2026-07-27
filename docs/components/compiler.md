# Component: AKP Compiler

## Purpose
The compiler component is the public entry surface for turning OKF sources into immutable Knowledge Packs. It owns package identity, manifest-aware CLI behavior, rules loading, and delegation into the compilation pipeline without embedding stage logic in the entry layer.

## Modules Covered
- `kp_compiler.__init__` — package identity and compiler version contract
- `kp_compiler.__main__` — `python -m kp_compiler` entry point
- `kp_compiler.cli` — `kp-compile` argument parsing, manifest default resolution, and process exit behavior
- `kp_compiler.pipeline.compiler` — orchestration entry point
- `kp_compiler.pipeline.compilation_preparation` — discovery, ontology loading, and parsing coordination
- `kp_compiler.pipeline.compilation_projection` — validation, enrichment, graph, and retrieval projection coordination
- `kp_compiler.pipeline.compilation_persistence` — pack writing, manifest emission, and outcome reporting
- `kp_compiler.pipeline.semantic_unit_builder` — semantic-unit construction
- `kp_compiler.pipeline.alias_registry_builder` — alias-registry construction

## Responsibilities
- Expose the compiler package version used in build manifests
- Parse CLI arguments for compilation, ontology discovery, rules, and dependency packs
- Resolve `pack.yaml` defaults before invoking the pipeline
- Load declarative pack rules and pass them into orchestration
- Convert pipeline success or failure into shell exit codes

## Out of Scope
- Parsing Markdown sources
- Validating ontology semantics
- Writing DuckDB artifacts
- Serving compiled packs at runtime

## Promises
- **P-COMP-001**: Explicit CLI flags override `pack.yaml` defaults when both are present.
- **P-COMP-002**: Missing source or ontology inputs fail before `compile_pack(...)` is invoked.
- **P-COMP-003**: The compiler exits with `0` only when `compile_pack(...)` reports success.
- **P-COMP-004**: `kp_compiler.__main__` delegates to a single CLI entry path rather than duplicating compile logic.

## Invariants
- **INV-COMP-001**: Root compiler modules remain thin orchestration surfaces and do not implement stage logic.
- **INV-COMP-002**: The compiler version published by `kp_compiler.__version__` is the version propagated into compilation metadata.
- **INV-COMP-003**: Entry-surface modules may depend on pipeline and infrastructure, but pipeline stages do not depend back on the entry surface.

## Dependencies
- `kp_compiler.pipeline.compiler`
- `kp_compiler.infrastructure.rules_loader`
- `ruamel.yaml`
- `argparse` and `pathlib`

## Dependents
- CI build jobs
- Local authors running `kp-compile`
- SDK and automation wrappers
