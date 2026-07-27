# COM012: Web Acquisition Uses HTTP First, Browser Second

**Status:** Draft  
**Capability:** Composer  
**Date:** 2026-07-27

## Context

Web sources range from simple static pages to authenticated or JavaScript-rendered applications. Composer needs a deterministic default path that captures stable provenance and content fingerprints without incurring browser automation cost for every page.

## Decision

Use HTTPX for primary web retrieval with redirect handling, canonical URL handling, ETag and Last-Modified support, content hashing, response-header capture and raw HTML snapshotting. Use Trafilatura to extract primary content, metadata, links and tables from static HTML, and escalate to Playwright only when JavaScript rendering, authentication, materially different visible DOM, dynamic loading or reader/print generation require a browser path. Store the URL record, HTTP response, raw HTML, rendered DOM when used, screenshots or PDFs when relevant, extracted content, canonical URL and content fingerprint.

## Consequences

Static content follows a cheaper and more reproducible acquisition path, while complex sites remain supported through controlled escalation. Provenance improves because Composer retains both acquisition artifacts and extraction products rather than only the final text.
