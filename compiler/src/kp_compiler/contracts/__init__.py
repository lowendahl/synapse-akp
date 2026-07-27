"""Contracts package — compiler protocols and typed errors."""

from kp_compiler.contracts.errors import OntologyViolation
from kp_compiler.contracts.protocols import (
    Diagnostic,
    Embedder,
    Enricher,
    GraphBuilder,
    GraphEdge,
    GraphNode,
    GraphResult,
    LexicalIndexer,
    PackWriter,
    Parser,
    Severity,
    SourceReader,
    Validator,
    VectorStore,
)

__all__ = [
    "Diagnostic",
    "Embedder",
    "Enricher",
    "GraphBuilder",
    "GraphEdge",
    "GraphNode",
    "GraphResult",
    "LexicalIndexer",
    "OntologyViolation",
    "PackWriter",
    "Parser",
    "Severity",
    "SourceReader",
    "Validator",
    "VectorStore",
]
