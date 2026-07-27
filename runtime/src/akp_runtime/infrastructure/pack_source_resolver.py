"""Pack source resolver — resolves pack URIs to local .duckdb file paths.

What: Implements the pack resolution chain (source → cache → fallback).
Why: Decouples pack location from runtime bootstrap; supports local, remote, cached modes.
Contracts: Implements PackResolver protocol from contracts/.
Boundaries: Handles file I/O and HTTP fetching; delegates nothing upstream.
"""

from __future__ import annotations

import hashlib
import logging
import urllib.request
from pathlib import Path
from typing import Any

from akp_runtime.contracts.mcp_config import PackBindingModel

logger = logging.getLogger(__name__)

_GITHUB_SCHEME = "github://"
_FILE_SCHEME = "file://"


class PackResolutionError(Exception):
    """Raised when a pack cannot be resolved from any source."""

    def __init__(self, pack_id: str, attempted_sources: list[str]) -> None:
        self.pack_id = pack_id
        self.attempted_sources = attempted_sources
        sources_text = ", ".join(attempted_sources) if attempted_sources else "none"
        super().__init__(f"Cannot resolve pack '{pack_id}' — tried: {sources_text}")


class PackSourceResolver:
    """Resolves pack bindings to local .duckdb file paths.

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

        # 1. Check local cache
        cache_path = source_model.local_cache or self._default_cache_path(binding.pack_id)
        if cache_path.exists() and cache_path.stat().st_size > 0:
            logger.debug("Pack '%s' resolved from cache: %s", binding.pack_id, cache_path)
            return cache_path

        # 2. Resolve source URI
        source = source_model.source
        if source is not None:
            attempted.append(source)
            resolved = self._resolve_source(source, cache_path, binding.pack_id)
            if resolved is not None:
                return resolved

        # 3. Legacy path field (backward compat)
        if binding.path is not None:
            attempted.append(f"file://{binding.path}")
            if binding.path.exists():
                logger.debug("Pack '%s' resolved from legacy path: %s", binding.pack_id, binding.path)
                return binding.path

        # 4. Fallback
        if source_model.fallback is not None:
            attempted.append(f"fallback:{source_model.fallback}")
            if source_model.fallback.exists():
                logger.debug("Pack '%s' resolved from fallback: %s", binding.pack_id, source_model.fallback)
                return source_model.fallback

        # Nothing worked
        if binding.required:
            raise PackResolutionError(binding.pack_id, attempted)
        else:
            logger.warning("Optional pack '%s' not resolved; skipping", binding.pack_id)
            raise PackResolutionError(binding.pack_id, attempted)

    def _resolve_source(self, source: str, cache_path: Path, pack_id: str) -> Path | None:
        """Resolve a source URI string to a local path."""
        if source.startswith(_FILE_SCHEME):
            local_path = Path(source[len(_FILE_SCHEME) :])
            if local_path.exists():
                logger.debug("Pack '%s' resolved from file URI: %s", pack_id, local_path)
                return local_path
            return None

        if source.startswith(_GITHUB_SCHEME):
            return self._fetch_github_release(source, cache_path, pack_id)

        # Bare path (no scheme)
        local_path = Path(source)
        if local_path.exists():
            return local_path
        return None

    def _fetch_github_release(self, source: str, cache_path: Path, pack_id: str) -> Path | None:
        """Download a pack from a GitHub release asset.

        URI format: github://owner/repo/releases/tag/asset_filename
        For 'latest': github://owner/repo/releases/latest/asset_filename
        """
        parts = source[len(_GITHUB_SCHEME) :].split("/")
        if len(parts) < 5:
            logger.error("Invalid github:// URI for pack '%s': %s", pack_id, source)
            return None

        owner = parts[0]
        repo = parts[1]
        # parts[2] should be "releases"
        tag = parts[3]  # "latest" or a specific tag
        asset_name = "/".join(parts[4:])

        download_url = self._build_github_download_url(owner, repo, tag, asset_name)
        if download_url is None:
            return None

        try:
            return self._download_to_cache(download_url, cache_path, pack_id)
        except Exception:
            logger.exception("Failed to download pack '%s' from %s", pack_id, download_url)
            return None

    def _build_github_download_url(
        self, owner: str, repo: str, tag: str, asset_name: str
    ) -> str | None:
        """Build the download URL for a GitHub release asset."""
        if tag == "latest":
            # Use GitHub API to resolve latest release
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
            # Direct tag URL
            return f"https://github.com/{owner}/{repo}/releases/download/{tag}/{asset_name}"

    def _download_to_cache(self, url: str, cache_path: Path, pack_id: str) -> Path:
        """Download a URL to the cache path with progress logging."""
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

            # Atomic rename
            temp_path.replace(cache_path)
            logger.info("Pack '%s' cached at %s (%d bytes)", pack_id, cache_path, cache_path.stat().st_size)
            return cache_path

        except Exception:
            if temp_path.exists():
                temp_path.unlink()
            raise

    def _default_cache_path(self, pack_id: str) -> Path:
        """Compute the default cache path for a pack."""
        return self._cache_directory / f"{pack_id}.duckdb"

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
