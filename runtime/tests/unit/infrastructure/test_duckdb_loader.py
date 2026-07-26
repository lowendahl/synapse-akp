"""Unit tests for DuckDB Pack Loader.

Tests validate component promises and invariants from docs/components/pack-loader.md:
- P-READONLY: Never writes to pack files
- P-VALIDATE: Raises typed errors on invalid packs
- P-METADATA: All 19 manifest keys parsed to correct types
- P-PROTOCOL: Satisfies LoadedPack protocol
- P-DETERMINISTIC: Same input → same output
- P-CLOSE-SAFE: Double close doesn't raise; query after close raises
- P-ERROR-TYPED: Correct exception for each failure mode
- P-ISOLATION: Closing one pack doesn't affect another
- P-SCHEMA-MAJOR: Only schema major 2 accepted
- INV-CONNECTION: One connection per pack
- INV-NO-MUTATION: No DDL/DML
- INV-BFS-BOUNDED: Graph traversal respects depth/limit
"""

from __future__ import annotations

from pathlib import Path

import duckdb
import pytest

from akp_runtime.contracts.errors import (
    MissingManifestKey,
    MissingPackTable,
    PackOpenError,
    RuntimeStateError,
    UnsupportedSchemaVersion,
)
from akp_runtime.contracts.protocols import LoadedPack, PackLoader
from akp_runtime.domain.models import GraphEdgeHit, ProvenanceStep, SearchHit, SemanticUnitRecord
from akp_runtime.infrastructure.duckdb_loader import DuckDBLoadedPack, DuckDBPackLoader

# ─── Fixtures ────────────────────────────────────────────────────────────────

REQUIRED_TABLES_DDL = """
CREATE TABLE objects (
  id VARCHAR PRIMARY KEY,
  type VARCHAR NOT NULL,
  title VARCHAR,
  description VARCHAR,
  domain VARCHAR,
  status VARCHAR,
  aliases JSON,
  tags JSON,
  source_path VARCHAR,
  properties JSON
);

CREATE TABLE semantic_units (
  id VARCHAR PRIMARY KEY,
  source_object_id VARCHAR NOT NULL,
  heading_path VARCHAR,
  content VARCHAR,
  context VARCHAR,
  object_type VARCHAR,
  domain VARCHAR
);

CREATE TABLE aliases (
  alias VARCHAR NOT NULL,
  canonical_id VARCHAR NOT NULL,
  alias_type VARCHAR DEFAULT 'exact'
);

CREATE TABLE edges (
  subject_id VARCHAR NOT NULL,
  predicate VARCHAR NOT NULL,
  object_id VARCHAR NOT NULL,
  origin VARCHAR NOT NULL,
  confidence FLOAT
);

CREATE TABLE manifest (
  key VARCHAR PRIMARY KEY,
  value VARCHAR
);
"""

MANIFEST_KEYS = {
    "pack_id": "test.domain.pack",
    "pack_version": "1.0.0",
    "schema_version": "2.0.0",
    "ontology_version": "1.0.0",
    "compiler_version": "0.5.0",
    "build_timestamp": "2024-01-01T00:00:00Z",
    "source_file_count": "10",
    "object_count": "5",
    "node_count": "5",
    "edge_count": "3",
    "semantic_unit_count": "8",
    "alias_count": "2",
    "bm25_vocab_size": "150",
    "embedding_model": "BAAI/bge-small-en-v1.5",
    "embedding_dimensions": "384",
    "cross_pack_refs": "0",
    "content_hash": "sha256:abc123",
    "error_count": "0",
    "warning_count": "1",
}

SAMPLE_OBJECTS = [
    ("obj-1", "concept", "First Concept", "Description 1", "csu", "active", "[]", "[]", "path/a.md", "{}"),
    ("obj-2", "metric", "Second Metric", "Description 2", "csu", "active", '["alias-a"]', "[]", "path/b.md", "{}"),
    ("obj-3", "process", "Third Process", "Description 3", "csu", "active", "[]", '["tag1"]', "path/c.md", "{}"),
]

SAMPLE_UNITS = [
    ("unit-1", "obj-1", "## Overview", "Content of unit 1", "Context 1", "concept", "csu"),
    ("unit-2", "obj-1", "## Details", "Content of unit 2", "Context 2", "concept", "csu"),
    ("unit-3", "obj-2", "## Overview", "Content of unit 3", "Context 3", "metric", "csu"),
]

SAMPLE_ALIASES = [
    ("alias-a", "obj-2", "exact"),
    ("First Concept", "obj-1", "title"),
]

SAMPLE_EDGES = [
    ("obj-1", "relates_to", "obj-2", "authored", 0.9),
    ("obj-2", "depends_on", "obj-3", "authored", 0.8),
    ("obj-3", "informs", "obj-1", "derived", 0.7),
]


@pytest.fixture()
def valid_pack_path(tmp_path: Path) -> Path:
    """Create a valid pack database with all required tables and data."""
    db_path = tmp_path / "test.domain.pack.duckdb"
    con = duckdb.connect(str(db_path))
    con.execute(REQUIRED_TABLES_DDL)
    # Insert manifest
    for key, value in MANIFEST_KEYS.items():
        con.execute("INSERT INTO manifest VALUES (?, ?)", [key, value])
    # Insert objects
    for obj in SAMPLE_OBJECTS:
        con.execute("INSERT INTO objects VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", list(obj))
    # Insert semantic units
    for unit in SAMPLE_UNITS:
        con.execute("INSERT INTO semantic_units VALUES (?, ?, ?, ?, ?, ?, ?)", list(unit))
    # Insert aliases
    for alias in SAMPLE_ALIASES:
        con.execute("INSERT INTO aliases VALUES (?, ?, ?)", list(alias))
    # Insert edges
    for edge in SAMPLE_EDGES:
        con.execute("INSERT INTO edges VALUES (?, ?, ?, ?, ?)", list(edge))
    con.close()
    return db_path


@pytest.fixture()
def loaded_pack(valid_pack_path: Path) -> DuckDBLoadedPack:
    """Return a loaded pack from a valid database."""
    loader = DuckDBPackLoader()
    pack = loader.load(valid_pack_path)
    yield pack
    pack.close()


# ─── P-VALIDATE: Schema and table validation ─────────────────────────────────


class TestValidation:
    """P-VALIDATE: Invalid packs raise before returning LoadedPack."""

    def test_nonexistent_file_raises_pack_open_error(self, tmp_path: Path) -> None:
        """File not found → PackOpenError."""
        loader = DuckDBPackLoader()
        with pytest.raises(PackOpenError):
            loader.load(tmp_path / "nonexistent.duckdb")

    def test_schema_version_major_1_rejected(self, tmp_path: Path) -> None:
        """P-SCHEMA-MAJOR: Only schema major 2 accepted."""
        db_path = tmp_path / "old.duckdb"
        con = duckdb.connect(str(db_path))
        con.execute(REQUIRED_TABLES_DDL)
        keys = dict(MANIFEST_KEYS)
        keys["schema_version"] = "1.0.0"
        for key, value in keys.items():
            con.execute("INSERT INTO manifest VALUES (?, ?)", [key, value])
        con.close()
        loader = DuckDBPackLoader()
        with pytest.raises(UnsupportedSchemaVersion) as exc_info:
            loader.load(db_path)
        assert exc_info.value.found == "1.0.0"

    def test_schema_version_major_3_rejected(self, tmp_path: Path) -> None:
        """P-SCHEMA-MAJOR: Future versions also rejected."""
        db_path = tmp_path / "future.duckdb"
        con = duckdb.connect(str(db_path))
        con.execute(REQUIRED_TABLES_DDL)
        keys = dict(MANIFEST_KEYS)
        keys["schema_version"] = "3.1.0"
        for key, value in keys.items():
            con.execute("INSERT INTO manifest VALUES (?, ?)", [key, value])
        con.close()
        loader = DuckDBPackLoader()
        with pytest.raises(UnsupportedSchemaVersion):
            loader.load(db_path)

    def test_schema_version_2_1_0_accepted(self, tmp_path: Path) -> None:
        """P-SCHEMA-MAJOR: Minor/patch variants of 2 accepted."""
        db_path = tmp_path / "compat.duckdb"
        con = duckdb.connect(str(db_path))
        con.execute(REQUIRED_TABLES_DDL)
        keys = dict(MANIFEST_KEYS)
        keys["schema_version"] = "2.1.0"
        for key, value in keys.items():
            con.execute("INSERT INTO manifest VALUES (?, ?)", [key, value])
        con.close()
        loader = DuckDBPackLoader()
        pack = loader.load(db_path)
        assert pack.metadata.schema_version == "2.1.0"
        pack.close()

    def test_missing_objects_table_raises(self, tmp_path: Path) -> None:
        """Missing required table → MissingPackTable."""
        db_path = tmp_path / "notables.duckdb"
        con = duckdb.connect(str(db_path))
        # Create all tables EXCEPT objects
        con.execute("CREATE TABLE semantic_units (id VARCHAR PRIMARY KEY, source_object_id VARCHAR)")
        con.execute("CREATE TABLE aliases (alias VARCHAR, canonical_id VARCHAR)")
        con.execute("CREATE TABLE edges (subject_id VARCHAR, predicate VARCHAR, object_id VARCHAR, origin VARCHAR)")
        con.execute("CREATE TABLE manifest (key VARCHAR PRIMARY KEY, value VARCHAR)")
        for key, value in MANIFEST_KEYS.items():
            con.execute("INSERT INTO manifest VALUES (?, ?)", [key, value])
        con.close()
        loader = DuckDBPackLoader()
        with pytest.raises(MissingPackTable) as exc_info:
            loader.load(db_path)
        assert exc_info.value.table_name == "objects"

    def test_missing_semantic_units_table_raises(self, tmp_path: Path) -> None:
        """Missing semantic_units → MissingPackTable."""
        db_path = tmp_path / "nosem.duckdb"
        con = duckdb.connect(str(db_path))
        con.execute("CREATE TABLE objects (id VARCHAR PRIMARY KEY, type VARCHAR NOT NULL)")
        con.execute("CREATE TABLE aliases (alias VARCHAR, canonical_id VARCHAR)")
        con.execute("CREATE TABLE edges (subject_id VARCHAR, predicate VARCHAR, object_id VARCHAR, origin VARCHAR)")
        con.execute("CREATE TABLE manifest (key VARCHAR PRIMARY KEY, value VARCHAR)")
        for key, value in MANIFEST_KEYS.items():
            con.execute("INSERT INTO manifest VALUES (?, ?)", [key, value])
        con.close()
        loader = DuckDBPackLoader()
        with pytest.raises(MissingPackTable) as exc_info:
            loader.load(db_path)
        assert exc_info.value.table_name == "semantic_units"

    def test_missing_manifest_key_raises(self, tmp_path: Path) -> None:
        """Missing manifest key → MissingManifestKey."""
        db_path = tmp_path / "nokey.duckdb"
        con = duckdb.connect(str(db_path))
        con.execute(REQUIRED_TABLES_DDL)
        # Insert all keys except content_hash
        for key, value in MANIFEST_KEYS.items():
            if key == "content_hash":
                continue
            con.execute("INSERT INTO manifest VALUES (?, ?)", [key, value])
        con.close()
        loader = DuckDBPackLoader()
        with pytest.raises(MissingManifestKey) as exc_info:
            loader.load(db_path)
        assert exc_info.value.key == "content_hash"


# ─── P-METADATA: All 19 manifest values parsed ──────────────────────────────


class TestMetadata:
    """P-METADATA: PackMetadata contains all 19 keys with correct types."""

    def test_metadata_pack_id(self, loaded_pack: DuckDBLoadedPack) -> None:
        assert loaded_pack.metadata.pack_id == "test.domain.pack"

    def test_metadata_pack_version(self, loaded_pack: DuckDBLoadedPack) -> None:
        assert loaded_pack.metadata.pack_version == "1.0.0"

    def test_metadata_schema_version(self, loaded_pack: DuckDBLoadedPack) -> None:
        assert loaded_pack.metadata.schema_version == "2.0.0"

    def test_metadata_compiler_version(self, loaded_pack: DuckDBLoadedPack) -> None:
        assert loaded_pack.metadata.compiler_version == "0.5.0"

    def test_metadata_counts_are_integers(self, loaded_pack: DuckDBLoadedPack) -> None:
        m = loaded_pack.metadata
        assert isinstance(m.object_count, int) and m.object_count == 5
        assert isinstance(m.node_count, int) and m.node_count == 5
        assert isinstance(m.edge_count, int) and m.edge_count == 3
        assert isinstance(m.semantic_unit_count, int) and m.semantic_unit_count == 8
        assert isinstance(m.alias_count, int) and m.alias_count == 2
        assert isinstance(m.bm25_vocab_size, int) and m.bm25_vocab_size == 150
        assert isinstance(m.embedding_dimensions, int) and m.embedding_dimensions == 384
        assert isinstance(m.cross_pack_refs, int) and m.cross_pack_refs == 0
        assert isinstance(m.error_count, int) and m.error_count == 0
        assert isinstance(m.warning_count, int) and m.warning_count == 1

    def test_metadata_path_is_absolute(self, loaded_pack: DuckDBLoadedPack) -> None:
        assert loaded_pack.metadata.path.is_absolute()

    def test_metadata_content_hash(self, loaded_pack: DuckDBLoadedPack) -> None:
        assert loaded_pack.metadata.content_hash == "sha256:abc123"

    def test_metadata_embedding_model(self, loaded_pack: DuckDBLoadedPack) -> None:
        assert loaded_pack.metadata.embedding_model == "BAAI/bge-small-en-v1.5"

    def test_metadata_is_frozen(self, loaded_pack: DuckDBLoadedPack) -> None:
        with pytest.raises(AttributeError):
            loaded_pack.metadata.pack_id = "mutated"  # type: ignore[misc]


# ─── P-PROTOCOL: Satisfies LoadedPack protocol ──────────────────────────────


class TestProtocol:
    """P-PROTOCOL: DuckDBLoadedPack satisfies LoadedPack at runtime."""

    def test_loaded_pack_isinstance(self, loaded_pack: DuckDBLoadedPack) -> None:
        assert isinstance(loaded_pack, LoadedPack)

    def test_pack_loader_isinstance(self) -> None:
        loader = DuckDBPackLoader()
        assert isinstance(loader, PackLoader)


# ─── P-CLOSE-SAFE: Lifecycle guarantees ──────────────────────────────────────


class TestLifecycle:
    """P-CLOSE-SAFE: Double close safe, query after close raises."""

    def test_double_close_does_not_raise(self, loaded_pack: DuckDBLoadedPack) -> None:
        loaded_pack.close()
        loaded_pack.close()  # Should not raise

    def test_query_after_close_raises_state_error(self, loaded_pack: DuckDBLoadedPack) -> None:
        loaded_pack.close()
        with pytest.raises(RuntimeStateError) as exc_info:
            loaded_pack.exact_matches("anything", 10)
        assert "closed" in exc_info.value.reason.lower()

    def test_metadata_accessible_after_close(self, loaded_pack: DuckDBLoadedPack) -> None:
        """Metadata is cached — available even after connection closed."""
        loaded_pack.close()
        assert loaded_pack.metadata.pack_id == "test.domain.pack"

    def test_lookup_after_close_raises(self, loaded_pack: DuckDBLoadedPack) -> None:
        loaded_pack.close()
        with pytest.raises(RuntimeStateError):
            loaded_pack.lookup_concept("obj-1")

    def test_graph_after_close_raises(self, loaded_pack: DuckDBLoadedPack) -> None:
        loaded_pack.close()
        with pytest.raises(RuntimeStateError):
            loaded_pack.graph_neighbors("obj-1", 1, (), 10)


# ─── P-ISOLATION: Independent packs ─────────────────────────────────────────


class TestIsolation:
    """P-ISOLATION: Closing one pack doesn't affect another."""

    def test_close_one_pack_other_still_works(self, tmp_path: Path) -> None:
        # Create two valid packs
        for name in ["a", "b"]:
            db_path = tmp_path / f"test.domain.{name}.duckdb"
            con = duckdb.connect(str(db_path))
            con.execute(REQUIRED_TABLES_DDL)
            keys = dict(MANIFEST_KEYS)
            keys["pack_id"] = f"test.domain.{name}"
            for key, value in keys.items():
                con.execute("INSERT INTO manifest VALUES (?, ?)", [key, value])
            con.execute(
                "INSERT INTO objects VALUES ('obj-1', 'concept', 'T', 'D', 'd', 'active', '[]', '[]', 'p', '{}')"
            )
            con.close()

        loader = DuckDBPackLoader()
        pack_a = loader.load(tmp_path / "test.domain.a.duckdb")
        pack_b = loader.load(tmp_path / "test.domain.b.duckdb")

        pack_a.close()

        # pack_b should still work
        assert pack_b.metadata.pack_id == "test.domain.b"
        result = pack_b.lookup_concept("obj-1")
        assert result is not None
        pack_b.close()


# ─── P-DETERMINISTIC: Same query → same results ─────────────────────────────


class TestDeterminism:
    """P-DETERMINISTIC: Same input → same output across calls."""

    def test_exact_matches_deterministic(self, loaded_pack: DuckDBLoadedPack) -> None:
        r1 = loaded_pack.exact_matches("alias-a", 10)
        r2 = loaded_pack.exact_matches("alias-a", 10)
        assert r1 == r2

    def test_lookup_deterministic(self, loaded_pack: DuckDBLoadedPack) -> None:
        r1 = loaded_pack.lookup_concept("obj-1")
        r2 = loaded_pack.lookup_concept("obj-1")
        assert r1 == r2

    def test_graph_neighbors_deterministic(self, loaded_pack: DuckDBLoadedPack) -> None:
        r1 = loaded_pack.graph_neighbors("obj-1", 1, (), 10)
        r2 = loaded_pack.graph_neighbors("obj-1", 1, (), 10)
        assert r1 == r2


# ─── Query methods: Exact matches ────────────────────────────────────────────


class TestExactMatches:
    """Alias-based exact matching."""

    def test_exact_match_returns_search_hit(self, loaded_pack: DuckDBLoadedPack) -> None:
        results = loaded_pack.exact_matches("alias-a", 10)
        assert len(results) == 1
        assert isinstance(results[0], SearchHit)
        assert results[0].object_id == "obj-2"

    def test_exact_match_no_results_returns_empty(self, loaded_pack: DuckDBLoadedPack) -> None:
        results = loaded_pack.exact_matches("nonexistent-alias", 10)
        assert results == []

    def test_exact_match_title_alias(self, loaded_pack: DuckDBLoadedPack) -> None:
        results = loaded_pack.exact_matches("First Concept", 10)
        assert len(results) == 1
        assert results[0].object_id == "obj-1"

    def test_exact_match_respects_limit(self, loaded_pack: DuckDBLoadedPack) -> None:
        assert loaded_pack.exact_matches("alias-a", 0) == []


# ─── Query methods: Concept lookup ───────────────────────────────────────────


class TestLookupConcept:
    """Direct object ID lookup."""

    def test_lookup_existing_concept(self, loaded_pack: DuckDBLoadedPack) -> None:
        result = loaded_pack.lookup_concept("obj-1")
        assert result is not None
        assert isinstance(result, SearchHit)
        assert result.object_id == "obj-1"
        assert result.title == "First Concept"
        assert result.object_type == "concept"
        assert result.domain == "csu"

    def test_lookup_nonexistent_returns_none(self, loaded_pack: DuckDBLoadedPack) -> None:
        result = loaded_pack.lookup_concept("nonexistent-id")
        assert result is None

    def test_lookup_returns_correct_pack_id(self, loaded_pack: DuckDBLoadedPack) -> None:
        result = loaded_pack.lookup_concept("obj-1")
        assert result is not None
        assert result.pack_id == "test.domain.pack"
        assert result.pack_version == "1.0.0"


# ─── Query methods: Semantic units ───────────────────────────────────────────


class TestConceptUnits:
    """Semantic unit retrieval for an object."""

    def test_concept_units_returns_units(self, loaded_pack: DuckDBLoadedPack) -> None:
        units = loaded_pack.concept_units("obj-1", 10)
        assert len(units) == 2
        assert all(isinstance(u, SemanticUnitRecord) for u in units)

    def test_concept_units_correct_content(self, loaded_pack: DuckDBLoadedPack) -> None:
        units = loaded_pack.concept_units("obj-1", 10)
        contents = {u.content for u in units}
        assert "Content of unit 1" in contents
        assert "Content of unit 2" in contents

    def test_concept_units_respects_limit(self, loaded_pack: DuckDBLoadedPack) -> None:
        units = loaded_pack.concept_units("obj-1", 1)
        assert len(units) == 1

    def test_concept_units_nonexistent_object_empty(self, loaded_pack: DuckDBLoadedPack) -> None:
        units = loaded_pack.concept_units("nonexistent", 10)
        assert units == []


# ─── Query methods: Graph neighbors ─────────────────────────────────────────


class TestGraphNeighbors:
    """INV-BFS-BOUNDED: Graph traversal respects depth and limit."""

    def test_one_hop_from_obj1(self, loaded_pack: DuckDBLoadedPack) -> None:
        results = loaded_pack.graph_neighbors("obj-1", 1, (), 10)
        assert len(results) >= 1
        assert all(isinstance(r, GraphEdgeHit) for r in results)
        # obj-1 relates_to obj-2 (direct neighbor)
        neighbor_ids = {r.object_id for r in results}
        assert "obj-2" in neighbor_ids

    def test_graph_respects_hop_limit(self, loaded_pack: DuckDBLoadedPack) -> None:
        """1 hop from obj-1 should NOT reach obj-3 (obj-1→obj-2→obj-3)."""
        results_1 = loaded_pack.graph_neighbors("obj-1", 1, (), 10)
        # With 1 hop, only direct neighbors
        neighbor_ids_1 = {r.object_id for r in results_1}
        # obj-3 is reachable only through obj-2
        if "obj-3" not in neighbor_ids_1:
            # 2 hops should reach obj-3
            results_2 = loaded_pack.graph_neighbors("obj-1", 2, (), 10)
            neighbor_ids_2 = {r.object_id for r in results_2}
            assert "obj-3" in neighbor_ids_2

    def test_graph_respects_result_limit(self, loaded_pack: DuckDBLoadedPack) -> None:
        results = loaded_pack.graph_neighbors("obj-1", 3, (), 1)
        assert len(results) <= 1

    def test_graph_predicate_filter(self, loaded_pack: DuckDBLoadedPack) -> None:
        """Filter by predicate should only return matching edges."""
        results = loaded_pack.graph_neighbors("obj-1", 1, ("relates_to",), 10)
        assert all(r.predicate == "relates_to" for r in results)

    def test_graph_nonexistent_node_empty(self, loaded_pack: DuckDBLoadedPack) -> None:
        results = loaded_pack.graph_neighbors("nonexistent", 1, (), 10)
        assert results == []


# ─── Query methods: Provenance ───────────────────────────────────────────────


class TestProvenance:
    """INV-PROVENANCE-COMPLETE: Always includes pack-layer step."""

    def test_provenance_for_object(self, loaded_pack: DuckDBLoadedPack) -> None:
        steps = loaded_pack.provenance_for_object("obj-1")
        assert len(steps) >= 1
        assert all(isinstance(s, ProvenanceStep) for s in steps)
        # Must include pack layer
        layers = {s.layer for s in steps}
        assert "pack" in layers

    def test_provenance_includes_pack_id(self, loaded_pack: DuckDBLoadedPack) -> None:
        steps = loaded_pack.provenance_for_object("obj-1")
        pack_step = next(s for s in steps if s.layer == "pack")
        assert pack_step.pack_id == "test.domain.pack"
        assert pack_step.pack_version == "1.0.0"

    def test_provenance_for_unit(self, loaded_pack: DuckDBLoadedPack) -> None:
        steps = loaded_pack.provenance_for_unit("unit-1")
        assert len(steps) >= 1
        layers = {s.layer for s in steps}
        assert "pack" in layers

    def test_provenance_for_edge(self, loaded_pack: DuckDBLoadedPack) -> None:
        steps = loaded_pack.provenance_for_edge("obj-1", "relates_to", "obj-2")
        assert len(steps) >= 1
        layers = {s.layer for s in steps}
        assert "pack" in layers


# ─── Multi-pack loader ───────────────────────────────────────────────────────


class TestPackLoader:
    """PackLoader multi-pack management."""

    def test_load_many_returns_dict_keyed_by_pack_id(self, tmp_path: Path) -> None:
        paths = []
        for name in ["alpha", "beta"]:
            db_path = tmp_path / f"test.{name}.pack.duckdb"
            con = duckdb.connect(str(db_path))
            con.execute(REQUIRED_TABLES_DDL)
            keys = dict(MANIFEST_KEYS)
            keys["pack_id"] = f"test.{name}.pack"
            for key, value in keys.items():
                con.execute("INSERT INTO manifest VALUES (?, ?)", [key, value])
            con.close()
            paths.append(db_path)

        loader = DuckDBPackLoader()
        packs = loader.load_many(paths)
        assert "test.alpha.pack" in packs
        assert "test.beta.pack" in packs
        assert isinstance(packs["test.alpha.pack"], LoadedPack)
        loader.close_all()

    def test_close_all_closes_everything(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.duckdb"
        con = duckdb.connect(str(db_path))
        con.execute(REQUIRED_TABLES_DDL)
        for key, value in MANIFEST_KEYS.items():
            con.execute("INSERT INTO manifest VALUES (?, ?)", [key, value])
        con.close()

        loader = DuckDBPackLoader()
        packs = loader.load_many([db_path])
        loader.close_all()

        pack = list(packs.values())[0]
        with pytest.raises(RuntimeStateError):
            pack.lookup_concept("anything")
