"""MCP configuration models — server and pack binding contracts.

Supports three pack source modes:
  - file:// or bare path → local file (simplest fallback)
  - github://owner/repo/releases/tag/asset.duckdb → GitHub release asset
  - Legacy: just `path` field for backward compatibility
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class PackSourceModel(BaseModel):
    """Describes how to resolve a pack's .duckdb file.

    Resolution chain: source → local_cache → fallback (first that exists wins).
    """

    model_config = ConfigDict(extra="forbid")

    source: str | None = Field(
        default=None,
        description="Primary source URI: file:// path, github://owner/repo/releases/tag/asset, or bare path",
    )
    local_cache: Path | None = Field(
        default=None,
        description="Local cache path (e.g. ~/.akp/packs/mcem.duckdb). Used to avoid re-downloading.",
    )
    fallback: Path | None = Field(
        default=None,
        description="Fallback local path if source is unavailable (offline/air-gapped mode)",
    )


class PackBindingModel(BaseModel):
    """Configuration for a single knowledge pack binding."""

    model_config = ConfigDict(extra="forbid")

    pack_id: str = Field(min_length=1)
    path: Path | None = Field(default=None, description="Legacy: direct path to .duckdb file")
    source: str | None = Field(default=None, description="Source URI (overrides path if present)")
    local_cache: Path | None = Field(default=None, description="Local cache location")
    fallback: Path | None = Field(default=None, description="Fallback path for offline use")
    required: bool = True
    auto_update: bool = Field(default=False, description="Check for newer version on startup")

    @property
    def resolved_source(self) -> PackSourceModel:
        """Build a PackSourceModel from this binding's fields."""
        # Legacy mode: if only path is set, treat it as the source
        source = self.source
        if source is None and self.path is not None:
            source = f"file://{self.path}"
        return PackSourceModel(
            source=source,
            local_cache=self.local_cache,
            fallback=self.fallback,
        )


class RuntimeConfigModel(BaseModel):
    """Top-level runtime configuration."""

    model_config = ConfigDict(extra="forbid")

    server_name: str = "akp-runtime"
    default_limit: int = Field(default=10, ge=1, le=50)
    lexical_k: int = Field(default=20, ge=1, le=100)
    semantic_k: int = Field(default=20, ge=1, le=100)
    graph_boost_top_n: int = Field(default=3, ge=1, le=10)
    graph_boost_value: float = Field(default=0.1, ge=0.0, le=1.0)
    rrf_k: int = Field(default=60, ge=1, le=200)
    max_hops: int = Field(default=3, ge=1, le=5)
    embeddings_enabled: bool = True
    config_path: Path | None = None
    pack_cache_directory: Path = Field(
        default=Path.home() / ".akp" / "packs",
        description="Default directory for cached pack downloads",
    )
    packs: list[PackBindingModel] = Field(default_factory=list)
