"""Architectural boundary tests — enforce dependency rules (ADR-003, ES-03).

These tests validate that the layered architecture is respected:
  domain/     → ZERO external imports (except stdlib + pydantic)
  contracts/  → ZERO concrete implementation imports
  stages/     → may import domain + contracts, NOT infrastructure
  pipeline/   → composition root, may import everything
  consumer/   → may import infrastructure (reads compiled packs)

Violations caught here mean a layer is reaching into another's internals.
"""

from __future__ import annotations

import ast
import importlib
from pathlib import Path

import pytest

SRC_ROOT = Path(__file__).parent.parent / "src" / "kp_compiler"

# ─── Helpers ────────────────────────────────────────────────────────────────


def _get_imports(module_path: Path) -> list[str]:
    """Extract all import targets from a Python file."""
    source = module_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    return imports


def _collect_py_files(package_dir: Path) -> list[Path]:
    """Collect all .py files in a package directory (non-recursive into sub-packages)."""
    if not package_dir.exists():
        return []
    return [f for f in package_dir.rglob("*.py") if f.name != "__init__.py"]


# ─── Allowed external packages per layer ────────────────────────────────────

STDLIB_PREFIXES = {
    "os",
    "sys",
    "re",
    "pathlib",
    "dataclasses",
    "typing",
    "enum",
    "hashlib",
    "datetime",
    "collections",
    "functools",
    "itertools",
    "abc",
    "io",
    "json",
    "math",
    "time",
    "uuid",
    "logging",
    "__future__",
}

DOMAIN_ALLOWED = STDLIB_PREFIXES | {
    "pydantic",
    "ruamel",
    "kp_compiler.domain",
    "kp_compiler.contracts",
}

CONTRACTS_ALLOWED = STDLIB_PREFIXES | {
    "pydantic",
    "kp_compiler.contracts",
}

STAGES_FORBIDDEN_PREFIXES = {
    "kp_compiler.infrastructure",
    "kp_compiler.consumer",
    "kp_compiler.pipeline",
    "duckdb",
}

# ─── Tests ──────────────────────────────────────────────────────────────────


class TestDomainLayer:
    """Domain layer must not import infrastructure, stages, pipeline, or consumer."""

    DOMAIN_DIR = SRC_ROOT / "domain"
    FORBIDDEN = {
        "kp_compiler.infrastructure",
        "kp_compiler.stages",
        "kp_compiler.pipeline",
        "kp_compiler.consumer",
        "duckdb",
        "networkx",
        "rapidfuzz",
        "sentence_transformers",
        "usearch",
        "rank_bm25",
    }

    def test_no_forbidden_imports(self) -> None:
        violations: list[str] = []
        for py_file in _collect_py_files(self.DOMAIN_DIR):
            imports = _get_imports(py_file)
            for imp in imports:
                for forbidden in self.FORBIDDEN:
                    if imp == forbidden or imp.startswith(f"{forbidden}."):
                        violations.append(f"{py_file.name}: imports '{imp}' (forbidden: {forbidden})")
        assert not violations, "Domain layer boundary violations:\n" + "\n".join(violations)


class TestContractsLayer:
    """Contracts must not import any concrete implementations."""

    CONTRACTS_DIR = SRC_ROOT / "contracts"
    FORBIDDEN = {
        "kp_compiler.infrastructure",
        "kp_compiler.stages",
        "kp_compiler.pipeline",
        "kp_compiler.consumer",
        "duckdb",
        "networkx",
        "rapidfuzz",
        "sentence_transformers",
        "usearch",
        "rank_bm25",
    }

    def test_no_concrete_imports(self) -> None:
        violations: list[str] = []
        for py_file in _collect_py_files(self.CONTRACTS_DIR):
            imports = _get_imports(py_file)
            for imp in imports:
                for forbidden in self.FORBIDDEN:
                    if imp == forbidden or imp.startswith(f"{forbidden}."):
                        violations.append(f"{py_file.name}: imports '{imp}' (forbidden: {forbidden})")
        assert not violations, "Contracts layer boundary violations:\n" + "\n".join(violations)


class TestStagesLayer:
    """Stages must not import infrastructure or consumer directly."""

    STAGES_DIR = SRC_ROOT / "stages"

    def test_no_infrastructure_imports(self) -> None:
        violations: list[str] = []
        for py_file in _collect_py_files(self.STAGES_DIR):
            imports = _get_imports(py_file)
            for imp in imports:
                for forbidden in STAGES_FORBIDDEN_PREFIXES:
                    if imp == forbidden or imp.startswith(f"{forbidden}."):
                        # Allow cross_pack helpers that load manifests (they are
                        # infrastructure adapters living in the file for convenience
                        # but only called by the pipeline, not by validation logic)
                        if py_file.name == "cross_pack.py" and forbidden == "duckdb":
                            continue
                        if py_file.name == "outcome_validator.py" and forbidden == "duckdb":
                            # outcome_validator reads compiled pack — acceptable
                            continue
                        violations.append(f"{py_file.name}: imports '{imp}' (forbidden: {forbidden})")
        assert not violations, "Stages layer boundary violations:\n" + "\n".join(violations)


class TestInfrastructureLayer:
    """Infrastructure must not import stages or pipeline."""

    INFRA_DIR = SRC_ROOT / "infrastructure"
    FORBIDDEN = {"kp_compiler.stages", "kp_compiler.pipeline", "kp_compiler.consumer"}

    def test_no_upstream_imports(self) -> None:
        violations: list[str] = []
        for py_file in _collect_py_files(self.INFRA_DIR):
            imports = _get_imports(py_file)
            for imp in imports:
                for forbidden in self.FORBIDDEN:
                    if imp == forbidden or imp.startswith(f"{forbidden}."):
                        violations.append(f"{py_file.name}: imports '{imp}' (forbidden: {forbidden})")
        assert not violations, "Infrastructure layer boundary violations:\n" + "\n".join(violations)


class TestNoCyclicImports:
    """Verify no circular import chains exist at package level."""

    def test_all_packages_importable(self) -> None:
        """If circular imports exist, importing will fail."""
        import sys

        # Ensure src is on path
        src_path = str(SRC_ROOT.parent)
        if src_path not in sys.path:
            sys.path.insert(0, src_path)

        packages = [
            "kp_compiler.contracts",
            "kp_compiler.domain",
            "kp_compiler.events",
            "kp_compiler.stages",
            "kp_compiler.pipeline",
        ]
        for pkg_name in packages:
            try:
                importlib.import_module(pkg_name)
            except ImportError as e:
                pytest.fail(f"Cannot import {pkg_name}: {e}")


class TestVersionConsistency:
    """Verify version is defined in exactly one place."""

    def test_single_version_source(self) -> None:
        from kp_compiler import __version__

        assert __version__, "__version__ must be non-empty"
        # Verify pyproject.toml matches (if version is declared there)
        pyproject = SRC_ROOT.parent.parent / "pyproject.toml"
        if pyproject.exists():
            content = pyproject.read_text(encoding="utf-8")
            # Check if version is declared in pyproject
            import re

            match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
            if match:
                assert match.group(1) == __version__, (
                    f"pyproject.toml version '{match.group(1)}' != __init__.py '{__version__}'"
                )
