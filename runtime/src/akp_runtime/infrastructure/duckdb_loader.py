"""DuckDB pack adapter — reads compiled Knowledge Packs."""

from __future__ import annotations

import contextlib
import logging
from pathlib import Path

import duckdb

from akp_runtime.contracts.errors import PackOpenError
from akp_runtime.contracts.protocols import LoadedPack, PackLoader
from akp_runtime.domain.models import PackMetadata, SearchHit
from akp_runtime.domain.search_results import SemanticUnitRecord
from akp_runtime.infrastructure.duckdb_graph_service import DuckDBGraphService
from akp_runtime.infrastructure.duckdb_pack_connection import DuckDBPackConnection
from akp_runtime.infrastructure.persistence.queries.base import QueryExecutor
from akp_runtime.infrastructure.persistence.queries.search_queries import (
    ConceptUnitsQuery,
    ExactAliasMatchQuery,
    LexicalSearchQuery,
    LookupObjectQuery,
    ObjectFallbackQuery,
)
from akp_runtime.infrastructure.persistence.result_mapper import SearchHitMapper, SemanticUnitMapper

logger = logging.getLogger(__name__)


class DuckDBLoadedPack(LoadedPack):
    """A single opened Knowledge Pack backed by DuckDB."""

    def __init__(self, pack_path: Path) -> None:
        self._path = pack_path.resolve()
        self._closed = False
        try:
            self._connection = duckdb.connect(str(self._path), read_only=True)
        except Exception as error:
            raise PackOpenError(pack_path=self._path, detail=str(error)) from error
        self._executor = QueryExecutor(self._connection, pack_id="unknown")
        metadata_loader = DuckDBPackConnection(self._path, self._connection, self._executor)
        self._metadata = metadata_loader.build_metadata()
        self._executor = QueryExecutor(self._connection, pack_id=self._metadata.pack_id)
        self._pack_step = lambda: metadata_loader.pack_provenance_step(self._metadata)
        self._mapper = SearchHitMapper(
            self._metadata.pack_id,
            self._metadata.pack_version,
            self._pack_step(),
        )
        self._graph_service = DuckDBGraphService(self._executor, self._metadata, self._pack_step)

    @property
    def metadata(self) -> PackMetadata:
        return self._metadata

    def exact_matches(self, query: str, limit: int) -> list[SearchHit]:
        if limit <= 0:
            return []
        return [
            self._mapper.from_object_row(row)
            for row in self._executor.execute(ExactAliasMatchQuery(query, max(1, limit)))
        ]

    def object_fallback(self, query: str, limit: int) -> list[SearchHit]:
        return [
            self._mapper.from_object_row(row)
            for row in self._executor.execute(ObjectFallbackQuery(query, max(1, limit)))
        ]

    def lexical_matches(self, query: str, top_k: int) -> list[SearchHit]:
        return [
            self._mapper.from_object_row(row)
            for row in self._executor.execute(LexicalSearchQuery(query, max(1, top_k)))
        ]

    def semantic_matches(self, vector: list[float], top_k: int) -> list[SearchHit]:
        return []

    def lookup_concept(self, identifier: str) -> SearchHit | None:
        rows = self._executor.execute(LookupObjectQuery(identifier))
        return self._mapper.from_object_row(rows[0]) if rows else None

    def concept_units(self, object_id: str, limit: int) -> list[SemanticUnitRecord]:
        return [
            SemanticUnitMapper.from_row(row)
            for row in self._executor.execute(ConceptUnitsQuery(object_id, max(1, limit)))
        ]

    def graph_neighbors(
        self,
        object_id: str,
        hops: int,
        predicates: tuple[str, ...],
        limit: int,
    ) -> list:
        return self._graph_service.graph_neighbors(object_id, hops, predicates, limit)

    def provenance_for_object(self, object_id: str) -> tuple:
        return self._graph_service.provenance_for_object(object_id)

    def provenance_for_unit(self, unit_id: str) -> tuple:
        return self._graph_service.provenance_for_unit(unit_id)

    def provenance_for_edge(self, subject_id: str, predicate: str, object_id: str) -> tuple:
        return self._graph_service.provenance_for_edge(subject_id, predicate, object_id)

    def close(self) -> None:
        if not self._closed:
            self._closed = True
            self._executor.mark_closed()
            with contextlib.suppress(Exception):
                self._connection.close()


class DuckDBPackLoader(PackLoader):
    """Loads and manages multiple Knowledge Packs."""

    def __init__(self) -> None:
        self._packs: dict[str, DuckDBLoadedPack] = {}

    def load(self, pack_path: Path) -> DuckDBLoadedPack:
        if not pack_path.exists():
            raise PackOpenError(pack_path=pack_path, detail="File not found")
        pack = DuckDBLoadedPack(pack_path)
        self._packs[pack.metadata.pack_id] = pack
        return pack

    def load_many(self, pack_paths: list[Path]) -> dict[str, DuckDBLoadedPack]:
        return {pack.metadata.pack_id: pack for pack in (self.load(path) for path in pack_paths)}

    def close_all(self) -> None:
        for pack in self._packs.values():
            pack.close()
        self._packs.clear()
