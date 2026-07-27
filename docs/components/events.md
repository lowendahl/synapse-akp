# Component: Events

## Purpose
The events component provides the observability backbone for Synapse AKP. It defines immutable event payloads and synchronous pub/sub buses so compiler and runtime flows can publish lifecycle, stage, and tool execution signals without hard-coupling publishers to loggers or monitoring observers.

## Modules Covered
- `kp_compiler.events.__init__` — compiler events package marker
- `kp_compiler.events.bus` — compiler event types, event bus, and logging observer
- `akp_runtime.contracts.events` — runtime event type contracts
- `akp_runtime.events.__init__` — runtime events package marker and re-export surface
- `akp_runtime.events.bus` — runtime event bus engine

## Responsibilities
- Define immutable lifecycle and stage/tool event payloads
- Dispatch events synchronously to registered handlers by type
- Support base-type subscriptions for broad observability hooks
- Shield publishers from observer failures by logging or warning instead of propagating handler exceptions

## Out of Scope
- Persisting telemetry
- Starting transports or servers
- Business logic decisions based on events
- Cross-process event delivery

## Promises
- **P-EVENT-001**: Compiler event handlers subscribed to `DomainEvent` receive all compiler event subtypes.
- **P-EVENT-002**: Runtime event handlers subscribed to a base class receive subtype events through MRO traversal.
- **P-EVENT-003**: Event timestamps are assigned at event creation time.
- **P-EVENT-004**: Observer failures do not prevent subsequent handlers from running.

## Invariants
- **INV-EVENT-001**: Event payloads are data-only contracts and do not perform IO.
- **INV-EVENT-002**: Event buses dispatch by event type rather than by string topic names.
- **INV-EVENT-003**: Observability remains optional; publishers can emit without knowing subscriber implementations.

## Dependencies
- Standard library dataclasses, datetime, logging, and callable typing

## Dependents
- `kp_compiler.pipeline.compiler`
- `akp_runtime.pipeline.bootstrap`
- Logging and monitoring observers
