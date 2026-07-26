# ADR-022: The Package Graph SHALL Be Portable

**Status:** Accepted
**Date:** 2026-07-26
**Context:** Knowledge graphs are central to relationship navigation and reasoning, but binding the package graph to one graph database would reduce portability and complicate local and offline use.
**Decision:** The package graph SHALL use a portable representation that can be loaded into multiple supported graph engines or in-memory libraries. AKP SHALL NOT require Neo4j or any single graph product as part of the package contract.
**Consequences:** Packages can be consumed by local tools and enterprise runtimes alike, graph engine choice moves to implementation time, and graph serialization must remain interoperable rather than vendor-specific.
**References:** AKP Product Definition §15.3, §35
