# COM010: Use Specialist Agents, but a Deterministic Workflow

**Status:** Draft  
**Capability:** Composer  
**Date:** 2026-07-27

## Context

Composer benefits from specialist reasoning roles such as source analyst, claim extractor, concept librarian, ontology steward, contradiction analyst, wiki architect and quality reviewer. Unconstrained autonomous agent loops, however, are hard to resume, test, audit, reproduce, secure, evaluate and explain.

## Decision

Adopt deterministic workflow orchestration that invokes bounded specialist agents for explicit steps such as extract, assess quality, interpret, resolve, validate, request review and commit. Agents may generate proposals within those steps, but domain services and workflow state transitions must remain the only path that applies knowledge changes.

## Consequences

Composer can use targeted agentic reasoning without turning the platform into an opaque super-agent. Workflow checkpoints, validation and review remain auditable, and state changes can be resumed and tested independently of any single model run.
