"""Infrastructure protocol contracts for compiler projections."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, TypeVar, runtime_checkable

from kp_compiler.contracts.protocol_support_types import GraphResult
from kp_compiler.domain.models import KnowledgeObject, SemanticUnit
from kp_compiler.domain.rules import PackRules

ResultT = TypeVar("ResultT", covariant=True)


@runtime_checkable
class Embedder(Protocol):
    def embed_passages(self, texts: list[str]) -> list[list[float]]: ...
    def embed_query(self, query: str) -> list[float]: ...

    @property
    def model_name(self) -> str: ...

    @property
    def dimensions(self) -> int: ...


@runtime_checkable
class LexicalIndexer(Protocol):
    def index(self, corpus: list[str], ids: list[str]) -> None: ...
    def search(self, query: str, top_k: int = 10) -> list[tuple[str, float]]: ...


@runtime_checkable
class VectorStore(Protocol):
    def add(self, ids: list[str], vectors: list[list[float]]) -> None: ...
    def search(self, vector: list[float], top_k: int = 10) -> list[tuple[str, float]]: ...
    def save(self, path: Path) -> None: ...


@runtime_checkable
class QueryProtocol(Protocol[ResultT]):
    def execute(self, connection: object) -> ResultT: ...


@runtime_checkable
class PackWriter(Protocol):
    def write_objects(self, objects: list[KnowledgeObject]) -> None: ...
    def write_graph(self, result: GraphResult) -> None: ...
    def write_semantic_units(self, units: list[SemanticUnit]) -> None: ...
    def write_manifest(self, manifest: dict) -> None: ...
    def close(self) -> None: ...


@runtime_checkable
class SchemaBuilder(Protocol):
    """Contract for creating the compiled pack schema."""

    def create_schema(self, connection: object) -> None: ...


@runtime_checkable
class RulesLoaderProtocol(Protocol):
    """Contract for loading pack rules from the filesystem."""

    def load(self, path: Path) -> PackRules: ...
