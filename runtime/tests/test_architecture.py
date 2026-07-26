"""Architectural boundary tests for the AKP Runtime package.

Enforces layer dependency rules:
- contracts/ and domain/ MUST NOT import infrastructure, operations, pipeline, consumer
- operations/ MUST NOT import consumer or pipeline
- infrastructure/ MUST NOT import operations, pipeline, consumer
- consumer/ MUST NOT import infrastructure directly (goes through pipeline)
- Only infrastructure/duckdb_loader.py may import duckdb
- Only infrastructure/usearch_reader.py may import usearch
- Only infrastructure/fastembed_adapter.py may import fastembed
"""

from __future__ import annotations

import ast
from pathlib import Path

RUNTIME_SRC = Path(__file__).parent.parent / "src" / "akp_runtime"


def _get_imports(filepath: Path) -> set[str]:
    """Extract all import names from a Python file using AST."""
    try:
        tree = ast.parse(filepath.read_text(encoding="utf-8"))
    except SyntaxError:
        return set()

    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split(".")[0])
    return imports


def _get_full_imports(filepath: Path) -> set[str]:
    """Extract full dotted import paths from a Python file."""
    try:
        tree = ast.parse(filepath.read_text(encoding="utf-8"))
    except SyntaxError:
        return set()

    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)
    return imports


class TestLayerBoundaries:
    """Contracts and domain MUST NOT depend on upper layers."""

    def test_contracts_no_infra_imports(self) -> None:
        contracts_dir = RUNTIME_SRC / "contracts"
        if not contracts_dir.exists():
            return
        forbidden = {"infrastructure", "operations", "pipeline", "consumer"}
        for py_file in contracts_dir.rglob("*.py"):
            imports = _get_full_imports(py_file)
            for imp in imports:
                parts = imp.replace("akp_runtime.", "").split(".")
                assert parts[0] not in forbidden, (
                    f"{py_file.name} imports forbidden layer: {imp}"
                )

    def test_domain_no_infra_imports(self) -> None:
        domain_dir = RUNTIME_SRC / "domain"
        if not domain_dir.exists():
            return
        forbidden = {"infrastructure", "operations", "pipeline", "consumer"}
        for py_file in domain_dir.rglob("*.py"):
            imports = _get_full_imports(py_file)
            for imp in imports:
                parts = imp.replace("akp_runtime.", "").split(".")
                assert parts[0] not in forbidden, (
                    f"{py_file.name} imports forbidden layer: {imp}"
                )

    def test_operations_no_consumer_imports(self) -> None:
        ops_dir = RUNTIME_SRC / "operations"
        if not ops_dir.exists():
            return
        forbidden = {"consumer", "pipeline"}
        for py_file in ops_dir.rglob("*.py"):
            imports = _get_full_imports(py_file)
            for imp in imports:
                parts = imp.replace("akp_runtime.", "").split(".")
                assert parts[0] not in forbidden, (
                    f"{py_file.name} imports forbidden layer: {imp}"
                )


class TestDependencyIsolation:
    """External dependencies confined to specific adapters."""

    def test_only_duckdb_loader_imports_duckdb(self) -> None:
        for py_file in RUNTIME_SRC.rglob("*.py"):
            if py_file.name == "duckdb_loader.py":
                continue
            imports = _get_imports(py_file)
            assert "duckdb" not in imports, (
                f"{py_file.relative_to(RUNTIME_SRC)} must not import duckdb"
            )

    def test_only_usearch_reader_imports_usearch(self) -> None:
        for py_file in RUNTIME_SRC.rglob("*.py"):
            if py_file.name == "usearch_reader.py":
                continue
            imports = _get_imports(py_file)
            assert "usearch" not in imports, (
                f"{py_file.relative_to(RUNTIME_SRC)} must not import usearch"
            )

    def test_only_fastembed_adapter_imports_fastembed(self) -> None:
        for py_file in RUNTIME_SRC.rglob("*.py"):
            if py_file.name == "fastembed_adapter.py":
                continue
            imports = _get_imports(py_file)
            assert "fastembed" not in imports, (
                f"{py_file.relative_to(RUNTIME_SRC)} must not import fastembed"
            )


class TestVersionConsistency:
    """Package version must match pyproject.toml."""

    def test_version_matches_pyproject(self) -> None:
        import tomllib
        pyproject = Path(__file__).parent.parent / "pyproject.toml"
        if not pyproject.exists():
            return
        with open(pyproject, "rb") as f:
            data = tomllib.load(f)
        expected = data["project"]["version"]
        from akp_runtime import __version__
        assert __version__ == expected, (
            f"__init__.__version__={__version__} != pyproject.toml version={expected}"
        )


class TestNoCompilerImports:
    """Runtime MUST NOT import from the compiler package."""

    def test_no_kp_compiler_imports(self) -> None:
        for py_file in RUNTIME_SRC.rglob("*.py"):
            imports = _get_full_imports(py_file)
            for imp in imports:
                assert not imp.startswith("kp_compiler"), (
                    f"{py_file.relative_to(RUNTIME_SRC)} imports compiler: {imp}"
                )
