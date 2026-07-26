"""Domain events and event bus for pipeline observability (ES-05, ADR-012).

What: Typed domain events raised by each pipeline stage.
Why: Decoupled observability — stages emit events, observers log/react.
Contracts: Events are frozen dataclasses. Bus is a simple pub/sub.
Boundaries: No IO in events; observers handle logging/persistence.
Test strategy: Unit tests verify event emission and observer invocation.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable

logger = logging.getLogger("kp_compiler.events")


# ─── Base Event ─────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class DomainEvent:
    """Base class for all domain events."""

    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


# ─── Pipeline Events ───────────────────────────────────────────────────────


@dataclass(frozen=True)
class DiscoveryComplete(DomainEvent):
    file_count: int = 0


@dataclass(frozen=True)
class ObjectParsed(DomainEvent):
    object_id: str = ""
    source_file: str = ""
    object_type: str = ""


@dataclass(frozen=True)
class ParseComplete(DomainEvent):
    object_count: int = 0
    error_count: int = 0


@dataclass(frozen=True)
class ValidationComplete(DomainEvent):
    error_count: int = 0
    warning_count: int = 0


@dataclass(frozen=True)
class EnrichmentComplete(DomainEvent):
    aliases_added: int = 0
    entities_found: int = 0
    acronyms_resolved: int = 0


@dataclass(frozen=True)
class GraphBuilt(DomainEvent):
    node_count: int = 0
    edge_count: int = 0
    orphan_count: int = 0
    cycle_count: int = 0


@dataclass(frozen=True)
class BM25IndexBuilt(DomainEvent):
    unit_count: int = 0
    vocab_size: int = 0


@dataclass(frozen=True)
class EmbeddingComplete(DomainEvent):
    unit_count: int = 0
    model_name: str = ""
    dimensions: int = 0
    duration_seconds: float = 0.0


@dataclass(frozen=True)
class CrossPackValidationComplete(DomainEvent):
    refs_checked: int = 0
    refs_resolved: int = 0
    refs_broken: int = 0


@dataclass(frozen=True)
class PackWritten(DomainEvent):
    pack_id: str = ""
    path: str = ""
    content_hash: str = ""
    duration_seconds: float = 0.0


# ─── Event Bus ──────────────────────────────────────────────────────────────


class EventBus:
    """Simple synchronous pub/sub event bus.

    Stages call bus.emit(event). Observers subscribe by event type.
    """

    def __init__(self) -> None:
        self._handlers: dict[type, list[Callable[[Any], None]]] = {}

    def subscribe(self, event_type: type, handler: Callable[[Any], None]) -> None:
        """Register a handler for an event type."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def emit(self, event: DomainEvent) -> None:
        """Emit an event to all registered handlers."""
        event_type = type(event)
        for handler in self._handlers.get(event_type, []):
            try:
                handler(event)
            except Exception:
                logger.exception("Event handler failed for %s", event_type.__name__)

        # Also notify handlers subscribed to the base DomainEvent
        if event_type is not DomainEvent:
            for handler in self._handlers.get(DomainEvent, []):
                try:
                    handler(event)
                except Exception:
                    logger.exception("Base handler failed for %s", event_type.__name__)


class LoggingObserver:
    """Default observer that logs all domain events."""

    def __init__(self, bus: EventBus) -> None:
        bus.subscribe(DomainEvent, self._on_event)

    def _on_event(self, event: DomainEvent) -> None:
        event_name = type(event).__name__
        # Build a compact log line from event fields
        fields = {k: v for k, v in event.__dict__.items() if k != "timestamp"}
        field_str = ", ".join(f"{k}={v}" for k, v in fields.items())
        logger.info("[event] %s: %s", event_name, field_str)
