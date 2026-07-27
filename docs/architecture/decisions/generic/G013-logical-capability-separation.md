# ADR-020: Logical Capabilities SHALL Be Separated from Implementations

**Status:** Accepted
**Date:** 2026-07-26
**Context:** A package may describe capabilities that different deployments satisfy through different concrete systems. Embedding environment-specific endpoints in the package would destroy portability.
**Decision:** AKP SHALL describe logical capabilities and bindings using stable logical identifiers. Environment-specific endpoints, credentials, and concrete implementations SHALL be resolved at deployment time rather than encoded into the package contract.
**Consequences:** The same package can be deployed across regions and platforms, capability mappings move into runtime configuration, and packages avoid secrets and hard-coded infrastructure dependencies.
**References:** AKP Product Definition §8.8, §15.6, §30
