"""Hybrid search operation — exact + BM25 + vector + RRF + graph boost."""

from __future__ import annotations

from akp_runtime.contracts.mcp_models import SearchToolInput
from akp_runtime.domain.models import SearchHit


class HybridSearchOperation:
    """Implements the full hybrid search pipeline."""

    def search(self, request: SearchToolInput) -> tuple[SearchHit, ...]:
        raise NotImplementedError("PBI #7")
