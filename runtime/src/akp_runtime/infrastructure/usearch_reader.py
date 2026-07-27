"""USearch vector sidecar reader.

Reads the .usearch file produced by the compiler alongside each .duckdb pack.
"""

from __future__ import annotations

from pathlib import Path

from akp_runtime.contracts.protocols import VectorIndex


class USearchVectorIndex(VectorIndex):
    """Reads a .usearch sidecar file for ANN search."""

    def __init__(self, index_path: Path, dimensions: int) -> None:
        raise NotImplementedError("PBI #6")

    def search(self, vector: list[float], top_k: int) -> list[tuple[str, float]]:
        raise NotImplementedError("PBI #7")

    def close(self) -> None:
        raise NotImplementedError("PBI #6")
