# COM008: Use Two Separate AI Stages

**Status:** Draft  
**Capability:** Composer  
**Date:** 2026-07-27

## Context

Reading a source and deciding how it should change the OKF are different reasoning problems. A single source-to-wiki generation step mixes evidence discovery with ontology-aware resolution and makes validation, review and debugging much harder.

## Decision

Split AI work into two explicit stages. Stage A, source interpretation, produces evidence-grounded candidate knowledge objects such as concepts, claims, definitions, policies, procedures, metrics, relationships, source purpose, source authority and temporal scope. Stage B, knowledge resolution, compares those candidates to the existing OKF space and proposes actions such as create, extend, merge, alias, contradict, supersede, scope, ignore or escalate for review.

## Consequences

Composer must prohibit direct source-to-published-OKF generation. Each stage gets its own context, validation and evaluation surface, and the handoff between candidate extraction and knowledge change proposal becomes inspectable, reproducible and reviewable.
