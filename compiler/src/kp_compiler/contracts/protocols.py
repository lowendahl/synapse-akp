"""Protocol definitions for compiler stages and infrastructure adapters."""

from __future__ import annotations

from kp_compiler.contracts.infrastructure_protocols import (
    Embedder,
    LexicalIndexer,
    PackWriter,
    QueryProtocol,
    VectorStore,
)
from kp_compiler.contracts.protocol_support_types import Diagnostic, GraphEdge, GraphNode, GraphResult, Severity
from kp_compiler.contracts.stage_protocols import Enricher, GraphBuilder, Parser, SourceReader, Validator


class ProtocolCatalog:
    """Facade for backward-compatible protocol exports."""


__all__ = [
    "Diagnostic",
    "Embedder",
    "Enricher",
    "GraphBuilder",
    "GraphEdge",
    "GraphNode",
    "GraphResult",
    "LexicalIndexer",
    "PackWriter",
    "Parser",
    "ProtocolCatalog",
    "QueryProtocol",
    "Severity",
    "SourceReader",
    "Validator",
    "VectorStore",
]
