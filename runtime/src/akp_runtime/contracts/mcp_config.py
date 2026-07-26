"""MCP configuration models — server and pack binding contracts."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class PackBindingModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pack_id: str = Field(min_length=1)
    path: Path
    required: bool = True


class RuntimeConfigModel(BaseModel):
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
    packs: list[PackBindingModel] = Field(default_factory=list)
