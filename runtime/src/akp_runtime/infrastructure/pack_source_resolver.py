"""Pack source resolver — resolves pack URIs to local .duckdb file paths.

What: Implements the pack resolution chain (source → cache → fallback).
Why: Decouples pack location from runtime bootstrap; supports local, remote, cached modes.
Contracts: Implements PackResolver protocol from contracts/.
Boundaries: Handles file I/O and HTTP fetching; delegates nothing upstream.

Supported formats:
  - .akp files (ZIP containing manifest.yaml + pack.duckdb + optional pack.usearch)
  - .duckdb files (legacy, direct DuckDB access)
"""

from __future__ import annotations

import hashlib
import logging
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

import yaml

from akp_runtime.contracts.mcp_config import PackBindingModel

logger = logging.getLogger(__name__)

_GITHUB_SCHEME = "github://"
_FILE_SCHEME = "file://"
_SUPPORTED_PACK_FORMAT_VERSIONS = {1}


class PackResolutionError(Exception):
    """Raised when a pack cannot be resolved from any source."""

    def __init__(self, pack_id: str, attempted_sources: list[str]) -> None:
        self.pack_id = pack_id
        self.attempted_sources = attempted_sources
        sources_text = ", ".join(attempted_sources) if attempted_sources else "none"
        super().__init__(f"Cannot resolve pack '{pack_id}' — tried: {sources_text}")


class IncompatiblePackError(Exception):
    """Raised when a pack's format version is not supported by this runtime."""

    def __init__(self, pack_id: str, found_version: int) -> None:
        self.pack_id = pack_id
        self.found_version = found_version
        super().__init__(
            f"Pack '{pack_id}' has format version {found_version}, "
            f"but this runtime supports: {_SUPPORTED_PACK_FORMAT_VERSIONS}"
        )


class PackSourceResolver:
    """Resolves pack bindings to local .duckdb file paths.

    Supports both .akp packages (ZIP) and bare .duckdb files.

    Resolution chain for each pack:
    1. If local_cache exists and is valid → use it
    2. If source is file:// → resolve to local path
    3. If source is github:// → download to local_cache, then use it
    4. If fallback path exists → use it
    5. Raise PackResolutionError
    """

    def __init__(self, default_cache_directory: Path | None = None) -> None:
        self._cache_directory = default_cache_directory or (Path.home() / ".akp" / "packs")

    def resolve(self, binding: PackBindingModel) -> Path:
        """Resolve a pack binding to a local .duckdb file path."""
        attempted: list[str] = []
        source_model = binding.resolved_source

        # 1. Check local cache (extracted .duckdb from .akp)
        cache_path = source_model.local_cache or self._default_cache_path(binding.pack_id)
        extracted_duckdb = self._cache_directory / binding.pack_id / "pack.duckdb"
        if extracted_duckdb.exists() and extracted_duckdb.stat().st_size > 0:
            logger.debug("Pack '%s' resolved from extracted cache: %s", binding.pack_id, extracted_duckdb)
            return extracted_duckdb

        # Also check if cache_path itself is a .duckdb
        if cache_path.exists() and cache_path.stat().st_size > 0 and cache_path.suffix == ".duckdb":
            logger.debug("Pack '%s' resolved from cache: %s", binding.pack_id, cache_path)
            return cache_path

        # 2. Resolve source URI
        source = source_model.source
        if source is not None:
            attempted.append(source)
            resolved = self._resolve_source(source, binding.pack_id)
            if resolved is not None:
                return resolved

        # 3. Legacy path field (backward compat)
        if binding.path is not None:
            attempted.append(f"file://{binding.path}")
            resolved = self._resolve_local_file(binding.path, binding.pack_id)
            if resolved is not None:
                return resolved

        # 4. Fallback
        if source_model.fallback is not None:
            attempted.append(f"fallback:{source_model.fallback}")
            resolved = self._resolve_local_file(source_model.fallback, binding.pack_id)
            if resolved is not None:
                return resolved

        # Nothing worked
        raise PackResolutionError(binding.pack_id, attempted)

    def _resolve_local_file(self, path: Path, pack_id: str) -> Path | None:
        """Resolve a local file path — handles both .akp and .duckdb."""
        if not path.exists():
            return None

        if path.suffix == ".akp":
            return self._extract_akp(path, pack_id)
        elif path.suffix == ".duckdb":
            logger.debug("Pack '%s' resolved from local .duckdb: %s", pack_id, path)
            return path
        return None

    def _resolve_source(self, source: str, pack_id: str) -> Path | None:
        """Resolve a source URI string to a local path."""
        if source.startswith(_FILE_SCHEME):
            local_path = Path(source[len(_FILE_SCHEME) :])
            return self._resolve_local_file(local_path, pack_id)

        if source.startswith(_GITHUB_SCHEME):
            return self._fetch_github_release(source, pack_id)

        # Bare path (no scheme)
        local_path = Path(source)
        return self._resolve_local_file(local_path, pack_id)

    def _extract_akp(self, akp_path: Path, pack_id: str) -> Path | None:
        """Extract a .akp package and validate its manifest."""
        extract_dir = self._cache_directory / pack_id
        extract_dir.mkdir(parents=True, exist_ok=True)

        try:
            with zipfile.ZipFile(akp_path, "r") as archive:
                # Read and validate manifest first
                manifest_data = yaml.safe_load(archive.read("manifest.yaml"))
                self._validate_manifest(manifest_data, pack_id)

                # Extract all files
                archive.extractall(extract_dir)

            duckdb_path = extract_dir / "pack.duckdb"
            if not duckdb_path.exists():
                logger.error("Pack '%s': .akp missing pack.duckdb", pack_id)
                return None

            # Verify checksum
            expected = self._find_artifact_checksum(manifest_data, "pack.duckdb")
            if expected:
                actual = self.compute_checksum(duckdb_path)
                if actual != expected:
                    logger.error(
                        "Pack '%s': checksum mismatch (expected %s, got %s)",
                        pack_id,
                        expected[:12],
                        actual[:12],
                    )
                    return None

            logger.info(
                "Pack '%s' extracted from %s (format v%d)",
                pack_id,
                akp_path.name,
                manifest_data.get("pack_format_version", 0),
            )
            return duckdb_path

        except (zipfile.BadZipFile, KeyError, yaml.YAMLError, IncompatiblePackError) as error:
            logger.error("Pack '%s': invalid .akp file — %s", pack_id, error)
            return None

    def _validate_manifest(self, manifest: dict[str, Any], pack_id: str) -> None:
        """Validate pack manifest for compatibility."""
        format_version = manifest.get("pack_format_version", 0)
        if format_version not in _SUPPORTED_PACK_FORMAT_VERSIONS:
            raise IncompatiblePackError(pack_id, format_version)

    def _find_artifact_checksum(self, manifest: dict[str, Any], filename: str) -> str | None:
        """Find SHA-256 checksum for an artifact in the manifest."""
        for artifact in manifest.get("artifacts", []):
            if artifact.get("file") == filename:
                return artifact.get("sha256")
        return None

    def _fetch_github_release(self, source: str, pack_id: str) -> Path | None:
        """Download a .akp from a GitHub release asset."""
        parts = source[len(_GITHUB_SCHEME) :].split("/")
        if len(parts) < 5:
            logger.error("Invalid github:// URI for pack '%s': %s", pack_id, source)
            return None

        owner = parts[0]
        repo = parts[1]
        tag = parts[3]  # "latest" or a specific tag
        asset_name = "/".join(parts[4:])

        download_url = self._build_github_download_url(owner, repo, tag, asset_name)
        if download_url is None:
            return None

        try:
            cache_path = self._cache_directory / f"{pack_id}.akp"
            downloaded = self._download_to_cache(download_url, cache_path, pack_id)
            return self._resolve_local_file(downloaded, pack_id)
        except Exception:
            logger.exception("Failed to download pack '%s' from %s", pack_id, download_url)
            return None

    def _build_github_download_url(self, owner: str, repo: str, tag: str, asset_name: str) -> str | None:
        """Build the download URL for a GitHub release asset."""
        if tag == "latest":
            api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
            try:
                import json

                request = urllib.request.Request(api_url, headers={"Accept": "application/vnd.github+json"})
                with urllib.request.urlopen(request, timeout=30) as response:
                    release_data: dict[str, Any] = json.loads(response.read())
                    assets = release_data.get("assets", [])
                    for asset in assets:
                        if asset.get("name") == asset_name:
                            return str(asset["browser_download_url"])
                    logger.error("Asset '%s' not found in latest release of %s/%s", asset_name, owner, repo)
                    return None
            except Exception:
                logger.exception("Failed to query GitHub API for %s/%s latest release", owner, repo)
                return None
        else:
            return f"https://github.com/{owner}/{repo}/releases/download/{tag}/{asset_name}"

    def _download_to_cache(self, url: str, cache_path: Path, pack_id: str) -> Path:
        """Download a URL to the cache path."""
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = cache_path.with_suffix(".downloading")

        logger.info("Downloading pack '%s' from %s", pack_id, url)

        try:
            request = urllib.request.Request(url)
            with urllib.request.urlopen(request, timeout=120) as response, temp_path.open("wb") as destination:
                while True:
                    chunk = response.read(65536)
                    if not chunk:
                        break
                    destination.write(chunk)

            temp_path.replace(cache_path)
            logger.info("Pack '%s' cached at %s (%d bytes)", pack_id, cache_path, cache_path.stat().st_size)
            return cache_path

        except Exception:
            if temp_path.exists():
                temp_path.unlink()
            raise

    def _default_cache_path(self, pack_id: str) -> Path:
        """Compute the default cache path for a pack."""
        return self._cache_directory / f"{pack_id}.akp"

    @staticmethod
    def compute_checksum(file_path: Path) -> str:
        """Compute SHA-256 checksum of a file."""
        sha256 = hashlib.sha256()
        with file_path.open("rb") as file_handle:
            while True:
                chunk = file_handle.read(65536)
                if not chunk:
                    break
                sha256.update(chunk)
        return sha256.hexdigest()
