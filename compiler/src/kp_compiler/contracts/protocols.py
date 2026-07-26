"""Protocol definitions for compiler stages and infrastructure adapters.

These are the contracts that implementations must satisfy (ES-02, ES-06).
Stages depend on these Protocols, never on concrete implementations.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable

from kp_compiler.domain.models import KnowledgeObject, Relationship, SemanticUnit


# ─── Source Discovery & Reading ─────────────────────────────────────────────


@runtime_checkable
class SourceReader(Protocol):
    """Reads source files from a canonical repository."""

    def discover(self, root: Path) -> list[Path]:
        """Discover all OKF markdown files under root."""
        ...

    def read(self, path: Path) -> str:
        """Read file content as string."""
        ...


# ─── Parsing ────────────────────────────────────────────────────────────────


@runtime_checkable
class Parser(Protocol):
    """Parses raw markdown + YAML into typed domain objects."""

    def parse(self, content: str, source_path: str) -> KnowledgeObject:
        """Parse a single source file into a KnowledgeObject."""
        ...


# ─── Validation ─────────────────────────────────────────────────────────────


@runtime_checkable
class Validator(Protocol):
    """Validates objects against the ontology and schema."""

    def validate(self, obj: KnowledgeObject) -> list["Diagnostic"]:
        """Return diagnostics for a single object."""
        ...


# ─── Enrichment ─────────────────────────────────────────────────────────────


@runtime_checkable
class Enricher(Protocol):
    """Performs deterministic NLP enrichment."""

    def enrich(self, obj: KnowledgeObject) -> KnowledgeObject:
        """Return enriched copy of the object (aliases, entities, acronyms)."""
        ...


# ─── Graph Builder ──────────────────────────────────────────────────────────


@runtime_checkable
class GraphBuilder(Protocol):
    """Constructs and analyzes the knowledge graph."""

    def build(self, objects: list[KnowledgeObject]) -> "GraphResult":
        """Build graph from objects, return result with metrics and diagnostics."""
        ...


# ─── Projections ────────────────────────────────────────────────────────────


@runtime_checkable
class Embedder(Protocol):
    """Generates dense vector embeddings."""

    def embed_passages(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of passages (document/passage mode)."""
        ...

    def embed_query(self, query: str) -> list[float]:
        """Embed a single query (query mode — asymmetric)."""
        ...

    @property
    def model_name(self) -> str:
        """Return the model identifier for provenance."""
        ...

    @property
    def dimensions(self) -> int:
        """Return embedding dimensionality."""
        ...


@runtime_checkable
class LexicalIndexer(Protocol):
    """Builds a BM25/lexical index."""

    def index(self, corpus: list[str], ids: list[str]) -> None:
        """Index a corpus of texts with associated IDs."""
        ...

    def search(self, query: str, top_k: int = 10) -> list[tuple[str, float]]:
        """Search and return (id, score) pairs."""
        ...


@runtime_checkable
class VectorStore(Protocol):
    """Stores and searches dense vectors."""

    def add(self, ids: list[str], vectors: list[list[float]]) -> None:
        """Add vectors with associated IDs."""
        ...

    def search(self, vector: list[float], top_k: int = 10) -> list[tuple[str, float]]:
        """Search nearest neighbors, return (id, distance) pairs."""
        ...

    def save(self, path: Path) -> None:
        """Persist index to disk."""
        ...


@runtime_checkable
class PackWriter(Protocol):
    """Writes compiled projections to the Knowledge Pack."""

    def write_objects(self, objects: list[KnowledgeObject]) -> None:
        """Write canonical object table."""
        ...

    def write_graph(self, result: "GraphResult") -> None:
        """Write node and edge tables."""
        ...

    def write_semantic_units(self, units: list[SemanticUnit]) -> None:
        """Write semantic unit table."""
        ...

    def write_manifest(self, manifest: dict) -> None:
        """Write build manifest."""
        ...

    def close(self) -> None:
        """Finalize and close the pack file."""
        ...


# ─── Supporting Types (imported by protocols) ───────────────────────────────


from dataclasses import dataclass, field
from enum import Enum


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass(frozen=True)
class Diagnostic:
    """A structured build diagnostic."""

    severity: Severity
    source_file: str
    message: str
    stage: str
    object_id: str = ""
    line: int | None = None


@dataclass
class GraphResult:
    """Output of the graph builder stage."""

    nodes: list[dict] = field(default_factory=list)
    edges: list[dict] = field(default_factory=list)
    diagnostics: list[Diagnostic] = field(default_factory=list)
    metrics: dict = field(default_factory=dict)
