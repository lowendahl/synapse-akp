# ADR-015: AKP SHALL Remain Runtime-Neutral

**Status:** Accepted
**Date:** 2026-07-26
**Context:** AKP packages must be usable by local tools, embedded runtimes, service-hosted runtimes, and future Synapse deployments without encoding one execution stack, graph engine, or serving topology into the package contract.
**Decision:** AKP SHALL expose a runtime-neutral package and retrieval contract. Implementations MAY optimize loading and execution for a given environment, but published packages SHALL NOT require a specific runtime, agent framework, graph engine, or deployment topology.
**Consequences:** Packages remain portable across environments, runtime adapters can evolve independently, and deployment-specific optimizations must remain behind stable interfaces rather than leaking into the public contract.
**References:** AKP Product Definition §26, §27, §35
