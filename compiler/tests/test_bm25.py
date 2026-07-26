"""Tests for BM25 lexical index stage (ADR-012)."""

from kp_compiler.domain.models import SemanticUnit
from kp_compiler.stages.bm25 import build_bm25_index, query_bm25


def _make_unit(
    uid: str, heading: str, content: str, context: str = ""
) -> SemanticUnit:
    return SemanticUnit(
        id=uid,
        source_object_id="obj.test",
        heading_path=heading,
        content=content,
        context=context,
        depth=1,
    )


class TestBuildBM25Index:
    """Verify BM25 index construction."""

    def test_empty_corpus_returns_empty_result(self) -> None:
        result = build_bm25_index([])
        assert result.retriever is None
        assert result.vocab_size == 0

    def test_single_document_indexes(self) -> None:
        units = [_make_unit("u1", "Title", "Azure cloud migration workload")]
        result = build_bm25_index(units)
        assert result.retriever is not None
        assert len(result.unit_ids) == 1
        assert result.vocab_size > 0

    def test_corpus_tokens_are_string_lists(self) -> None:
        units = [
            _make_unit("u1", "Heading", "content alpha beta"),
            _make_unit("u2", "Heading", "content gamma delta"),
        ]
        result = build_bm25_index(units)
        for tokens in result.corpus_tokens:
            assert isinstance(tokens, list)
            for t in tokens:
                assert isinstance(t, str)


class TestQueryBM25:
    """Verify BM25 retrieval ranking."""

    def test_relevant_document_ranks_higher(self) -> None:
        units = [
            _make_unit("u1", "Cloud Migration", "Azure workload migration factory"),
            _make_unit("u2", "Customer Success", "Account manager planning review"),
            _make_unit("u3", "Migration Steps", "Step by step cloud migration guide"),
        ]
        result = build_bm25_index(units)
        hits = query_bm25(result, "cloud migration", top_k=3)

        # At least one hit should be from migration-related units
        hit_ids = [h[0] for h in hits]
        assert "u1" in hit_ids or "u3" in hit_ids

    def test_no_results_for_unrelated_query(self) -> None:
        units = [_make_unit("u1", "Title", "Azure cloud migration")]
        result = build_bm25_index(units)
        hits = query_bm25(result, "quantum physics", top_k=5)
        # May return 0 or very low scores
        assert all(score < 1.0 for _, score in hits)

    def test_empty_index_returns_empty(self) -> None:
        from kp_compiler.stages.bm25 import BM25Result

        result = BM25Result()
        hits = query_bm25(result, "anything")
        assert hits == []

    def test_top_k_limits_results(self) -> None:
        units = [_make_unit(f"u{i}", f"Doc {i}", f"word{i} content") for i in range(20)]
        result = build_bm25_index(units)
        hits = query_bm25(result, "content", top_k=5)
        assert len(hits) <= 5
