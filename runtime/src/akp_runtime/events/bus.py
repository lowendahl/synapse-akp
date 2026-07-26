"""Runtime domain events and event bus.

Mirrors the compiler's event bus pattern for runtime observability.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable

logger = logging.getLogger("akp_runtime.events")


@dataclass(frozen=True)
class RuntimeEvent:
    """Base class for all runtime domain events."""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


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


@dataclass(frozen=True)
class ToolInvoked(RuntimeEvent):
    tool_name: str = ""
    pack_ids: list[str] = field(default_factory=list)


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


@dataclass(frozen=True)
class ServerStopping(RuntimeEvent):
    reason: str = "shutdown"


EventHandler = Callable[[RuntimeEvent], None]


class EventBus:
    """Simple pub/sub event bus for runtime observability."""

    def __init__(self) -> None:
        self._handlers: list[EventHandler] = []

    def subscribe(self, handler: EventHandler) -> None:
        self._handlers.append(handler)

    def emit(self, event: RuntimeEvent) -> None:
        for handler in self._handlers:
            try:
                handler(event)
            except Exception as exc:
                logger.warning("Event handler error: %s", exc)
