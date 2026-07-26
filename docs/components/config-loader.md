# Component: Config Loader

## Module

`akp_runtime.infrastructure.config_loader`

## Purpose

Load and merge runtime configuration from multiple sources into a validated
`RuntimeConfigModel`. Provides a single, deterministic configuration object
that the bootstrap pipeline uses to initialize the runtime.

## Responsibilities

1. **Load YAML configuration** — read a `config.yaml` file from disk.
2. **Apply environment variable overrides** — `AKP_*` prefixed env vars
   override YAML values.
3. **Apply precedence** — env vars > YAML file > defaults (Pydantic defaults).
4. **Resolve pack paths** — relative paths resolved against config file directory.
5. **Validate configuration** — produce a typed `RuntimeConfigModel` or fail.
6. **Support explicit config path** — caller may pass a specific path.
7. **Support auto-discovery** — search current directory and `~/.akp/` for config.

## Out of Scope

- **Pack validation** — handled by pack loader.
- **Runtime lifecycle** — handled by `pipeline/bootstrap.py`.
- **MCP server setup** — handled by `consumer/mcp_server.py`.
- **Secret management** — env vars only; no vault integration.

## Promises

1. **P-PRECEDENCE**: Environment variables ALWAYS override YAML values which
   ALWAYS override Pydantic defaults. This order is guaranteed.
2. **P-VALIDATED**: The returned model is fully validated by Pydantic.
   Invalid values raise `ConfigurationError`.
3. **P-PROTOCOL**: The implementation MUST satisfy the `ConfigLoader` protocol.
4. **P-RESOLVE-PATHS**: Pack paths are resolved to absolute paths relative to
   the config file's parent directory.
5. **P-MISSING-OK**: If no config file is found and no explicit path given,
   return defaults (no packs loaded, embeddings enabled, default limits).
6. **P-ENV-PREFIX**: Only `AKP_` prefixed environment variables are read.
   Unknown env vars are ignored.
7. **P-DETERMINISTIC**: Same inputs (file + env) → same output model.

## Invariants

1. **INV-NO-SIDE-EFFECTS**: Loading config MUST NOT modify the filesystem,
   environment, or any global state.
2. **INV-LAYER-BOUNDARY**: This module imports ONLY from `contracts/`.
   It MUST NOT import from `domain/`, `operations/`, `pipeline/`, or `consumer/`.
3. **INV-SINGLE-RESPONSIBILITY**: This module handles ONLY configuration.
   No database connections, no embedding initialization.

## Dependencies

- `pyyaml` — YAML parsing
- `akp_runtime.contracts.mcp_models` — `RuntimeConfigModel`, `PackBindingModel`
- `akp_runtime.contracts.errors` — `ConfigurationError`

## Testing Strategy

- **Unit tests**: YAML parsing, env override, path resolution, defaults.
- **Validation tests**: Invalid YAML, missing required pack fields, bad types.
- **Precedence tests**: Env overrides YAML overrides defaults.
- **Path resolution tests**: Relative and absolute paths, missing directories.
- **Protocol compliance**: `isinstance(impl, ConfigLoader)` passes.
