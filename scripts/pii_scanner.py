"""PII and customer data scanner for knowledge pack sources.

Scans OKF Markdown files for patterns that indicate personally identifiable
information or customer-specific data that should never appear in published
knowledge packs.

Exit code 0 = clean, 1 = violations found.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# ── PII Patterns ───────────────────────────────────────────────────────────

PATTERNS: list[tuple[str, str, str]] = [
    # (pattern, description, severity)
    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "Email address", "error"),
    (r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "Phone number", "error"),
    (
        r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
        "UUID/tenant/subscription ID",
        "warning",
    ),
    (r"\b(MSFT|msft)[-/]?\d{6,}\b", "Microsoft internal ticket/case number", "warning"),
    (
        r"https?://[^\s]*[?&](token|key|secret|password|auth)=[^\s&]*",
        "URL with embedded credential",
        "error",
    ),
    (r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b", "Credit card number pattern", "error"),
    (r"\b\d{3}-\d{2}-\d{4}\b", "SSN pattern", "error"),
]

# Known safe patterns (UUIDs that are part of our schema, not customer data)
ALLOWLIST: list[str] = [
    r"generated:\s*\{.*\}",  # YAML frontmatter generated fields
]


class PiiScanner:
    """Scans Markdown files for PII patterns."""

    def __init__(self, patterns: list[tuple[str, str, str]]) -> None:
        self._compiled = [(re.compile(p, re.IGNORECASE), desc, sev) for p, desc, sev in patterns]
        self._allowlist = [re.compile(p) for p in ALLOWLIST]

    def scan_file(self, path: Path) -> list[tuple[int, str, str, str]]:
        """Scan a file, returning (line_number, matched_text, description, severity)."""
        violations: list[tuple[int, str, str, str]] = []
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            return violations

        for line_number, line in enumerate(content.splitlines(), start=1):
            # Skip YAML frontmatter metadata lines
            if any(allow.search(line) for allow in self._allowlist):
                continue

            for pattern, description, severity in self._compiled:
                matches = pattern.findall(line)
                for match in matches:
                    # Redact most of the match for safe reporting
                    redacted = match[:4] + "***" if len(match) > 4 else "***"
                    violations.append((line_number, redacted, description, severity))

        return violations

    def scan_directory(self, directory: Path) -> dict[Path, list[tuple[int, str, str, str]]]:
        """Scan all Markdown files in a directory tree."""
        results: dict[Path, list[tuple[int, str, str, str]]] = {}
        for md_file in sorted(directory.rglob("*.md")):
            violations = self.scan_file(md_file)
            if violations:
                results[md_file] = violations
        return results


def main() -> int:
    """Run PII scan on OKF sources. Returns 0 if clean, 1 if violations found."""
    okf_dir = Path(__file__).resolve().parents[1] / "okf"
    if not okf_dir.exists():
        print(f"OKF directory not found: {okf_dir}", file=sys.stderr)
        return 1

    scanner = PiiScanner(PATTERNS)
    results = scanner.scan_directory(okf_dir)

    if not results:
        print("✓ PII scan clean — no violations detected")
        return 0

    error_count = 0
    warning_count = 0

    for file_path, violations in results.items():
        relative = file_path.relative_to(okf_dir.parent)
        for line_number, redacted, description, severity in violations:
            marker = "ERROR" if severity == "error" else "WARNING"
            print(f"{marker}: {relative}:{line_number} — {description} ({redacted})")
            if severity == "error":
                error_count += 1
            else:
                warning_count += 1

    print(f"\nPII scan complete: {error_count} error(s), {warning_count} warning(s)")

    if error_count > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
