"""BM25 Lexical Index Stage — builds term-frequency retrieval index.

What: Indexes semantic units using BM25 via bm25s library.
Why: Proper term-frequency retrieval beats SQL LIKE for recall and ranking.
Contracts: Receives list[SemanticUnit]. Produces BM25Result with tokenized corpus.
Boundaries: Must NOT perform IO. Tokenization + scoring only.
Test strategy: Unit tests with small corpus; verify retrieval ranking.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import bm25s

from kp_compiler.domain.models import SemanticUnit


@dataclass
class BM25Result:
    """Output of the BM25 indexing stage."""

    retriever: bm25s.BM25 | None = None
    unit_ids: list[str] = field(default_factory=list)
    corpus_tokens: list[list[str]] = field(default_factory=list)
    vocab_size: int = 0


def build_bm25_index(units: list[SemanticUnit]) -> BM25Result:
    """Build a BM25 index over semantic units.

    Each unit is indexed with its content prepended by heading and aliases
    for better term coverage.
    """
    if not units:
        return BM25Result()

    # Build corpus: combine context + content for each unit
    corpus_texts: list[str] = []
    unit_ids: list[str] = []

    for unit in units:
        # Heading + content only — aliases are handled by the alias stage
        text_parts = []
        if unit.heading_path:
            text_parts.append(unit.heading_path)
        text_parts.append(unit.content)
        corpus_texts.append(" ".join(text_parts))
        unit_ids.append(unit.id)

    # Tokenize using bm25s built-in tokenizer
    corpus_tokens = bm25s.tokenize(corpus_texts, stopwords="en")

    # Build BM25 index
    retriever = bm25s.BM25()
    retriever.index(corpus_tokens)

    # Get vocab size
    vocab_size = 0
    if hasattr(retriever, "vocab_dict"):
        vocab_size = len(retriever.vocab_dict)

    # Convert tokens to serializable string lists
    token_lists: list[list[str]] = []
    for doc_tokens in corpus_tokens:
        if hasattr(doc_tokens, "tolist"):
            token_lists.append([str(t) for t in doc_tokens.tolist()])
        elif hasattr(doc_tokens, "__iter__"):
            token_lists.append([str(t) for t in doc_tokens])
        else:
            token_lists.append([])

    return BM25Result(
        retriever=retriever,
        unit_ids=unit_ids,
        corpus_tokens=token_lists,
        vocab_size=vocab_size,
    )


def query_bm25(
    result: BM25Result,
    query: str,
    top_k: int = 10,
) -> list[tuple[str, float]]:
    """Query the BM25 index. Returns (unit_id, score) pairs."""
    if result.retriever is None or not result.unit_ids:
        return []

    query_tokens = bm25s.tokenize([query], stopwords="en")
    scores, indices = result.retriever.retrieve(query_tokens, k=min(top_k, len(result.unit_ids)))

    hits: list[tuple[str, float]] = []
    for i in range(scores.shape[1]):
        idx = int(indices[0, i])
        score = float(scores[0, i])
        if score > 0 and idx < len(result.unit_ids):
            hits.append((result.unit_ids[idx], score))

    return hits
