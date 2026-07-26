"""Composition root — instantiates all adapters and wires the runtime.

What: Creates and owns the full runtime lifecycle (startup → serve → shutdown).
Why: Single ownership point guarantees resource cleanup on all exit paths.
Contracts: RuntimeContext is an async context manager; resources released in finally.
Boundaries: Only module that composes infrastructure + operations + consumer layers.
Test strategy: Integration tests verify startup, tool availability, and clean shutdown.
"""

from __future__ import annotations

import signal
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

from akp_runtime.contracts.events import ServerStarting, ServerStopping
from akp_runtime.events.bus import EventBus


class RuntimeContext:
    """Owns the runtime lifecycle and guarantees resource cleanup.

    Usage:
        with RuntimeContext(config_path) as ctx:
            ctx.serve()  # blocks on MCP stdio
    """

    def __init__(self, config_path: Path | None = None) -> None:
        self._config_path = config_path
        self._bus = EventBus()
        self._closed = False

    def __enter__(self) -> RuntimeContext:
        """Bootstrap: load config, open packs, register tools, install signal handlers."""
        self._bus.emit(ServerStarting(config_source=str(self._config_path or "auto")))
        self._install_signal_handlers()
        # PBI #11: full bootstrap logic
        return self

    def __exit__(self, exc_type: type | None, exc_val: BaseException | None, exc_tb: object) -> None:
        """Guaranteed cleanup: close packs, vector indexes, and emit shutdown event."""
        if not self._closed:
            self._shutdown()

    def serve(self) -> None:
        """Run MCP stdio server (blocks until client disconnects)."""
        raise NotImplementedError("PBI #11")

    def _shutdown(self) -> None:
        """Release all resources in reverse-init order."""
        self._closed = True
        self._bus.emit(ServerStopping(reason="shutdown"))
        # PBI #11: close vector indexes, DuckDB connections, embedder

    def _install_signal_handlers(self) -> None:
        """Register SIGTERM/SIGINT handlers for graceful shutdown."""
        for sig in (signal.SIGTERM, signal.SIGINT):
            signal.signal(sig, self._signal_handler)

    def _signal_handler(self, signum: int, frame: object) -> None:
        """Handle termination signals gracefully."""
        if not self._closed:
            self._shutdown()
        raise SystemExit(0)


@contextmanager
def runtime_context(config_path: Path | None = None) -> Generator[RuntimeContext, None, None]:
    """Convenience context manager for the runtime lifecycle."""
    ctx = RuntimeContext(config_path)
    with ctx:
        yield ctx


def bootstrap_runtime(config_path: Path | None = None) -> None:
    """Bootstrap the runtime: load config, open packs, register MCP tools, serve."""
    with RuntimeContext(config_path) as ctx:
        ctx.serve()
