# COM021: UI Technology Stack

**Status:** Accepted  
**Capability:** Composer  
**Date:** 2026-07-27

## Context

Synapse Composer requires a rich user interface for source management, extraction monitoring, knowledge graph exploration, review queue interaction, and release management. The backend (FastAPI + Python) is established. The UI must support:

- Review queue with evidence display, diffs, and approve/reject actions
- Knowledge graph visualization (concepts, relationships, conflicts)
- Source registration and extraction progress monitoring
- Release history and compilation status

The project is open-source under `lowendahl/synapse-akp` (not official Microsoft). The architecture must support a single contributor or small team maintaining both backend and frontend.

## Decision

### Frontend Stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| Framework | **Next.js** | File-based routing, SSR-capable (future), strong ecosystem |
| Language | **TypeScript** | Type safety matching Pydantic contracts; shared type generation |
| Styling | **Tailwind CSS** | Utility-first, fast iteration, no component lock-in |
| Graph Viz | **React Flow** | Node-based diagrams, ideal for knowledge graph exploration |
| State | **TanStack Query** | Server state management, cache invalidation, WebSocket support |
| Forms | **React Hook Form** | Performant forms for review queue actions |

### Repository Structure

Monorepo within `synapse-akp`:

```
synapse-akp/
  compiler/          # Existing — AK Compiler (Python)
  runtime/           # Existing — AKP Runtime + MCP (Python)
  composer/          # NEW — Composer backend (Python/FastAPI)
  composer-ui/       # NEW — Composer frontend (Next.js/TypeScript)
    src/
      app/           # Next.js App Router pages
      components/    # React components
      lib/           # API client, types, utilities
      hooks/         # Custom React hooks
    package.json
    tsconfig.json
    tailwind.config.ts
    next.config.ts
```

### API Contract

- FastAPI backend generates OpenAPI spec
- `openapi-typescript` generates TypeScript types from OpenAPI
- Shared types ensure frontend and backend stay in sync
- WebSocket for real-time extraction progress and review notifications

### Communication Pattern

```
Browser (Next.js SPA)
    ↕ REST (CRUD, queries)
    ↕ WebSocket (progress, notifications, live updates)
FastAPI Backend
    ↕ Domain logic
DuckDB + Git OKF
```

### Development Workflow

```bash
# Backend
cd composer && pip install -e ".[dev]" && uvicorn synapse_composer.api:app --reload

# Frontend
cd composer-ui && npm install && npm run dev

# Type generation (after API changes)
cd composer-ui && npm run generate-types
```

### Deployment

- **Local**: `npm run build` produces static export, served by FastAPI or standalone
- **Production**: Next.js build + FastAPI behind reverse proxy
- **Single binary** (future): Bundle frontend static assets into Python package

## Consequences

- Two language ecosystems in one repo (Python + TypeScript/Node)
- Need CI for both (pytest + vitest/playwright)
- Type generation keeps contracts synchronized
- React Flow provides immediate graph visualization without custom D3 work
- Next.js App Router gives future SSR option if needed for SEO/sharing
- Tailwind avoids component library lock-in while maintaining design consistency

## Alternatives Considered

- **CLI + HTMX** — simpler but insufficient for graph viz and rich review UX
- **Tauri** — native feel but adds Rust toolchain, three languages
- **VS Code extension** — locks to one editor, harder to demo
- **Vite + React** — lighter but loses Next.js routing conventions and SSR option
