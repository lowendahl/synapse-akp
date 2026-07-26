"""Protocol definitions for runtime dependency injection.

All infrastructure adapters implement these protocols so the runtime
is mockable without DuckDB, USearch, FastEmbed, or MCP in unit tests.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable

from akp_runtime.contracts.mcp_models import (
    ExpandGraphToolInput,
    GetProvenanceToolInput,
    LookupConceptToolInput,
    RuntimeConfigModel,
    SearchToolInput,
)
from akp_runtime.domain.models import GraphEdgeHit, PackMetadata, ProvenanceStep, SearchHit, SemanticUnitRecord


@runtime_checkable
class ConfigLoader(Protocol):
    def load(self, config_path: Path | None = None) -> RuntimeConfigModel: ...


@runtime_checkable
class VectorIndex(Protocol):
    def search(self, vector: list[float], top_k: int) -> list[tuple[str, float]]: ...
    def close(self) -> None: ...


@runtime_checkable
class QueryEmbedder(Protocol):
    def embed_query(self, query: str) -> list[float]: ...
    @property
    def model_name(self) -> str: ...
    @property
    def dimensions(self) -> int: ...


@runtime_checkable
class LoadedPack(Protocol):
    @property
    def metadata(self) -> PackMetadata: ...
    def exact_matches(self, query: str, limit: int) -> list[SearchHit]: ...
    def object_fallback(self, query: str, limit: int) -> list[SearchHit]: ...
    def lexical_matches(self, query: str, top_k: int) -> list[SearchHit]: ...
    def semantic_matches(self, vector: list[float], top_k: int) -> list[SearchHit]: ...
    def lookup_concept(self, identifier: str) -> SearchHit | None: ...
    def concept_units(self, object_id: str, limit: int) -> list[SemanticUnitRecord]: ...
    def graph_neighbors(
        self, object_id: str, hops: int, predicates: tuple[str, ...], limit: int
    ) -> list[GraphEdgeHit]: ...
    def provenance_for_object(self, object_id: str) -> tuple[ProvenanceStep, ...]: ...
    def provenance_for_unit(self, unit_id: str) -> tuple[ProvenanceStep, ...]: ...
    def provenance_for_edge(self, subject_id: str, predicate: str, object_id: str) -> tuple[ProvenanceStep, ...]: ...
    def close(self) -> None: ...


@runtime_checkable
class PackLoader(Protocol):
    def load(self, pack_path: Path) -> LoadedPack: ...
    def load_many(self, pack_paths: list[Path]) -> dict[str, LoadedPack]: ...
    def close_all(self) -> None: ...


@runtime_checkable
class SearchOperation(Protocol):
    def search(self, request: SearchToolInput) -> tuple[SearchHit, ...]: ...


@runtime_checkable
class LookupConceptOperation(Protocol):
    def lookup(self, request: LookupConceptToolInput) -> SearchHit: ...


@runtime_checkable
class ExpandGraphOperation(Protocol):
    def expand(self, request: ExpandGraphToolInput) -> tuple[GraphEdgeHit, ...]: ...


@runtime_checkable
class GetProvenanceOperation(Protocol):
    def get(self, request: GetProvenanceToolInput) -> tuple[ProvenanceStep, ...]: ...
