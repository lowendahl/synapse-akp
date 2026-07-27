"""Tests for compiler-facing entry point wrappers."""

from __future__ import annotations

import sys
from pathlib import Path

import duckdb
import pytest

from kp_compiler import __main__ as package_main
from kp_compiler.cli import CompilerCli
from kp_compiler.cli import main as compiler_main
from kp_compiler.consumer.cli import PackSearcher, expand_graph, search_aliases, search_objects
from kp_compiler.consumer.explorer import ExplorerGenerator
from kp_compiler.consumer.explorer import main as explorer_main


def _make_search_pack(tmp_path: Path) -> Path:
    pack_path = tmp_path / "search.duckdb"
    con = duckdb.connect(str(pack_path))
    con.execute(
        """
        CREATE TABLE objects (
            id VARCHAR PRIMARY KEY,
            type VARCHAR NOT NULL,
            title VARCHAR,
            description VARCHAR,
            domain VARCHAR
        )
        """
    )
    con.execute(
        """
        INSERT INTO objects (id, type, title, description, domain)
        VALUES
            ('csu.metric.c2c', 'KPI', 'Commit to Complete', 'C2C metric', 'csu'),
            ('csu.process.delivery', 'Process', 'Delivery Process', 'Delivery work', 'csu')
        """
    )
    con.execute(
        """
        CREATE TABLE aliases (
            alias VARCHAR NOT NULL,
            canonical_id VARCHAR NOT NULL,
            alias_type VARCHAR NOT NULL
        )
        """
    )
    con.execute(
        """
        INSERT INTO aliases (alias, canonical_id, alias_type)
        VALUES ('C2C', 'csu.metric.c2c', 'explicit')
        """
    )
    con.execute(
        """
        CREATE TABLE edges (
            subject_id VARCHAR NOT NULL,
            predicate VARCHAR NOT NULL,
            object_id VARCHAR NOT NULL
        )
        """
    )
    con.execute(
        """
        INSERT INTO edges (subject_id, predicate, object_id)
        VALUES ('csu.process.delivery', 'measures', 'csu.metric.c2c')
        """
    )
    con.close()
    return pack_path


def test_package_application_dispatches_compile(monkeypatch: pytest.MonkeyPatch) -> None:
    called: list[str] = []
    monkeypatch.setattr(sys, "argv", ["kp", "compile", "okf/csu"])
    monkeypatch.setattr("kp_compiler.cli.main", lambda: called.append("compile"))

    package_main.Application().run()

    assert called == ["compile"]
    assert sys.argv == ["kp", "okf/csu"]


def test_compiler_main_delegates_to_application(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(CompilerCli, "run", lambda self, argv=None: 7)

    with pytest.raises(SystemExit) as excinfo:
        compiler_main()

    assert excinfo.value.code == 7


def test_search_api_remains_available(tmp_path: Path) -> None:
    pack_path = _make_search_pack(tmp_path)
    con = duckdb.connect(str(pack_path), read_only=True)

    try:
        alias_hits = search_aliases(con, "c2c")
        object_hits = search_objects(con, "delivery")
        graph_hits = expand_graph(con, "csu.process.delivery")
    finally:
        con.close()

    assert alias_hits[0]["id"] == "csu.metric.c2c"
    assert object_hits[0]["id"] == "csu.process.delivery"
    assert graph_hits[0]["object"] == "csu.metric.c2c"


def test_pack_searcher_class_wraps_search_functions(tmp_path: Path) -> None:
    pack_path = _make_search_pack(tmp_path)
    con = duckdb.connect(str(pack_path), read_only=True)
    searcher = PackSearcher()

    try:
        hits = searcher.search_aliases(con, "C2C")
    finally:
        con.close()

    assert hits[0]["title"] == "Commit to Complete"


def test_explorer_main_delegates_to_generator(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(ExplorerGenerator, "run", lambda self, argv=None: 3)

    with pytest.raises(SystemExit) as excinfo:
        explorer_main()

    assert excinfo.value.code == 3
