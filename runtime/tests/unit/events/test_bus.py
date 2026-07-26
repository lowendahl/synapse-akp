"""Tests for runtime event bus behavior and event immutability."""

from __future__ import annotations

import logging
from dataclasses import FrozenInstanceError

import pytest

from akp_runtime.contracts.events import (
    PackLoaded,
    RuntimeEvent,
    ServerReady,
    ServerStopping,
    ToolCompleted,
    ToolInvoked,
)
from akp_runtime.events.bus import EventBus


# Invariant: subscribing to a concrete event type only receives that event subtype.
def test_subscribe_by_type_receives_only_matching_events(event_bus: EventBus) -> None:
    seen: list[PackLoaded] = []
    pack_event = PackLoaded(pack_id="test.domain.pack", pack_version="1.0.0", object_count=10)

    event_bus.subscribe(PackLoaded, seen.append)
    event_bus.emit(pack_event)
    event_bus.emit(ServerReady(pack_count=1, tools_registered=4))

    assert seen == [pack_event]


# Invariant: subscribing to RuntimeEvent receives all event subtypes.
def test_subscribe_to_runtime_event_receives_all_subtypes(
    event_bus: EventBus,
    event_recorder: list[RuntimeEvent],
) -> None:
    pack_event = PackLoaded(pack_id="test.domain.pack", pack_version="1.0.0", object_count=10)
    tool_event = ToolCompleted(tool_name="akp_search", result_count=3, duration_ms=5.0)

    event_bus.emit(pack_event)
    event_bus.emit(tool_event)

    assert event_recorder == [pack_event, tool_event]


# Invariant: one failing handler is isolated and must not block later handlers.
def test_handler_exceptions_are_logged_and_do_not_block_other_handlers(
    event_bus: EventBus,
    caplog: pytest.LogCaptureFixture,
) -> None:
    received: list[str] = []

    def broken_handler(event: RuntimeEvent) -> None:
        _ = event
        raise RuntimeError("boom")

    def healthy_handler(event: RuntimeEvent) -> None:
        received.append(type(event).__name__)

    caplog.set_level(logging.WARNING, logger="akp_runtime.events")
    event_bus.subscribe(ToolCompleted, broken_handler)
    event_bus.subscribe(ToolCompleted, healthy_handler)

    event_bus.emit(ToolCompleted(tool_name="akp_search", result_count=1, duration_ms=1.5))

    assert received == ["ToolCompleted"]
    assert "Event handler error for ToolCompleted: boom" in caplog.text


# Invariant: runtime events are frozen value objects.
@pytest.mark.parametrize(
    ("event", "attribute", "value"),
    (
        (PackLoaded(pack_id="pack", pack_version="1.0.0", object_count=1), "pack_id", "other"),
        (ServerReady(pack_count=1, tools_registered=4), "pack_count", 2),
        (ToolInvoked(tool_name="akp_search", pack_ids=("pack",)), "tool_name", "other"),
    ),
)
def test_events_are_frozen(event: RuntimeEvent, attribute: str, value: object) -> None:
    with pytest.raises(FrozenInstanceError):
        setattr(event, attribute, value)


# Invariant: ToolInvoked.pack_ids is an immutable tuple payload.
def test_tool_invoked_pack_ids_is_tuple_immutable() -> None:
    event = ToolInvoked(tool_name="akp_search", pack_ids=("pack-a", "pack-b"))

    assert isinstance(event.pack_ids, tuple)
    with pytest.raises(AttributeError):
        event.pack_ids.append("pack-c")


# Invariant: handlers for the same event type run in subscription order.
def test_event_handler_order_matches_subscription_order(event_bus: EventBus) -> None:
    order: list[str] = []

    event_bus.subscribe(PackLoaded, lambda event: order.append(f"first:{event.pack_id}"))
    event_bus.subscribe(PackLoaded, lambda event: order.append(f"second:{event.pack_id}"))
    event_bus.subscribe(PackLoaded, lambda event: order.append(f"third:{event.pack_id}"))

    event_bus.emit(PackLoaded(pack_id="test.domain.pack", pack_version="1.0.0", object_count=10))

    assert order == [
        "first:test.domain.pack",
        "second:test.domain.pack",
        "third:test.domain.pack",
    ]


# Invariant: emitting on an empty bus is always a no-op and never crashes.
def test_empty_bus_emit_is_noop() -> None:
    EventBus().emit(ServerStopping(reason="tests-complete"))
