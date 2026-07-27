"""Pack manager — install, refresh, list, remove knowledge packs.

What: Manages the local pack registry (~/.akp/config.yaml) and cache.
Why: Provides a clean UX for consumers who don't want to edit YAML manually.
Boundaries: Consumer layer — delegates to PackSourceResolver for downloads.
"""

from __future__ import annotations

import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from akp_runtime.contracts.mcp_config import PackBindingModel
from akp_runtime.infrastructure.pack_source_resolver import PackResolutionError, PackSourceResolver

_AKP_HOME = Path.home() / ".akp"
_CONFIG_PATH = _AKP_HOME / "config.yaml"
_PACKS_DIR = _AKP_HOME / "packs"


class PackManager:
    """Manages knowledge pack installation and lifecycle."""

    def __init__(self) -> None:
        self._resolver = PackSourceResolver(default_cache_directory=_PACKS_DIR)
        _AKP_HOME.mkdir(parents=True, exist_ok=True)
        _PACKS_DIR.mkdir(parents=True, exist_ok=True)

    def install(self, source: str) -> None:
        """Install a pack from a source URI or file path.

        Supported formats:
          - ./path/to/file.akp                                          → local file
          - https://github.com/org/repo/releases/download/v1/pack.akp   → direct URL
          - github://org/repo/releases/latest/pack.akp                  → GitHub shorthand
          - org/repo/pack_id                                            → shorthand (latest release)
        """
        normalized_source, pack_id = self._normalize_source(source)

        print(f"Installing pack '{pack_id}' from {normalized_source}...")

        binding = PackBindingModel(
            pack_id=pack_id,
            source=normalized_source,
            required=True,
        )

        try:
            resolved_path = self._resolver.resolve(binding)
        except PackResolutionError as error:
            print(f"✗ Failed to install: {error}", file=sys.stderr)
            sys.exit(1)

        # Read manifest from extracted pack
        manifest = self._read_extracted_manifest(pack_id)

        # Register in config
        self._register_pack(pack_id, normalized_source, manifest)

        version = manifest.get("compiler_version", "unknown") if manifest else "unknown"
        print(f"✓ Installed {pack_id} (v{version}, resolved to {resolved_path.name})")

    def list_packs(self) -> None:
        """List installed packs."""
        config = self._load_config()
        packs = config.get("packs", [])

        if not packs:
            print("No packs installed. Use 'akp install <source>' to add one.")
            return

        print(f"{'Pack ID':<20} {'Version':<12} {'Source':<50}")
        print("-" * 82)
        for pack in packs:
            pack_id = pack.get("pack_id", "?")
            version = pack.get("installed_version", "?")
            source = pack.get("source", pack.get("path", "?"))
            # Truncate long sources
            if len(str(source)) > 48:
                source = "..." + str(source)[-45:]
            print(f"{pack_id:<20} {version:<12} {source:<50}")

    def update(self, pack_id: str | None = None) -> None:
        """Refresh one or all packs to their latest version."""
        config = self._load_config()
        packs = config.get("packs", [])

        if not packs:
            print("No packs installed.")
            return

        targets = [p for p in packs if pack_id is None or p.get("pack_id") == pack_id]
        if not targets:
            print(f"Pack '{pack_id}' not found. Run 'akp list' to see installed packs.")
            return

        for pack in targets:
            pid = pack["pack_id"]
            # Clear cache to force re-download
            cache_dir = _PACKS_DIR / pid
            if cache_dir.exists():
                shutil.rmtree(cache_dir)

            source = pack.get("source")
            if not source:
                print(f"  ⚠ {pid}: no remote source, skipping")
                continue

            print(f"  Updating {pid}...")
            binding = PackBindingModel(pack_id=pid, source=source, required=True)
            try:
                self._resolver.resolve(binding)
                manifest = self._read_extracted_manifest(pid)
                if manifest:
                    pack["installed_version"] = manifest.get("compiler_version", "unknown")
                    pack["updated_at"] = datetime.now(UTC).isoformat()
                print(f"  ✓ {pid} updated")
            except PackResolutionError as error:
                print(f"  ✗ {pid}: {error}", file=sys.stderr)

        self._save_config(config)

    def remove(self, pack_id: str) -> None:
        """Remove an installed pack."""
        config = self._load_config()
        packs = config.get("packs", [])
        original_count = len(packs)

        config["packs"] = [p for p in packs if p.get("pack_id") != pack_id]

        if len(config["packs"]) == original_count:
            print(f"Pack '{pack_id}' not found.")
            return

        # Remove cached files
        cache_dir = _PACKS_DIR / pack_id
        if cache_dir.exists():
            shutil.rmtree(cache_dir)
        akp_file = _PACKS_DIR / f"{pack_id}.akp"
        if akp_file.exists():
            akp_file.unlink()

        self._save_config(config)
        print(f"✓ Removed {pack_id}")

    def info(self, pack_id: str) -> None:
        """Show detailed pack information."""
        manifest = self._read_extracted_manifest(pack_id)
        if not manifest:
            print(f"Pack '{pack_id}' not found or not extracted. Run 'akp install' first.")
            return

        print(f"Pack: {manifest.get('pack_id', '?')}")
        print(f"Format Version: {manifest.get('pack_format_version', '?')}")
        print(f"Compiler: {manifest.get('compiler_version', '?')}")
        print(f"Schema: {manifest.get('schema_version', '?')}")
        print(f"Content Hash: {manifest.get('content_hash', '?')}")
        print(f"Built: {manifest.get('build_timestamp', '?')}")
        print(f"Embeddings: {'Yes' if manifest.get('embeddings_included') else 'No'}")
        if manifest.get("embeddings_included"):
            print(f"  Model: {manifest.get('embedding_model', '?')}")
            print(f"  Dimensions: {manifest.get('embedding_dimensions', '?')}")
        print("Artifacts:")
        for artifact in manifest.get("artifacts", []):
            size_mb = artifact.get("size_bytes", 0) / (1024 * 1024)
            print(f"  - {artifact['file']} ({artifact['type']}, {size_mb:.1f} MB)")

    def _normalize_source(self, source: str) -> tuple[str, str]:
        """Normalize user input to a source URI and pack_id.

        Supported formats:
          - ./path/to/file.akp              → file:// local path
          - https://host/path/to/pack.akp   → https:// direct download
          - github://org/repo/tag/file.akp  → GitHub release asset
          - file:///absolute/path.akp       → explicit file URI
          - org/repo/pack_id                → shorthand for github latest release
        """
        # Local file
        local_path = Path(source)
        if local_path.exists() and local_path.suffix == ".akp":
            pack_id = local_path.stem
            return f"file://{local_path.resolve()}", pack_id

        # Already a full URI (https://, github://, file://)
        if source.startswith(("https://", "http://", "github://", "file://")):
            parts = source.rstrip("/").split("/")
            pack_id = parts[-1].replace(".akp", "").replace(".duckdb", "")
            return source, pack_id

        # Shorthand: org/repo/pack_id
        parts = source.split("/")
        if len(parts) == 3:
            org, repo, pack_id = parts
            return f"github://{org}/{repo}/releases/latest/{pack_id}.akp", pack_id

        # Shorthand: org/repo (install all packs? just use repo name)
        if len(parts) == 2:
            print(f"Please specify pack_id: {source}/<pack_id>", file=sys.stderr)
            sys.exit(1)

        print(f"Cannot parse source: {source}", file=sys.stderr)
        sys.exit(1)

    def _read_extracted_manifest(self, pack_id: str) -> dict[str, Any] | None:
        """Read manifest.yaml from an extracted pack."""
        manifest_path = _PACKS_DIR / pack_id / "manifest.yaml"
        if not manifest_path.exists():
            return None
        return yaml.safe_load(manifest_path.read_text(encoding="utf-8"))

    def _register_pack(self, pack_id: str, source: str, manifest: dict[str, Any] | None) -> None:
        """Register a pack in ~/.akp/config.yaml."""
        config = self._load_config()
        packs = config.setdefault("packs", [])

        # Remove existing entry for same pack_id
        packs[:] = [p for p in packs if p.get("pack_id") != pack_id]

        entry: dict[str, Any] = {
            "pack_id": pack_id,
            "source": source,
            "required": True,
            "installed_at": datetime.now(UTC).isoformat(),
        }
        if manifest:
            entry["installed_version"] = manifest.get("compiler_version", "unknown")

        packs.append(entry)
        self._save_config(config)

    def _load_config(self) -> dict[str, Any]:
        """Load or create ~/.akp/config.yaml."""
        if _CONFIG_PATH.exists():
            data = yaml.safe_load(_CONFIG_PATH.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        return {"server_name": "akp-runtime", "packs": []}

    def _save_config(self, config: dict[str, Any]) -> None:
        """Save config to ~/.akp/config.yaml."""
        _CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        _CONFIG_PATH.write_text(
            yaml.dump(config, default_flow_style=False, sort_keys=False),
            encoding="utf-8",
        )
