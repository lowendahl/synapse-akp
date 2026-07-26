"""DuckDB pack adapter — reads compiled Knowledge Packs.

What: Opens .duckdb files read-only, validates schema, warms retrieval caches.
Why: Isolates DuckDB dependency behind adapter boundary.
Contracts: Implements LoadedPack and PackLoader protocols.
Boundaries: ONLY runtime file that imports duckdb.
"""

from __future__ import annotations

from pathlib import Path


class DuckDBLoadedPack:
    """A single opened Knowledge Pack backed by DuckDB."""

    def __init__(self, pack_path: Path) -> None:
        raise NotImplementedError("PBI #6")


class DuckDBPackLoader:
    """Loads and manages multiple Knowledge Packs."""

    def load(self, pack_path: Path) -> DuckDBLoadedPack:
        raise NotImplementedError("PBI #6")

    def load_many(self, pack_paths: list[Path]) -> dict[str, DuckDBLoadedPack]:
        raise NotImplementedError("PBI #6")

    def close_all(self) -> None:
        raise NotImplementedError("PBI #6")
