"""USearch vector sidecar reader.

Reads the .usearch file produced by the compiler alongside each .duckdb pack.
Provides approximate nearest neighbor search for dense vector queries.
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
from usearch.index import Index

from akp_runtime.contracts.protocols import VectorIndex

logger = logging.getLogger(__name__)


class USearchVectorIndex(VectorIndex):
    """Reads a .usearch sidecar file for ANN search."""

    def __init__(self, index_path: Path, dimensions: int, labels: list[str] | None = None) -> None:
        self._path = index_path
        self._dimensions = dimensions
        self._index = Index(ndim=dimensions, metric="cos")
        self._index.load(str(index_path))
        self._labels = labels or []
        logger.debug("Loaded vector index: %s (%d vectors, %dd)", index_path.name, len(self._index), dimensions)

    def search(self, vector: list[float], top_k: int) -> list[tuple[str, float]]:
        """Search the index for nearest neighbors. Returns (label, distance) pairs."""
        query = np.array(vector, dtype=np.float32)
        results = self._index.search(query, top_k)

        matches: list[tuple[str, float]] = []
        for key, distance in zip(results.keys, results.distances, strict=False):
            key_int = int(key)
            label = self._labels[key_int] if self._labels and key_int < len(self._labels) else str(key_int)
            # Convert distance to similarity score (cosine: 1 - distance)
            similarity = 1.0 - float(distance)
            matches.append((label, similarity))

        return matches

    def close(self) -> None:
        """Release the index resources."""
        # usearch Index doesn't have an explicit close, but we clear the reference
        self._index = None  # type: ignore[assignment]
