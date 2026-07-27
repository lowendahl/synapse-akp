"""Tests for PackSourceResolver — verifies resolution chain logic."""

from __future__ import annotations

import zipfile
from pathlib import Path

import pytest
import yaml

from akp_runtime.contracts.mcp_config import PackBindingModel
from akp_runtime.infrastructure.pack_source_resolver import (
    PackResolutionError,
    PackSourceResolver,
)


@pytest.fixture()
def temp_pack(tmp_path: Path) -> Path:
    """Create a temp .duckdb file for testing."""
    pack_file = tmp_path / "test.duckdb"
    pack_file.write_bytes(b"FAKE_DUCKDB_CONTENT")
    return pack_file


@pytest.fixture()
def temp_akp(tmp_path: Path) -> Path:
    """Create a temp .akp file (ZIP with manifest + duckdb)."""
    duckdb_content = b"FAKE_DUCKDB_IN_AKP"
    import hashlib

    checksum = hashlib.sha256(duckdb_content).hexdigest()
    manifest = {
        "pack_id": "test",
        "pack_format_version": 1,
        "compiler_version": "0.2.0",
        "schema_version": "2.0.0",
        "content_hash": "abc123",
        "build_timestamp": "2025-01-01T00:00:00Z",
        "embeddings_included": False,
        "artifacts": [
            {"file": "pack.duckdb", "type": "duckdb", "size_bytes": len(duckdb_content), "sha256": checksum}
        ],
        "runtime_minimum_version": "0.1.0",
    }
    akp_path = tmp_path / "test.akp"
    with zipfile.ZipFile(akp_path, "w") as archive:
        archive.writestr("manifest.yaml", yaml.dump(manifest))
        archive.writestr("pack.duckdb", duckdb_content)
    return akp_path


@pytest.fixture()
def resolver(tmp_path: Path) -> PackSourceResolver:
    """Resolver with tmp_path as cache dir."""
    return PackSourceResolver(default_cache_directory=tmp_path / "cache")


class TestLegacyPathResolution:
    """Test backward-compatible path-only resolution."""

    def test_resolves_existing_legacy_path(self, resolver: PackSourceResolver, temp_pack: Path) -> None:
        binding = PackBindingModel(pack_id="test", path=temp_pack)
        result = resolver.resolve(binding)
        assert result == temp_pack

    def test_raises_for_missing_required_pack(self, resolver: PackSourceResolver, tmp_path: Path) -> None:
        binding = PackBindingModel(pack_id="missing", path=tmp_path / "nonexistent.duckdb", required=True)
        with pytest.raises(PackResolutionError) as exc_info:
            resolver.resolve(binding)
        assert "missing" in str(exc_info.value)

    def test_raises_for_missing_optional_pack(self, resolver: PackSourceResolver, tmp_path: Path) -> None:
        binding = PackBindingModel(pack_id="opt", path=tmp_path / "nonexistent.duckdb", required=False)
        with pytest.raises(PackResolutionError):
            resolver.resolve(binding)


class TestAkpResolution:
    """Test .akp package extraction and resolution."""

    def test_resolves_akp_file(self, resolver: PackSourceResolver, temp_akp: Path) -> None:
        binding = PackBindingModel(pack_id="test", path=temp_akp)
        result = resolver.resolve(binding)
        assert result.name == "pack.duckdb"
        assert result.exists()
        assert result.read_bytes() == b"FAKE_DUCKDB_IN_AKP"

    def test_akp_checksum_validation(self, resolver: PackSourceResolver, tmp_path: Path) -> None:
        """Corrupted .akp with wrong checksum should fall through."""
        manifest = {
            "pack_id": "bad",
            "pack_format_version": 1,
            "artifacts": [{"file": "pack.duckdb", "type": "duckdb", "sha256": "wrong_checksum"}],
        }
        akp_path = tmp_path / "bad.akp"
        with zipfile.ZipFile(akp_path, "w") as archive:
            archive.writestr("manifest.yaml", yaml.dump(manifest))
            archive.writestr("pack.duckdb", b"some content")

        binding = PackBindingModel(pack_id="bad", path=akp_path, required=True)
        with pytest.raises(PackResolutionError):
            resolver.resolve(binding)

    def test_incompatible_format_version(self, resolver: PackSourceResolver, tmp_path: Path) -> None:
        """AKP with unsupported format version should fail."""
        manifest = {
            "pack_id": "future",
            "pack_format_version": 99,
            "artifacts": [{"file": "pack.duckdb", "type": "duckdb"}],
        }
        akp_path = tmp_path / "future.akp"
        with zipfile.ZipFile(akp_path, "w") as archive:
            archive.writestr("manifest.yaml", yaml.dump(manifest))
            archive.writestr("pack.duckdb", b"content")

        binding = PackBindingModel(pack_id="future", path=akp_path, required=True)
        with pytest.raises(PackResolutionError):
            resolver.resolve(binding)


class TestFileUriResolution:
    """Test file:// URI resolution."""

    def test_resolves_file_uri_duckdb(self, resolver: PackSourceResolver, temp_pack: Path) -> None:
        binding = PackBindingModel(pack_id="test", source=f"file://{temp_pack}")
        result = resolver.resolve(binding)
        assert result == temp_pack

    def test_resolves_file_uri_akp(self, resolver: PackSourceResolver, temp_akp: Path) -> None:
        binding = PackBindingModel(pack_id="test", source=f"file://{temp_akp}")
        result = resolver.resolve(binding)
        assert result.name == "pack.duckdb"

    def test_file_uri_not_found_falls_to_fallback(
        self, resolver: PackSourceResolver, temp_pack: Path, tmp_path: Path
    ) -> None:
        binding = PackBindingModel(
            pack_id="test",
            source=f"file://{tmp_path / 'nonexistent.duckdb'}",
            fallback=temp_pack,
        )
        result = resolver.resolve(binding)
        assert result == temp_pack


class TestFallbackChain:
    """Test full resolution chain with fallback."""

    def test_source_then_fallback(self, resolver: PackSourceResolver, temp_pack: Path, tmp_path: Path) -> None:
        binding = PackBindingModel(
            pack_id="chain",
            source=f"file://{tmp_path / 'primary.duckdb'}",
            fallback=temp_pack,
        )
        result = resolver.resolve(binding)
        assert result == temp_pack

    def test_all_sources_fail_raises(self, resolver: PackSourceResolver, tmp_path: Path) -> None:
        binding = PackBindingModel(
            pack_id="all-fail",
            source=f"file://{tmp_path / 'nope.duckdb'}",
            fallback=tmp_path / "also-nope.duckdb",
            required=True,
        )
        with pytest.raises(PackResolutionError) as exc_info:
            resolver.resolve(binding)
        assert len(exc_info.value.attempted_sources) >= 2


class TestGithubUriParsing:
    """Test GitHub URI parsing (without actual downloads)."""

    def test_invalid_github_uri_falls_through(self, resolver: PackSourceResolver, temp_pack: Path) -> None:
        binding = PackBindingModel(
            pack_id="test",
            source="github://invalid",
            fallback=temp_pack,
        )
        result = resolver.resolve(binding)
        assert result == temp_pack


class TestChecksum:
    """Test checksum computation."""

    def test_compute_checksum_deterministic(self, temp_pack: Path) -> None:
        checksum_1 = PackSourceResolver.compute_checksum(temp_pack)
        checksum_2 = PackSourceResolver.compute_checksum(temp_pack)
        assert checksum_1 == checksum_2
        assert len(checksum_1) == 64  # SHA-256 hex
