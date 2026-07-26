"""Runtime domain event contracts.

What: Frozen dataclass event types forming the contract between publishers and subscribers.
Why: Events are the communication protocol for decoupled observability.
Boundaries: No IO, no logic — pure data contracts only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

# ─── Base Event ─────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class RuntimeEvent:
    """Base class for all runtime domain events."""

    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


# ─── Lifecycle Events ───────────────────────────────────────────────────────


@dataclass(frozen=True)
class ServerStarting(RuntimeEvent):
    """Emitted when the runtime begins initialization."""

    config_source: str = ""


@dataclass(frozen=True)
class PackLoaded(RuntimeEvent):
    """Emitted when a knowledge pack is successfully loaded."""

    pack_id: str = ""
    pack_version: str = ""
    object_count: int = 0


@dataclass(frozen=True)
class ServerReady(RuntimeEvent):
    """Emitted when the runtime is fully initialized and ready to serve."""

    pack_count: int = 0
    tools_registered: int = 0


# ─── Tool Events ────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class ToolInvoked(RuntimeEvent):
    """Emitted when a tool execution begins."""

    tool_name: str = ""
    pack_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class ToolCompleted(RuntimeEvent):
    """Emitted when a tool execution succeeds."""

    tool_name: str = ""
    result_count: int = 0
    duration_ms: float = 0.0


@dataclass(frozen=True)
class ToolFailed(RuntimeEvent):
    """Emitted when a tool execution fails."""

    tool_name: str = ""
    error_type: str = ""
    error_message: str = ""


# ─── Shutdown Event ─────────────────────────────────────────────────────────


@dataclass(frozen=True)
class ServerStopping(RuntimeEvent):
    """Emitted when the runtime begins shutdown."""

    reason: str = "shutdown"
