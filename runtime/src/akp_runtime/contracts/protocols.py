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
from akp_runtime.domain.explain_models import SynthesisResult
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


# ─── Infrastructure Protocols ───────────────────────────────────────────────


@runtime_checkable
class QueryObjectProtocol(Protocol):
    """Contract for all query objects in the persistence layer."""

    def sql(self) -> str: ...
    def parameters(self) -> list[object]: ...
    def map_results(self, rows: list[tuple]) -> object: ...


@runtime_checkable
class QueryExecutorProtocol(Protocol):
    """Contract for executing query objects against a connection."""

    def execute(self, query: QueryObjectProtocol) -> object: ...
    def mark_closed(self) -> None: ...


@runtime_checkable
class SchemaValidator(Protocol):
    """Contract for validating pack schema and building metadata."""

    def build_metadata(self) -> PackMetadata: ...


@runtime_checkable
class ResultMapper(Protocol):
    """Contract for mapping raw query rows to domain objects."""

    def from_object_row(self, row: tuple) -> SearchHit: ...


@runtime_checkable
class ProvenanceFactory(Protocol):
    """Contract for building provenance steps."""

    def pack_step(self, metadata: PackMetadata) -> ProvenanceStep: ...


@runtime_checkable
class ManifestParserProtocol(Protocol):
    """Contract for parsing manifest key-value pairs into metadata."""

    def build_metadata(self, manifest: dict[str, str], pack_path: Path) -> PackMetadata: ...


@runtime_checkable
class GraphService(Protocol):
    """Contract for graph traversal and provenance queries."""

    def graph_neighbors(
        self, object_id: str, hops: int, predicates: tuple[str, ...], limit: int
    ) -> list[GraphEdgeHit]: ...
    def provenance_for_object(self, object_id: str) -> tuple[ProvenanceStep, ...]: ...
    def provenance_for_unit(self, unit_id: str) -> tuple[ProvenanceStep, ...]: ...
    def provenance_for_edge(self, subject_id: str, predicate: str, object_id: str) -> tuple[ProvenanceStep, ...]: ...


@runtime_checkable
class SemanticReasoningClient(Protocol):
    """Protocol for LLM-backed explanation synthesis (ADR-036, ADR-038)."""

    def synthesize_explanation(
        self,
        concept_title: str,
        concept_type: str,
        semantic_units: list[SemanticUnitRecord],
        neighbors: list[GraphEdgeHit],
        detail_level: str,
    ) -> SynthesisResult: ...
