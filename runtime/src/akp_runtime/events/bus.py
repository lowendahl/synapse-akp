"""Runtime event bus engine.

What: Type-based pub/sub dispatcher for runtime domain events.
Why: Decoupled observability — components emit events, observers react.
Boundaries: Bus is pure infrastructure; event types live in contracts/events.py.
"""

from __future__ import annotations

import logging
from collections.abc import Callable

from akp_runtime.contracts.events import RuntimeEvent

logger = logging.getLogger("akp_runtime.events")

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
