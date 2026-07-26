"""Unit tests for Config Loader.

Tests validate component promises and invariants from docs/components/config-loader.md:
- P-PRECEDENCE: env > YAML > defaults
- P-VALIDATED: Invalid values raise ConfigurationError
- P-PROTOCOL: Satisfies ConfigLoader protocol
- P-RESOLVE-PATHS: Relative paths resolved against config directory
- P-MISSING-OK: No config file → defaults
- P-ENV-PREFIX: Only AKP_ prefixed env vars read
- P-DETERMINISTIC: Same input → same output
- INV-NO-SIDE-EFFECTS: No filesystem/env mutation
- INV-LAYER-BOUNDARY: Only imports from contracts/
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from akp_runtime.contracts.errors import ConfigurationError
from akp_runtime.contracts.mcp_models import RuntimeConfigModel
from akp_runtime.contracts.protocols import ConfigLoader
from akp_runtime.infrastructure.config_loader import YamlConfigLoader

# ─── Fixtures ────────────────────────────────────────────────────────────────


MINIMAL_YAML = """\
server_name: test-runtime
default_limit: 15
packs:
  - pack_id: test.domain.pack
    path: ./packs/test.duckdb
    required: true
"""

FULL_YAML = """\
server_name: full-runtime
default_limit: 20
lexical_k: 30
semantic_k: 30
graph_boost_top_n: 5
graph_boost_value: 0.2
rrf_k: 80
max_hops: 4
embeddings_enabled: false
packs:
  - pack_id: test.domain.alpha
    path: ./alpha.duckdb
    required: true
  - pack_id: test.domain.beta
    path: /absolute/beta.duckdb
    required: false
"""


@pytest.fixture()
def config_file(tmp_path: Path) -> Path:
    """Write a minimal config YAML and return its path."""
    cfg = tmp_path / "config.yaml"
    cfg.write_text(MINIMAL_YAML, encoding="utf-8")
    return cfg


@pytest.fixture()
def full_config_file(tmp_path: Path) -> Path:
    """Write a full config YAML and return its path."""
    cfg = tmp_path / "config.yaml"
    cfg.write_text(FULL_YAML, encoding="utf-8")
    return cfg


# ─── P-PROTOCOL: Satisfies ConfigLoader ─────────────────────────────────────


class TestProtocol:
    """P-PROTOCOL: YamlConfigLoader satisfies ConfigLoader protocol."""

    def test_isinstance_config_loader(self) -> None:
        loader = YamlConfigLoader()
        assert isinstance(loader, ConfigLoader)


# ─── P-MISSING-OK: No config file → defaults ────────────────────────────────


class TestDefaults:
    """P-MISSING-OK: Without a config file, returns defaults."""

    def test_no_config_returns_defaults(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        # Clear any AKP_ env vars
        for key in list(os.environ):
            if key.startswith("AKP_"):
                monkeypatch.delenv(key, raising=False)
        loader = YamlConfigLoader()
        config = loader.load(None)
        assert isinstance(config, RuntimeConfigModel)
        assert config.server_name == "akp-runtime"
        assert config.default_limit == 10
        assert config.packs == []

    def test_explicit_nonexistent_path_raises(self, tmp_path: Path) -> None:
        """Explicit path that doesn't exist → ConfigurationError."""
        loader = YamlConfigLoader()
        with pytest.raises(ConfigurationError):
            loader.load(tmp_path / "nonexistent.yaml")


# ─── P-PRECEDENCE: env > YAML > defaults ────────────────────────────────────


class TestPrecedence:
    """P-PRECEDENCE: Environment variables override YAML override defaults."""

    def test_yaml_overrides_defaults(self, config_file: Path) -> None:
        loader = YamlConfigLoader()
        config = loader.load(config_file)
        assert config.server_name == "test-runtime"
        assert config.default_limit == 15

    def test_env_overrides_yaml(self, config_file: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AKP_DEFAULT_LIMIT", "25")
        loader = YamlConfigLoader()
        config = loader.load(config_file)
        assert config.default_limit == 25

    def test_env_overrides_defaults(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("AKP_SERVER_NAME", "env-runtime")
        loader = YamlConfigLoader()
        config = loader.load(None)
        assert config.server_name == "env-runtime"

    def test_env_bool_parsing(self, config_file: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AKP_EMBEDDINGS_ENABLED", "false")
        loader = YamlConfigLoader()
        config = loader.load(config_file)
        assert config.embeddings_enabled is False

    def test_env_int_parsing(self, config_file: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AKP_RRF_K", "100")
        loader = YamlConfigLoader()
        config = loader.load(config_file)
        assert config.rrf_k == 100


# ─── P-RESOLVE-PATHS: Path resolution ───────────────────────────────────────


class TestPathResolution:
    """P-RESOLVE-PATHS: Relative paths resolved against config dir."""

    def test_relative_path_resolved(self, config_file: Path) -> None:
        loader = YamlConfigLoader()
        config = loader.load(config_file)
        assert len(config.packs) == 1
        pack = config.packs[0]
        # Relative path should be resolved against config file's parent
        expected = config_file.parent / "packs" / "test.duckdb"
        assert pack.path == expected
        assert pack.path.is_absolute()

    def test_absolute_path_preserved(self, full_config_file: Path) -> None:
        loader = YamlConfigLoader()
        config = loader.load(full_config_file)
        beta = next(p for p in config.packs if p.pack_id == "test.domain.beta")
        # On Windows /absolute/... gets a drive letter, but it stays absolute
        assert beta.path.is_absolute()
        assert "beta.duckdb" in str(beta.path)


# ─── P-VALIDATED: Invalid values raise ConfigurationError ────────────────────


class TestValidation:
    """P-VALIDATED: Invalid config raises ConfigurationError."""

    def test_invalid_default_limit_zero(self, tmp_path: Path) -> None:
        cfg = tmp_path / "bad.yaml"
        cfg.write_text("default_limit: 0", encoding="utf-8")
        loader = YamlConfigLoader()
        with pytest.raises(ConfigurationError):
            loader.load(cfg)

    def test_invalid_default_limit_too_high(self, tmp_path: Path) -> None:
        cfg = tmp_path / "bad.yaml"
        cfg.write_text("default_limit: 999", encoding="utf-8")
        loader = YamlConfigLoader()
        with pytest.raises(ConfigurationError):
            loader.load(cfg)

    def test_invalid_yaml_syntax(self, tmp_path: Path) -> None:
        cfg = tmp_path / "bad.yaml"
        cfg.write_text("server_name: [unclosed", encoding="utf-8")
        loader = YamlConfigLoader()
        with pytest.raises(ConfigurationError):
            loader.load(cfg)

    def test_pack_missing_pack_id(self, tmp_path: Path) -> None:
        cfg = tmp_path / "bad.yaml"
        cfg.write_text("packs:\n  - path: ./test.duckdb\n    required: true", encoding="utf-8")
        loader = YamlConfigLoader()
        with pytest.raises(ConfigurationError):
            loader.load(cfg)


# ─── P-ENV-PREFIX: Only AKP_ env vars ───────────────────────────────────────


class TestEnvPrefix:
    """P-ENV-PREFIX: Only AKP_ prefixed env vars are read."""

    def test_non_prefixed_env_ignored(self, config_file: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("DEFAULT_LIMIT", "99")
        monkeypatch.setenv("SERVER_NAME", "should-not-work")
        loader = YamlConfigLoader()
        config = loader.load(config_file)
        # These should NOT override — they lack AKP_ prefix
        assert config.default_limit == 15
        assert config.server_name == "test-runtime"


# ─── P-DETERMINISTIC: Same input → same output ──────────────────────────────


class TestDeterminism:
    """P-DETERMINISTIC: Same config file + env → same model."""

    def test_load_twice_identical(self, config_file: Path) -> None:
        loader = YamlConfigLoader()
        c1 = loader.load(config_file)
        c2 = loader.load(config_file)
        assert c1.model_dump() == c2.model_dump()


# ─── INV-NO-SIDE-EFFECTS: No mutation ───────────────────────────────────────


class TestNoSideEffects:
    """INV-NO-SIDE-EFFECTS: Loading doesn't modify filesystem or env."""

    def test_loading_does_not_create_files(self, config_file: Path) -> None:
        parent = config_file.parent
        before = set(parent.iterdir())
        loader = YamlConfigLoader()
        loader.load(config_file)
        after = set(parent.iterdir())
        assert before == after
