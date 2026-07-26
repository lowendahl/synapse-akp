"""Configuration loading with precedence: env vars → YAML file → model defaults."""

from __future__ import annotations

from pathlib import Path

from akp_runtime.contracts.mcp_models import PackBindingModel, RuntimeConfigModel


class YamlConfigLoader:
    """Loads runtime configuration from env, YAML, and defaults."""

    def load(self, config_path: Path | None = None) -> RuntimeConfigModel:
        """Load config with precedence: env vars → YAML → defaults."""
        raise NotImplementedError("PBI #12")
