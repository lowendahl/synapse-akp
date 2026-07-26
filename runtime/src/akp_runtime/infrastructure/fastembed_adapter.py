"""FastEmbed query embedding adapter.

Lazy-loads the embedding model on first use to keep startup fast.
"""

from __future__ import annotations


class FastEmbedQueryEmbedder:
    """Embeds queries using FastEmbed for vector search."""

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5") -> None:
        raise NotImplementedError("PBI #7")

    def embed_query(self, query: str) -> list[float]:
        raise NotImplementedError("PBI #7")

    @property
    def model_name(self) -> str:
        raise NotImplementedError("PBI #7")

    @property
    def dimensions(self) -> int:
        raise NotImplementedError("PBI #7")
