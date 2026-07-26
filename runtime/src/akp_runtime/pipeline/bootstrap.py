"""Composition root — instantiates all adapters and wires the runtime."""

from __future__ import annotations

from pathlib import Path


def bootstrap_runtime(config_path: Path | None = None) -> None:
    """Bootstrap the runtime: load config, open packs, register MCP tools."""
    raise NotImplementedError("PBI #11")
