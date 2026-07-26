# AKP Registry

## Purpose

Store, version, and distribute AKP packages.

## Responsibilities

- Publish packages
- Retrieve packages
- List versions
- Resolve dependencies
- Verify signatures
- Deprecate packages
- Revoke packages
- Promote packages between environments
- Record lineage

## Out of Scope

- Compilation
- Runtime serving
- Knowledge authoring

## Promises

- Immutable released versions
- Dependency resolution support
- Trust verification support

## Invariants

- A published version is never overwritten
- Revoked packages are rejected by production runtimes
