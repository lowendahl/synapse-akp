"""Tests for PackSourceResolver — verifies resolution chain logic."""

from __future__ import annotations

from pathlib import Path

import pytest

from akp_runtime.contracts.mcp_config import PackBindingModel
from akp_runtime.infrastructure.pack_source_resolver import PackResolutionError, PackSourceResolver


@pytest.fixture()
def temp_pack(tmp_path: Path) -> Path:
    """Create a temp .duckdb file for testing."""
    pack_file = tmp_path / "test.duckdb"
    pack_file.write_bytes(b"FAKE_DUCKDB_CONTENT")
    return pack_file


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


class TestFileUriResolution:
    """Test file:// URI resolution."""

    def test_resolves_file_uri(self, resolver: PackSourceResolver, temp_pack: Path) -> None:
        binding = PackBindingModel(pack_id="test", source=f"file://{temp_pack}")
        result = resolver.resolve(binding)
        assert result == temp_pack

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


class TestCacheResolution:
    """Test cache-first resolution."""

    def test_uses_cache_if_exists(self, resolver: PackSourceResolver, tmp_path: Path) -> None:
        cache_path = tmp_path / "cache" / "cached.duckdb"
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_bytes(b"CACHED_CONTENT")

        binding = PackBindingModel(
            pack_id="cached",
            source="github://owner/repo/releases/latest/test.duckdb",
            local_cache=cache_path,
        )
        result = resolver.resolve(binding)
        assert result == cache_path

    def test_skips_empty_cache(self, resolver: PackSourceResolver, tmp_path: Path) -> None:
        cache_path = tmp_path / "cache" / "empty.duckdb"
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_bytes(b"")  # empty file

        fallback = tmp_path / "real.duckdb"
        fallback.write_bytes(b"REAL_CONTENT")

        binding = PackBindingModel(
            pack_id="test",
            source="github://owner/repo/releases/latest/missing.duckdb",
            local_cache=cache_path,
            fallback=fallback,
        )
        result = resolver.resolve(binding)
        assert result == fallback


class TestFallbackChain:
    """Test full resolution chain with fallback."""

    def test_source_then_fallback(self, resolver: PackSourceResolver, temp_pack: Path, tmp_path: Path) -> None:
        binding = PackBindingModel(
            pack_id="chain",
            source=f"file://{tmp_path / 'primary.duckdb'}",  # doesn't exist
            fallback=temp_pack,  # exists
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
            source="github://invalid",  # too few parts
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
