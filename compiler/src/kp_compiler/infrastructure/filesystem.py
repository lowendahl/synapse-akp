"""Filesystem adapter — reads source files from disk.

What: Discovers and reads OKF markdown files.
Why: Isolates filesystem IO from domain logic (ES-03, ES-11, ES-12).
Contracts: Implements SourceReader protocol.
Boundaries: Only file in compiler that uses pathlib for reading corpus files.
Test strategy: Integration tests with real temp directories.
"""

from __future__ import annotations

import fnmatch
from collections.abc import Sequence
from pathlib import Path

from kp_compiler.contracts.stage_protocols import SourceReader


class FilesystemReader(SourceReader):
    """Reads OKF source files from disk. Implements SourceReader protocol."""

    def discover(self, root: Path, exclude: Sequence[str] | None = None) -> list[Path]:
        """Discover all .md files under root, excluding reserved patterns and any file
        whose path (relative to root, posix-style) matches one of the `exclude` globs.

        A pattern ending in `/**` excludes a whole subtree (e.g. `assets/**`); other
        patterns are matched with fnmatch (e.g. `*.draft.md`, `notes/scratch-*.md`)."""
        patterns = [p.strip().replace("\\", "/") for p in (exclude or []) if p and p.strip()]
        files: list[Path] = []
        for path in sorted(root.rglob("*.md")):
            # Skip ADR directory — those are architectural docs, not knowledge objects
            if "/adr/" in str(path).replace("\\", "/") or "\\adr\\" in str(path):
                continue
            relative = path.relative_to(root).as_posix()
            if any(self._matches(relative, pattern) for pattern in patterns):
                continue
            files.append(path)
        return files

    @staticmethod
    def _matches(relative: str, pattern: str) -> bool:
        if pattern.endswith("/**"):
            prefix = pattern[:-3].rstrip("/")
            return relative == prefix or relative.startswith(prefix + "/")
        return fnmatch.fnmatch(relative, pattern)

    def read(self, path: Path) -> str:
        """Read file content as UTF-8 string."""
        return path.read_text(encoding="utf-8")
