"""Configuration loading with precedence: env vars → YAML file → model defaults.

What: Loads runtime configuration from YAML + env overrides.
Why: Single deterministic config source for the runtime bootstrap.
Contracts: Implements ConfigLoader protocol.
Boundaries: Only imports from contracts/.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from akp_runtime.contracts.errors import ConfigurationError
from akp_runtime.contracts.mcp_models import RuntimeConfigModel

_ENV_PREFIX = "AKP_"

_BOOL_TRUTHY = frozenset({"true", "1", "yes"})
_BOOL_FALSY = frozenset({"false", "0", "no"})


def _parse_env_value(key: str, value: str) -> str | int | float | bool:
    """Attempt to parse env var values to appropriate types."""
    lower = value.lower()
    if lower in _BOOL_TRUTHY:
        return True
    if lower in _BOOL_FALSY:
        return False
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


def _collect_env_overrides() -> dict[str, Any]:
    """Collect AKP_ prefixed env vars as config overrides."""
    overrides: dict[str, Any] = {}
    for key, value in os.environ.items():
        if key.startswith(_ENV_PREFIX):
            config_key = key[len(_ENV_PREFIX) :].lower()
            overrides[config_key] = _parse_env_value(config_key, value)
    return overrides


def _resolve_pack_paths(packs: list[dict[str, Any]], base_dir: Path) -> list[dict[str, Any]]:
    """Resolve relative pack paths against the config file's parent directory."""
    resolved = []
    for pack in packs:
        p = pack.get("path", "")
        path = Path(p)
        if not path.is_absolute():
            path = base_dir / path
        pack_copy = dict(pack)
        pack_copy["path"] = path
        resolved.append(pack_copy)
    return resolved


class YamlConfigLoader:
    """Loads runtime configuration from env, YAML, and defaults.

    Precedence: env vars (AKP_*) > YAML file > Pydantic defaults.
    """

    def load(self, config_path: Path | None = None) -> RuntimeConfigModel:
        """Load config with precedence: env vars → YAML → defaults."""
        yaml_data: dict[str, Any] = {}
        base_dir = Path.cwd()

        if config_path is not None:
            if not config_path.exists():
                raise ConfigurationError(
                    source=str(config_path),
                    violation=f"Config file not found: {config_path}",
                )
            yaml_data = self._load_yaml(config_path)
            base_dir = config_path.parent
        else:
            # Auto-discovery: check cwd and ~/.akp/
            for candidate in [Path.cwd() / "config.yaml", Path.home() / ".akp" / "config.yaml"]:
                if candidate.exists():
                    yaml_data = self._load_yaml(candidate)
                    base_dir = candidate.parent
                    break

        # Resolve pack paths
        if "packs" in yaml_data:
            yaml_data["packs"] = _resolve_pack_paths(yaml_data["packs"], base_dir)

        # Apply env overrides (env > YAML > defaults)
        env_overrides = _collect_env_overrides()
        merged = {**yaml_data, **env_overrides}

        # Remove 'packs' from env overrides — packs only come from YAML
        if "packs" in yaml_data and "packs" not in env_overrides:
            merged["packs"] = yaml_data["packs"]

        try:
            return RuntimeConfigModel(**merged)
        except ValidationError as e:
            raise ConfigurationError(
                source=str(config_path or "merged config"),
                violation=str(e),
            ) from e

    def _load_yaml(self, path: Path) -> dict[str, Any]:
        """Parse YAML file, raising ConfigurationError on failure."""
        try:
            text = path.read_text(encoding="utf-8")
            data = yaml.safe_load(text)
        except yaml.YAMLError as e:
            raise ConfigurationError(
                source=str(path),
                violation=f"YAML parse error: {e}",
            ) from e

        if data is None:
            return {}
        if not isinstance(data, dict):
            raise ConfigurationError(
                source=str(path),
                violation="Config must be a YAML mapping (dict), not a scalar or list",
            )
        return data
