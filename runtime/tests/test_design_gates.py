"""Design quality gates.

Automated enforcement of architecture standards that block merge on violation.
Configuration: docs/architecture/decisions/gates/gate-config.yaml
Rationale: docs/architecture/decisions/gates/README.md
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest
import yaml

RUNTIME_SRC = Path(__file__).parent.parent / "src" / "akp_runtime"
_GATE_CONFIG_PATH = (
    Path(__file__).parent.parent.parent / "docs" / "architecture" / "decisions" / "gates" / "gate-config.yaml"
)

with _GATE_CONFIG_PATH.open(encoding="utf-8") as _f:
    _CONFIG = yaml.safe_load(_f)

MAX_LOGIC_LINES: int = _CONFIG["max_logic_lines"]
ACCEPTED_ACRONYMS = frozenset(_CONFIG["accepted_acronyms"])
ACCEPTED_SHORT_WORDS = frozenset(_CONFIG["accepted_short_words"])
SQL_ALLOWED_DIRS = set(_CONFIG["sql_allowed_directories"])
SQL_ALLOWED_FILE_PATTERNS = set(_CONFIG["sql_allowed_file_patterns"])
EXCLUDED_FILENAMES = {"__init__.py", "__main__.py", "conftest.py"}

_SQL_KEYWORD_PATTERN = re.compile(
    r"\b(SELECT|INSERT|CREATE\s+TABLE|ALTER\s+TABLE|DROP\s+TABLE|UPDATE|DELETE\s+FROM)\b",
    re.IGNORECASE,
)


def _source_files() -> list[Path]:
    if not RUNTIME_SRC.exists():
        return []
    return [f for f in RUNTIME_SRC.rglob("*.py") if f.name not in EXCLUDED_FILENAMES]


def _count_logic_lines(filepath: Path) -> int:
    try:
        source = filepath.read_text(encoding="utf-8")
        ast.parse(source)
    except (SyntaxError, UnicodeDecodeError):
        return 0

    logic_lines = 0
    in_docstring = False

    for line in source.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith('"""') or stripped.startswith("'''"):
            if stripped.count('"""') == 2 or stripped.count("'''") == 2:
                continue
            in_docstring = not in_docstring
            continue
        if in_docstring:
            continue
        logic_lines += 1

    return logic_lines


def _has_class_definition(filepath: Path) -> bool:
    try:
        tree = ast.parse(filepath.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError):
        return False
    return any(isinstance(node, ast.ClassDef) for node in ast.walk(tree))


def _is_reexport_facade(filepath: Path) -> bool:
    try:
        tree = ast.parse(filepath.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError):
        return False
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Assign, ast.Expr)):
            continue
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            return False
    return True


def _find_sql_strings(filepath: Path) -> list[tuple[int, str]]:
    try:
        tree = ast.parse(filepath.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError):
        return []

    return [
        (node.lineno, node.value[:80])
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and _SQL_KEYWORD_PATTERN.search(node.value)
    ]


def _is_sql_allowed_location(filepath: Path) -> bool:
    if set(filepath.parts) & SQL_ALLOWED_DIRS:
        return True
    return any(pattern in filepath.stem.lower() for pattern in SQL_ALLOWED_FILE_PATTERNS)


def _is_abbreviation(word: str) -> bool:
    lower = word.lower()
    if lower in ACCEPTED_ACRONYMS or lower in ACCEPTED_SHORT_WORDS:
        return False
    return len(word) <= 2


class TestModuleSize:
    """No module exceeds the configured logic-line ceiling."""

    def test_all_files_within_limit(self) -> None:
        violations = [
            f"  {filepath.relative_to(RUNTIME_SRC)}: {count} lines (max {MAX_LOGIC_LINES})"
            for filepath in _source_files()
            if (count := _count_logic_lines(filepath)) > MAX_LOGIC_LINES
        ]
        if violations:
            pytest.fail("Gate 1 VIOLATION:\n" + "\n".join(violations))


class TestNoLooseFunctions:
    """Every source module defines at least one class."""

    def test_all_modules_have_classes(self) -> None:
        violations = []
        for filepath in _source_files():
            if _count_logic_lines(filepath) < 5:
                continue
            if _is_reexport_facade(filepath):
                continue
            if not _has_class_definition(filepath):
                violations.append(f"  {filepath.relative_to(RUNTIME_SRC)}")

        if violations:
            pytest.fail("Gate 2 VIOLATION — modules without classes:\n" + "\n".join(violations))


class TestSqlConfinement:
    """SQL strings exist only inside query/persistence directories."""

    def test_sql_only_in_allowed_locations(self) -> None:
        violations = []
        for filepath in _source_files():
            if _is_sql_allowed_location(filepath):
                continue
            for lineno, snippet in _find_sql_strings(filepath):
                violations.append(f"  {filepath.relative_to(RUNTIME_SRC)}:{lineno}: {snippet}...")

        if violations:
            pytest.fail("Gate 3 VIOLATION:\n" + "\n".join(violations))


class TestEventSeparation:
    """Event dataclasses live in contracts/; the bus engine has no event definitions."""

    def test_no_event_definitions_in_bus_implementation(self) -> None:
        events_dir = RUNTIME_SRC / "events"
        if not events_dir.exists():
            return

        violations = []
        for filepath in events_dir.rglob("*.py"):
            if filepath.name in EXCLUDED_FILENAMES:
                continue
            try:
                tree = ast.parse(filepath.read_text(encoding="utf-8"))
            except (SyntaxError, UnicodeDecodeError):
                continue

            for node in ast.walk(tree):
                if not isinstance(node, ast.ClassDef):
                    continue
                for decorator in node.decorator_list:
                    decorator_name = ""
                    if isinstance(decorator, ast.Name):
                        decorator_name = decorator.id
                    elif isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name):
                        decorator_name = decorator.func.id
                    if decorator_name == "dataclass":
                        violations.append(f"  {filepath.relative_to(RUNTIME_SRC)}: '{node.name}' belongs in contracts/")

        if violations:
            pytest.fail("Gate 5 VIOLATION:\n" + "\n".join(violations))


class TestDomainFileConcentration:
    """Domain files hold at most 4 classes to prevent model dumps."""

    MAX_CLASSES_PER_FILE = 4

    def test_no_model_dump_files(self) -> None:
        domain_dir = RUNTIME_SRC / "domain"
        if not domain_dir.exists():
            return

        violations = []
        for filepath in domain_dir.rglob("*.py"):
            if filepath.name in EXCLUDED_FILENAMES:
                continue
            try:
                tree = ast.parse(filepath.read_text(encoding="utf-8"))
            except (SyntaxError, UnicodeDecodeError):
                continue

            class_count = sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))
            if class_count > self.MAX_CLASSES_PER_FILE:
                violations.append(
                    f"  {filepath.relative_to(RUNTIME_SRC)}: {class_count} classes (max {self.MAX_CLASSES_PER_FILE})"
                )

        if violations:
            pytest.fail("Gate 6 VIOLATION:\n" + "\n".join(violations))
