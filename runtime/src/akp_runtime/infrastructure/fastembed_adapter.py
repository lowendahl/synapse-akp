"""FastEmbed query embedding adapter.

Lazy-loads the embedding model on first use to keep startup fast.
Uses the same model the compiler used (BAAI/bge-small-en-v1.5, 384d).
"""

from __future__ import annotations

import logging

from akp_runtime.contracts.protocols import QueryEmbedder

logger = logging.getLogger(__name__)


class FastEmbedQueryEmbedder(QueryEmbedder):
    """Embeds queries using FastEmbed for vector search.

    Lazy-loads the model on first embed_query call to keep server startup fast.
    """

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5") -> None:
        self._model_name = model_name
        self._model = None
        self._dimensions = 384  # bge-small-en-v1.5 default

    def embed_query(self, query: str) -> list[float]:
        """Embed a single query string into a dense vector."""
        if self._model is None:
            self._load_model()
        embeddings = list(self._model.query_embed([query]))  # type: ignore[union-attr]
        return embeddings[0].tolist()

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def dimensions(self) -> int:
        return self._dimensions

    def _load_model(self) -> None:
        """Lazy-load the embedding model."""
        from fastembed import TextEmbedding

        logger.info("Loading embedding model: %s", self._model_name)
        self._model = TextEmbedding(model_name=self._model_name)
        logger.info("Embedding model ready (%dd)", self._dimensions)
