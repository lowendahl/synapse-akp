# COM011: Start with an Explicit Persistent State Machine; Introduce Temporal When Required

**Status:** Draft  
**Capability:** Composer  
**Date:** 2026-07-27

## Context

Composer workflows must survive retries, human review and long-running external work, but the local MVP should not require heavyweight enterprise orchestration. The design must therefore start durable and evolvable without assuming Temporal from day one.

## Decision

Model composition as an explicit persistent state machine from the start, built initially from Python application services, persistent job and step records, idempotent activities, explicit workflow states, retry policies, review gates and append-only events. Use DuckDB or SQLite-backed workflow state locally, and design activity boundaries so they can later map cleanly to Temporal activities when workloads become long-running, high-fan-out or crash-resilient at enterprise scale.

## Consequences

The MVP stays simple while preserving a durable workflow contract. Composer gains resumability and auditability immediately, and a future Temporal migration becomes an implementation upgrade rather than a conceptual redesign of the workflow model.
