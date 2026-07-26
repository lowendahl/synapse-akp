"""Dense Embedding Stage — generates contextualized vectors via fastembed.

What: Embeds semantic units and builds a USearch ANN index.
Why: Enables semantic similarity search for natural-language queries.
Contracts: Receives list[SemanticUnit]. Produces EmbeddingResult with vectors.
Boundaries: Must NOT perform IO beyond USearch index serialization.
Test strategy: Unit tests verify vector dimensions and index search.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from kp_compiler.domain.models import SemanticUnit


@dataclass
class EmbeddingResult:
    """Output of the embedding stage."""

    unit_ids: list[str] = field(default_factory=list)
    vectors: np.ndarray | None = None
    model_name: str = ""
    dimensions: int = 0
    input_hashes: list[str] = field(default_factory=list)


def build_embeddings(
    units: list[SemanticUnit],
    model_name: str = "BAAI/bge-small-en-v1.5",
) -> EmbeddingResult:
    """Generate dense embeddings for all semantic units.

    Uses fastembed for CPU-friendly embedding generation.
    Each unit is embedded with its context prepended for better retrieval.
    """
    import hashlib

    from fastembed import TextEmbedding

    if not units:
        return EmbeddingResult(model_name=model_name)

    # Build contextualized texts for embedding
    texts: list[str] = []
    unit_ids: list[str] = []
    input_hashes: list[str] = []

    for unit in units:
        # Contextualized embedding input
        text = f"{unit.context}\n{unit.content}" if unit.context else unit.content
        texts.append(text)
        unit_ids.append(unit.id)
        input_hashes.append(hashlib.sha256(text.encode()).hexdigest()[:16])

    # Generate embeddings using fastembed
    model = TextEmbedding(model_name=model_name)
    embeddings_iter = model.passage_embed(texts)
    vectors = np.array(list(embeddings_iter), dtype=np.float32)

    return EmbeddingResult(
        unit_ids=unit_ids,
        vectors=vectors,
        model_name=model_name,
        dimensions=vectors.shape[1] if len(vectors.shape) > 1 else 0,
        input_hashes=input_hashes,
    )


def save_usearch_index(result: EmbeddingResult, index_path: Path) -> None:
    """Save vectors to a USearch HNSW index file."""
    from usearch.index import Index

    if result.vectors is None or len(result.unit_ids) == 0:
        return

    index = Index(
        ndim=result.dimensions,
        metric="cos",
        dtype="f32",
    )

    # Add vectors with integer keys (mapped via unit_ids list order)
    for i, vector in enumerate(result.vectors):
        index.add(i, vector)

    index_path.parent.mkdir(parents=True, exist_ok=True)
    index.save(str(index_path))


def search_usearch_index(
    index_path: Path,
    query_vector: np.ndarray,
    top_k: int = 10,
) -> list[tuple[int, float]]:
    """Search a saved USearch index. Returns (key, distance) pairs."""
    from usearch.index import Index

    if not index_path.exists():
        return []

    index = Index.restore(str(index_path))
    results = index.search(query_vector, top_k)

    return [(int(results.keys[i]), float(results.distances[i])) for i in range(len(results.keys))]
