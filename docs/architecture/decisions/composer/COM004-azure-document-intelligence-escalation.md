# COM004: Azure Document Intelligence Is an Escalation Tier

**Status:** Draft  
**Capability:** Composer  
**Date:** 2026-07-27

## Context

Some documents, especially scanned PDFs, complex tables, forms and handwritten material, exceed the confidence of local extraction. At the same time, Composer must remain capable of offline, low-cost, provider-independent and restricted-data operation.

## Decision

Use Azure AI Document Intelligence as a policy-controlled escalation tier rather than the default ingestion path. Composer must first attempt local extraction, assess extraction quality, and only route to Azure Document Intelligence when confidence or source characteristics justify escalation; the workflow may then compare or merge local and managed results.

## Consequences

Managed OCR and layout become available for hard cases and enterprise SLA needs without making Azure a mandatory dependency. Routing policy, thresholds and data-governance rules must be explicit, and local extraction must remain a complete supported path for normal and sensitive workloads.
