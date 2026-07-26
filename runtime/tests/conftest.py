"""Shared test fixtures and configuration for the AKP Runtime test suite."""

import pytest

from akp_runtime.events.bus import EventBus, RuntimeEvent


@pytest.fixture
def event_bus() -> EventBus:
    """Fresh event bus for each test."""
    return EventBus()


@pytest.fixture
def event_recorder(event_bus: EventBus) -> list[RuntimeEvent]:
    """Records all events emitted to the bus."""
    events: list[RuntimeEvent] = []
    event_bus.subscribe(RuntimeEvent, lambda event: events.append(event))
    return events
