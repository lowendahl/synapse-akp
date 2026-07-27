"""Tests for runtime entry-point wrappers."""

from __future__ import annotations

import pytest

from akp_runtime import __main__ as runtime_main
from akp_runtime.consumer import mcp_server


def test_runtime_main_delegates_to_application(monkeypatch: pytest.MonkeyPatch) -> None:
    called: list[str] = []
    monkeypatch.setattr(runtime_main.Application, "run", lambda self: called.append("runtime"))

    runtime_main.main()

    assert called == ["runtime"]


def test_mcp_server_main_delegates_to_application(monkeypatch: pytest.MonkeyPatch) -> None:
    called: list[str] = []
    monkeypatch.setattr(mcp_server.McpServerApplication, "run", lambda self: called.append("mcp"))

    mcp_server.main()

    assert called == ["mcp"]


def test_mcp_server_creates_fastmcp_instance() -> None:
    """The _create_server function produces a configured FastMCP instance."""
    server = mcp_server._create_server(config_path=None)
    assert server is not None
    assert server.name == "akp-runtime"
