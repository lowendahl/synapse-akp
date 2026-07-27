"""Filesystem adapter — reads source files from disk.

What: Discovers and reads OKF markdown files.
Why: Isolates filesystem IO from domain logic (ES-03, ES-11, ES-12).
Contracts: Implements SourceReader protocol.
Boundaries: Only file in compiler that uses pathlib for reading corpus files.
Test strategy: Integration tests with real temp directories.
"""

from __future__ import annotations

from pathlib import Path

from kp_compiler.contracts.stage_protocols import SourceReader


class FilesystemReader(SourceReader):
    """Reads OKF source files from disk. Implements SourceReader protocol."""

    def discover(self, root: Path) -> list[Path]:
        """Discover all .md files under root, excluding reserved patterns."""
        files: list[Path] = []
        for path in sorted(root.rglob("*.md")):
            # Skip ADR directory — those are architectural docs, not knowledge objects
            if "/adr/" in str(path).replace("\\", "/") or "\\adr\\" in str(path):
                continue
            files.append(path)
        return files

    def read(self, path: Path) -> str:
        """Read file content as UTF-8 string."""
        return path.read_text(encoding="utf-8")
