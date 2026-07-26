"""Tests for runtime dependency-injection protocols and import boundaries."""

from __future__ import annotations

import ast
import builtins
import importlib
import sys
from pathlib import Path
from typing import Any

import pytest

from akp_runtime.contracts.mcp_models import (
    ExpandGraphToolInput,
    GetProvenanceToolInput,
    LookupConceptToolInput,
    RuntimeConfigModel,
    SearchToolInput,
)
from akp_runtime.contracts.protocols import (
    ConfigLoader,
    ExpandGraphOperation,
    GetProvenanceOperation,
    LoadedPack,
    LookupConceptOperation,
    PackLoader,
    QueryEmbedder,
    SearchOperation,
    VectorIndex,
)
from akp_runtime.domain.models import GraphEdgeHit, PackMetadata, ProvenanceStep, SearchHit, SemanticUnitRecord
from tests.factories import (
    make_graph_edge_hit,
    make_pack_metadata,
    make_provenance_step,
    make_search_hit,
    make_semantic_unit_record,
)

RUNTIME_ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = RUNTIME_ROOT / "src" / "akp_runtime"


class FakeConfigLoader:
    def load(self, config_path: Path | None = None) -> RuntimeConfigModel:
        _ = config_path
        return RuntimeConfigModel()


class FakeVectorIndex:
    def search(self, vector: list[float], top_k: int) -> list[tuple[str, float]]:
        _ = (vector, top_k)
        return [("csu.metric.c2c::definition", 0.9)]

    def close(self) -> None:
        return None


class FakeQueryEmbedder:
    @property
    def model_name(self) -> str:
        return "BAAI/bge-small-en-v1.5"

    @property
    def dimensions(self) -> int:
        return 384

    def embed_query(self, query: str) -> list[float]:
        _ = query
        return [0.1, 0.2, 0.3]


class FakeLoadedPack:
    @property
    def metadata(self) -> PackMetadata:
        return make_pack_metadata()

    def exact_matches(self, query: str, limit: int) -> list[SearchHit]:
        _ = (query, limit)
        return [make_search_hit()]

    def object_fallback(self, query: str, limit: int) -> list[SearchHit]:
        _ = (query, limit)
        return [make_search_hit(unit_id=None)]

    def lexical_matches(self, query: str, top_k: int) -> list[SearchHit]:
        _ = (query, top_k)
        return [make_search_hit()]

    def semantic_matches(self, vector: list[float], top_k: int) -> list[SearchHit]:
        _ = (vector, top_k)
        return [make_search_hit()]

    def lookup_concept(self, identifier: str) -> SearchHit | None:
        _ = identifier
        return make_search_hit(unit_id=None)

    def concept_units(self, object_id: str, limit: int) -> list[SemanticUnitRecord]:
        _ = (object_id, limit)
        return [make_semantic_unit_record()]

    def graph_neighbors(
        self,
        object_id: str,
        hops: int,
        predicates: tuple[str, ...],
        limit: int,
    ) -> list[GraphEdgeHit]:
        _ = (object_id, hops, predicates, limit)
        return [make_graph_edge_hit()]

    def provenance_for_object(self, object_id: str) -> tuple[ProvenanceStep, ...]:
        _ = object_id
        return (make_provenance_step(),)

    def provenance_for_unit(self, unit_id: str) -> tuple[ProvenanceStep, ...]:
        _ = unit_id
        return (make_provenance_step(layer="semantic_unit"),)

    def provenance_for_edge(self, subject_id: str, predicate: str, object_id: str) -> tuple[ProvenanceStep, ...]:
        _ = (subject_id, predicate, object_id)
        return (make_provenance_step(layer="edge"),)

    def close(self) -> None:
        return None


class FakePackLoader:
    def load(self, pack_path: Path) -> LoadedPack:
        _ = pack_path
        return FakeLoadedPack()

    def load_many(self, pack_paths: list[Path]) -> dict[str, LoadedPack]:
        _ = pack_paths
        return {"test.domain.pack": FakeLoadedPack()}

    def close_all(self) -> None:
        return None


class FakeSearchOperation:
    def search(self, request: SearchToolInput) -> tuple[SearchHit, ...]:
        _ = request
        return (make_search_hit(),)


class FakeLookupConceptOperation:
    def lookup(self, request: LookupConceptToolInput) -> SearchHit:
        _ = request
        return make_search_hit(unit_id=None)


class FakeExpandGraphOperation:
    def expand(self, request: ExpandGraphToolInput) -> tuple[GraphEdgeHit, ...]:
        _ = request
        return (make_graph_edge_hit(),)


class FakeGetProvenanceOperation:
    def get(self, request: GetProvenanceToolInput) -> tuple[ProvenanceStep, ...]:
        _ = request
        return (make_provenance_step(),)


class MissingLoadConfigLoader:
    pass


class MissingCloseVectorIndex:
    def search(self, vector: list[float], top_k: int) -> list[tuple[str, float]]:
        _ = (vector, top_k)
        return []


class MissingDimensionsQueryEmbedder:
    @property
    def model_name(self) -> str:
        return "model"

    def embed_query(self, query: str) -> list[float]:
        _ = query
        return []


class MissingMetadataLoadedPack:
    def exact_matches(self, query: str, limit: int) -> list[SearchHit]:
        _ = (query, limit)
        return []


class MissingLoadManyPackLoader:
    def load(self, pack_path: Path) -> LoadedPack:
        _ = pack_path
        return FakeLoadedPack()

    def close_all(self) -> None:
        return None


class MissingSearchOperation:
    pass


class MissingLookupOperation:
    pass


class MissingExpandOperation:
    pass


class MissingGetOperation:
    pass


def _imported_roots(py_file: Path) -> set[str]:
    tree = ast.parse(py_file.read_text(encoding="utf-8"))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name.split(".")[0] for alias in node.names)
        if isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module.split(".")[0])
    return modules


# Invariant: minimal fakes can satisfy every runtime protocol via structural typing.
@pytest.mark.parametrize(
    ("protocol_type", "instance"),
    (
        (ConfigLoader, FakeConfigLoader()),
        (VectorIndex, FakeVectorIndex()),
        (QueryEmbedder, FakeQueryEmbedder()),
        (LoadedPack, FakeLoadedPack()),
        (PackLoader, FakePackLoader()),
        (SearchOperation, FakeSearchOperation()),
        (LookupConceptOperation, FakeLookupConceptOperation()),
        (ExpandGraphOperation, FakeExpandGraphOperation()),
        (GetProvenanceOperation, FakeGetProvenanceOperation()),
    ),
)
def test_fake_implementations_satisfy_runtime_protocols(protocol_type: type[object], instance: object) -> None:
    assert isinstance(instance, protocol_type)


# Invariant: missing required protocol members must fail runtime_checkable isinstance checks.
@pytest.mark.parametrize(
    ("protocol_type", "instance"),
    (
        (ConfigLoader, MissingLoadConfigLoader()),
        (VectorIndex, MissingCloseVectorIndex()),
        (QueryEmbedder, MissingDimensionsQueryEmbedder()),
        (LoadedPack, MissingMetadataLoadedPack()),
        (PackLoader, MissingLoadManyPackLoader()),
        (SearchOperation, MissingSearchOperation()),
        (LookupConceptOperation, MissingLookupOperation()),
        (ExpandGraphOperation, MissingExpandOperation()),
        (GetProvenanceOperation, MissingGetOperation()),
    ),
)
def test_missing_protocol_members_fail_isinstance(protocol_type: type[object], instance: object) -> None:
    assert not isinstance(instance, protocol_type)


# Invariant: protocol imports must remain decoupled from optional infrastructure packages.
def test_protocols_import_without_optional_packages(monkeypatch: pytest.MonkeyPatch) -> None:
    blocked = {"duckdb", "usearch", "fastembed", "kp_compiler"}
    real_import = builtins.__import__

    def guarded_import(
        name: str,
        globals_dict: dict[str, Any] | None = None,
        locals_dict: dict[str, Any] | None = None,
        fromlist: tuple[str, ...] = (),
        level: int = 0,
    ) -> object:
        if name.split(".")[0] in blocked:
            raise AssertionError(f"unexpected optional import: {name}")
        return real_import(name, globals_dict, locals_dict, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", guarded_import)
    sys.modules.pop("akp_runtime.contracts.protocols", None)

    module = importlib.import_module("akp_runtime.contracts.protocols")

    assert module.LoadedPack.__name__ == "LoadedPack"


# Invariant: runtime must never import kp_compiler and optional packages stay behind designated adapters.
@pytest.mark.parametrize(
    ("forbidden_module", "allowed_paths"),
    (
        ("duckdb", (Path("infrastructure\\duckdb_loader.py"), Path("infrastructure\\persistence"))),
        ("usearch", (Path("infrastructure\\usearch_reader.py"),)),
        ("fastembed", (Path("infrastructure\\fastembed_adapter.py"),)),
    ),
)
def test_optional_dependency_imports_are_isolated(
    forbidden_module: str,
    allowed_paths: tuple[Path, ...],
) -> None:
    for py_file in SOURCE_ROOT.rglob("*.py"):
        imported = _imported_roots(py_file)
        if forbidden_module in imported:
            rel = py_file.relative_to(SOURCE_ROOT)
            allowed = any(
                rel == p or str(rel).startswith(str(p))
                for p in allowed_paths
            )
            assert allowed, f"{rel} must not import {forbidden_module}"


# Invariant: runtime must have no compiler dependency at the source level.
def test_runtime_source_has_no_kp_compiler_imports() -> None:
    offenders = [
        py_file.relative_to(SOURCE_ROOT)
        for py_file in SOURCE_ROOT.rglob("*.py")
        if "kp_compiler" in _imported_roots(py_file)
    ]

    assert offenders == []
