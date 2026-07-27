# Component: Config Loader

## Purpose
The config loader converts YAML files, environment overrides, and model defaults into a single validated `RuntimeConfigModel`. It is the runtime's deterministic configuration boundary and keeps configuration parsing out of bootstrap and operations code.

## Modules Covered
- `akp_runtime.infrastructure.config_loader` — YAML parsing, `AKP_` environment overrides, path resolution, and validation

## Responsibilities
- Load `config.yaml` from an explicit path or standard discovery locations
- Merge configuration sources with precedence `environment > YAML > defaults`
- Resolve relative pack paths against the configuration file location
- Validate the merged configuration into `RuntimeConfigModel`
- Translate malformed configuration into typed runtime errors

## Out of Scope
- Pack schema validation
- Runtime lifecycle management
- MCP server setup
- Secret vault integration

## Promises
- **P-CONFIG-001**: Only `AKP_`-prefixed environment variables participate in overrides.
- **P-CONFIG-002**: Environment overrides take precedence over YAML, which takes precedence over model defaults.
- **P-CONFIG-003**: Relative pack paths in YAML are rewritten relative to the config file directory.
- **P-CONFIG-004**: Missing auto-discovered config files fall back to defaults rather than failing.
- **P-CONFIG-005**: Invalid YAML or invalid merged values raise `ConfigurationError` with source context.

## Invariants
- **INV-CONFIG-001**: Configuration loading performs no writes to the filesystem or environment.
- **INV-CONFIG-002**: This component imports only runtime contracts and standard parsing libraries.
- **INV-CONFIG-003**: Bootstrap receives a fully validated model rather than raw dictionaries.

## Dependencies
- `akp_runtime.contracts.mcp_models`
- `akp_runtime.contracts.errors`
- `yaml` and `pydantic`

## Dependents
- `akp_runtime.pipeline.bootstrap`
- Runtime startup automation
