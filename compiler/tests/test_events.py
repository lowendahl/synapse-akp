"""Tests for domain event bus (ADR-012, ES-05)."""

from kp_compiler.events.bus import (
    DomainEvent,
    DiscoveryComplete,
    EnrichmentComplete,
    EventBus,
    GraphBuilt,
    LoggingObserver,
    PackWritten,
    ParseComplete,
    ValidationComplete,
)


class TestEventBus:
    """Verify pub/sub mechanics of EventBus."""

    def test_subscribe_and_emit_specific_type(self) -> None:
        bus = EventBus()
        received: list[DomainEvent] = []
        bus.subscribe(DiscoveryComplete, received.append)

        bus.emit(DiscoveryComplete(file_count=42))

        assert len(received) == 1
        assert received[0].file_count == 42

    def test_base_handler_receives_all_events(self) -> None:
        bus = EventBus()
        received: list[DomainEvent] = []
        bus.subscribe(DomainEvent, received.append)

        bus.emit(DiscoveryComplete(file_count=1))
        bus.emit(ParseComplete(object_count=5, error_count=0))

        assert len(received) == 2

    def test_specific_handler_not_called_for_other_types(self) -> None:
        bus = EventBus()
        received: list[DomainEvent] = []
        bus.subscribe(DiscoveryComplete, received.append)

        bus.emit(ParseComplete(object_count=5, error_count=0))

        assert len(received) == 0

    def test_multiple_handlers_for_same_type(self) -> None:
        bus = EventBus()
        a: list[DomainEvent] = []
        b: list[DomainEvent] = []
        bus.subscribe(GraphBuilt, a.append)
        bus.subscribe(GraphBuilt, b.append)

        bus.emit(GraphBuilt(node_count=10, edge_count=5))

        assert len(a) == 1
        assert len(b) == 1

    def test_handler_exception_does_not_crash_bus(self) -> None:
        bus = EventBus()
        received: list[DomainEvent] = []

        def bad_handler(_event: DomainEvent) -> None:
            raise RuntimeError("boom")

        bus.subscribe(PackWritten, bad_handler)
        bus.subscribe(PackWritten, received.append)

        bus.emit(PackWritten(pack_id="test", path="/tmp/x.duckdb"))

        # second handler still called
        assert len(received) == 1

    def test_events_are_frozen(self) -> None:
        event = ValidationComplete(error_count=3, warning_count=7)
        try:
            event.error_count = 99  # type: ignore[misc]
            assert False, "Should not allow mutation"
        except AttributeError:
            pass


class TestLoggingObserver:
    """Verify LoggingObserver subscribes and logs without error."""

    def test_observer_does_not_crash(self) -> None:
        bus = EventBus()
        LoggingObserver(bus)
        bus.emit(EnrichmentComplete(aliases_added=10, acronyms_resolved=5))
        # no assertion needed — verifying no exception
