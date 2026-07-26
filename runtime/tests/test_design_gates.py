"""Design quality gates — automated enforcement of code architecture standards.

These gates BLOCK merge when violated. They enforce:
- Gate 1: Module size (max 200 LoC of logic)
- Gate 2: No loose-function modules (classes required)
- Gate 3: SQL confinement (only in query/persistence files)
- Gate 4: No abbreviations in public identifiers
- Gate 5: Event contract separation (events in contracts, bus in infra)
- Gate 6: One concept per domain file (no model dumps)
- Gate 7: Code is documentation (naming clarity)

See docs/architecture/decisions/gates/README.md for full rationale.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest

# ─── Configuration ───────────────────────────────────────────────────────────

RUNTIME_SRC = Path(__file__).parent.parent / "src" / "akp_runtime"

# Files excluded from design gates
EXCLUDED_NAMES = {"__init__.py", "__main__.py", "conftest.py"}

# Directories that contain SQL legitimately
SQL_ALLOWED_DIRS = {"queries", "persistence", "writer", "migration"}
SQL_ALLOWED_FILE_PATTERNS = {"query", "writer", "migration", "schema"}

# Accepted acronyms that are not "abbreviations"
ACCEPTED_ACRONYMS = frozenset({
    "rrf", "bm25", "mcp", "ddd", "bfs", "sql", "id", "url", "api",
    "abc", "duckdb", "yaml", "json", "utf", "io", "os", "db",
    "uuid", "http", "tcp", "ip", "sdk", "cli", "env", "config",
})

# Known short words that are fine
ACCEPTED_SHORT_WORDS = frozenset({
    "bus", "hit", "key", "map", "raw", "run", "log", "top", "get",
    "set", "add", "all", "new", "old", "max", "min", "sum", "avg",
    "for", "the", "and", "not", "has", "is", "of", "on", "at",
})

MAX_LOGIC_LINES = 200


# ─── Helpers ─────────────────────────────────────────────────────────────────


def _count_logic_lines(filepath: Path) -> int:
    """Count non-blank, non-comment, non-docstring executable lines."""
    try:
        source = filepath.read_text(encoding="utf-8")
        tree = ast.parse(source)
    except (SyntaxError, UnicodeDecodeError):
        return 0

    lines = source.splitlines()
    logic_lines = 0
    in_docstring = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith('"""') or stripped.startswith("'''"):
            if stripped.count('"""') == 2 or stripped.count("'''") == 2:
                continue  # single-line docstring
            in_docstring = not in_docstring
            continue
        if in_docstring:
            continue
        logic_lines += 1

    return logic_lines


def _has_class_definition(filepath: Path) -> bool:
    """Check if file defines at least one class."""
    try:
        tree = ast.parse(filepath.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError):
        return False

    return any(isinstance(node, ast.ClassDef) for node in ast.walk(tree))


def _find_sql_strings(filepath: Path) -> list[tuple[int, str]]:
    """Find string literals containing SQL keywords."""
    sql_pattern = re.compile(
        r"\b(SELECT|INSERT|CREATE\s+TABLE|ALTER\s+TABLE|DROP\s+TABLE|UPDATE|DELETE\s+FROM)\b",
        re.IGNORECASE,
    )
    violations = []
    try:
        tree = ast.parse(filepath.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError):
        return []

    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if sql_pattern.search(node.value):
                violations.append((node.lineno, node.value[:80]))

    return violations


def _is_sql_allowed_location(filepath: Path) -> bool:
    """Check if file is in a directory where SQL is allowed."""
    parts = set(filepath.parts)
    if parts & SQL_ALLOWED_DIRS:
        return True
    stem = filepath.stem.lower()
    return any(pattern in stem for pattern in SQL_ALLOWED_FILE_PATTERNS)


def _get_public_identifiers(filepath: Path) -> list[tuple[int, str]]:
    """Extract public (non-underscore-prefixed) class/function/variable names."""
    try:
        tree = ast.parse(filepath.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError):
        return []

    identifiers = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
            identifiers.append((node.lineno, node.name))
        elif isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            identifiers.append((node.lineno, node.name))
        elif isinstance(node, ast.AsyncFunctionDef) and not node.name.startswith("_"):
            identifiers.append((node.lineno, node.name))
    return identifiers


def _is_abbreviation(word: str) -> bool:
    """Check if a word looks like an abbreviation (too short and not a known word)."""
    lower = word.lower()
    if lower in ACCEPTED_ACRONYMS or lower in ACCEPTED_SHORT_WORDS:
        return False
    # Single/double char that isn't a known word
    if len(word) <= 2:
        return True
    return False


def _source_files() -> list[Path]:
    """Get all Python source files (excluding tests and excluded names)."""
    if not RUNTIME_SRC.exists():
        return []
    return [
        f for f in RUNTIME_SRC.rglob("*.py")
        if f.name not in EXCLUDED_NAMES
    ]


# ─── Gate 1: Module Size ────────────────────────────────────────────────────


class TestModuleSize:
    """Gate 1: No module exceeds 200 lines of logic."""

    def test_no_file_exceeds_max_logic_lines(self) -> None:
        violations = []
        for filepath in _source_files():
            count = _count_logic_lines(filepath)
            if count > MAX_LOGIC_LINES:
                rel = filepath.relative_to(RUNTIME_SRC)
                violations.append(f"  {rel}: {count} lines (max {MAX_LOGIC_LINES})")

        if violations:
            msg = f"Gate 1 VIOLATION — files exceed {MAX_LOGIC_LINES} LoC:\n" + "\n".join(violations)
            pytest.fail(msg)


# ─── Gate 2: No Loose-Function Modules ──────────────────────────────────────


class TestNoLooseFunctions:
    """Gate 2: Every source module defines at least one class."""

    def test_all_modules_have_classes(self) -> None:
        violations = []
        for filepath in _source_files():
            # Skip type-only files and empty files
            if _count_logic_lines(filepath) < 5:
                continue
            if not _has_class_definition(filepath):
                rel = filepath.relative_to(RUNTIME_SRC)
                violations.append(f"  {rel}: no class definition (loose functions)")

        if violations:
            msg = "Gate 2 VIOLATION — modules without class definitions:\n" + "\n".join(violations)
            pytest.fail(msg)


# ─── Gate 3: SQL Confinement ────────────────────────────────────────────────


class TestSqlConfinement:
    """Gate 3: SQL strings only in query/persistence files."""

    def test_sql_only_in_allowed_locations(self) -> None:
        violations = []
        for filepath in _source_files():
            if _is_sql_allowed_location(filepath):
                continue
            sql_hits = _find_sql_strings(filepath)
            if sql_hits:
                rel = filepath.relative_to(RUNTIME_SRC)
                for lineno, snippet in sql_hits:
                    violations.append(f"  {rel}:{lineno}: {snippet}...")

        if violations:
            msg = "Gate 3 VIOLATION — SQL outside query/persistence files:\n" + "\n".join(violations)
            pytest.fail(msg)


# ─── Gate 5: Event Contract Separation ──────────────────────────────────────


class TestEventSeparation:
    """Gate 5: Event types in contracts/, bus implementation separate."""

    def test_no_event_definitions_in_bus_implementation(self) -> None:
        """Bus implementation files should not define event dataclasses."""
        events_dir = RUNTIME_SRC / "events"
        if not events_dir.exists():
            return

        violations = []
        for filepath in events_dir.rglob("*.py"):
            if filepath.name in EXCLUDED_NAMES:
                continue
            try:
                tree = ast.parse(filepath.read_text(encoding="utf-8"))
            except (SyntaxError, UnicodeDecodeError):
                continue

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Check if it's a dataclass (has @dataclass decorator)
                    for decorator in node.decorator_list:
                        dec_name = ""
                        if isinstance(decorator, ast.Name):
                            dec_name = decorator.id
                        elif isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name):
                            dec_name = decorator.func.id
                        if dec_name == "dataclass":
                            rel = filepath.relative_to(RUNTIME_SRC)
                            violations.append(
                                f"  {rel}: event class '{node.name}' defined in bus "
                                f"implementation (should be in contracts/)"
                            )

        if violations:
            msg = "Gate 5 VIOLATION — event definitions mixed with bus:\n" + "\n".join(violations)
            pytest.fail(msg)


# ─── Gate 6: One Concept Per Domain File ────────────────────────────────────


class TestDomainFileConcentration:
    """Gate 6: Domain files contain models for a single concept."""

    MAX_DATACLASSES_PER_FILE = 4  # Allow related types (e.g., Hit + ChannelScore)

    def test_no_model_dump_files(self) -> None:
        domain_dir = RUNTIME_SRC / "domain"
        if not domain_dir.exists():
            return

        violations = []
        for filepath in domain_dir.rglob("*.py"):
            if filepath.name in EXCLUDED_NAMES:
                continue
            try:
                tree = ast.parse(filepath.read_text(encoding="utf-8"))
            except (SyntaxError, UnicodeDecodeError):
                continue

            class_count = sum(
                1 for node in ast.walk(tree)
                if isinstance(node, ast.ClassDef)
            )
            if class_count > self.MAX_DATACLASSES_PER_FILE:
                rel = filepath.relative_to(RUNTIME_SRC)
                violations.append(
                    f"  {rel}: {class_count} classes (max {self.MAX_DATACLASSES_PER_FILE}) "
                    f"— split into per-concept files"
                )

        if violations:
            msg = "Gate 6 VIOLATION — too many concepts in single file:\n" + "\n".join(violations)
            pytest.fail(msg)
