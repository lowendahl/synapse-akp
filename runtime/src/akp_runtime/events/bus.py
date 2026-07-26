"""Runtime domain events and event bus.

What: Typed domain events raised by runtime lifecycle and tool invocations.
Why: Decoupled observability — components emit events, observers log/react.
Contracts: Events are frozen dataclasses with immutable fields. Bus dispatches by type.
Boundaries: No IO in events; observers handle logging/persistence.
Test strategy: Unit tests verify event emission, type dispatch, and handler isolation.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime

logger = logging.getLogger("akp_runtime.events")


# ─── Base Event ─────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class RuntimeEvent:
    """Base class for all runtime domain events."""

    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


# ─── Lifecycle Events ───────────────────────────────────────────────────────


@dataclass(frozen=True)
class ServerStarting(RuntimeEvent):
    config_source: str = ""


@dataclass(frozen=True)
class PackLoaded(RuntimeEvent):
    pack_id: str = ""
    pack_version: str = ""
    object_count: int = 0


@dataclass(frozen=True)
class ServerReady(RuntimeEvent):
    pack_count: int = 0
    tools_registered: int = 0


# ─── Tool Events ────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class ToolInvoked(RuntimeEvent):
    tool_name: str = ""
    pack_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class ToolCompleted(RuntimeEvent):
    tool_name: str = ""
    result_count: int = 0
    duration_ms: float = 0.0


@dataclass(frozen=True)
class ToolFailed(RuntimeEvent):
    tool_name: str = ""
    error_type: str = ""
    error_message: str = ""


# ─── Shutdown Event ─────────────────────────────────────────────────────────


@dataclass(frozen=True)
class ServerStopping(RuntimeEvent):
    reason: str = "shutdown"


# ─── Event Bus ──────────────────────────────────────────────────────────────

EventHandler = Callable[[RuntimeEvent], None]


class EventBus:
    """Type-based pub/sub event bus for runtime observability.

    Handlers subscribe to specific event types. A handler registered for
    a base type receives events of all subtypes (fallthrough).
    """

    def __init__(self) -> None:
        self._handlers: dict[type[RuntimeEvent], list[EventHandler]] = {}

    def subscribe(
        self,
        event_type: type[RuntimeEvent],
        handler: EventHandler,
    ) -> None:
        """Register a handler for a specific event type."""
        self._handlers.setdefault(event_type, []).append(handler)

    def emit(self, event: RuntimeEvent) -> None:
        """Dispatch event to all matching handlers (exact type + base types)."""
        for cls in type(event).__mro__:
            if cls is object:
                break
            handlers = self._handlers.get(cls, [])  # type: ignore[arg-type]
            for handler in handlers:
                try:
                    handler(event)
                except Exception as exc:
                    logger.warning("Event handler error for %s: %s", type(event).__name__, exc)
