# COM022: Frontend Architecture — Feature-Sliced Design

**Status:** Accepted  
**Capability:** Composer  
**Date:** 2026-07-27

## Context

React applications degrade into unmaintainable god-objects when components mix data fetching, business logic, and presentation. The Composer UI has multiple distinct concerns (source management, extraction monitoring, review queue, graph exploration, release management) that must remain independently developable and testable.

We need an architecture that:
- Prevents cross-concern coupling (review queue doesn't import graph explorer internals)
- Separates presentation from logic (components are testable in isolation)
- Mirrors the backend's Clean Architecture discipline
- Scales to multiple developers working on different features simultaneously
- Keeps each module small and focused (no 500-line components)

## Decision

Adopt **Feature-Sliced Design (FSD)** for the Composer UI.

### Layer Structure

```
composer-ui/src/
│
├── app/                    # Layer 1: App shell (Next.js App Router)
│   ├── layout.tsx          # Root layout, providers, global styles
│   ├── page.tsx            # Landing/dashboard
│   ├── sources/            # Route: /sources
│   ├── review/             # Route: /review
│   ├── graph/              # Route: /graph
│   └── releases/           # Route: /releases
│
├── features/               # Layer 2: Feature modules (business logic units)
│   ├── source-registry/
│   │   ├── ui/             # Feature-specific components
│   │   ├── model/          # Hooks, state, business logic
│   │   ├── api/            # API calls for this feature
│   │   └── index.ts        # Public API (only exports from here)
│   ├── extraction-monitor/
│   │   ├── ui/
│   │   ├── model/
│   │   ├── api/
│   │   └── index.ts
│   ├── review-queue/
│   │   ├── ui/
│   │   ├── model/
│   │   ├── api/
│   │   └── index.ts
│   ├── graph-explorer/
│   │   ├── ui/
│   │   ├── model/
│   │   ├── api/
│   │   └── index.ts
│   └── release-manager/
│       ├── ui/
│       ├── model/
│       ├── api/
│       └── index.ts
│
├── entities/               # Layer 3: Shared domain objects
│   ├── concept/            # Concept type, display components
│   ├── source/             # Source type, status badge
│   ├── proposal/           # Proposal type, evidence display
│   └── relationship/       # Relationship type, edge rendering
│
├── shared/                 # Layer 4: Infrastructure & utilities
│   ├── api/                # Generated API client (from OpenAPI)
│   ├── ui/                 # Design system components (buttons, cards, modals)
│   ├── hooks/              # Generic hooks (useWebSocket, useDebounce)
│   ├── types/              # Generated TypeScript types from FastAPI
│   └── lib/                # Pure utilities (formatting, validation)
│
└── generated/              # Auto-generated from OpenAPI spec
    └── api-types.ts        # TypeScript types matching Pydantic models
```

### Import Rules (ENFORCED)

These are the FSD equivalent of our backend's design gates:

| From ↓ / To → | app | features | entities | shared |
|----------------|-----|----------|----------|--------|
| **app** | — | ✅ | ✅ | ✅ |
| **features** | ❌ | ❌ (no cross-feature) | ✅ | ✅ |
| **entities** | ❌ | ❌ | — | ✅ |
| **shared** | ❌ | ❌ | ❌ | — |

**Key rule:** Features NEVER import from other features. If two features need shared logic, it moves down to `entities/` or `shared/`.

### Feature Module Internal Structure

Each feature follows a mini Clean Architecture internally:

```
features/review-queue/
  ui/                       # Presentation (React components, no logic)
    ReviewList.tsx           # Renders list of proposals
    ReviewCard.tsx           # Single proposal card
    EvidencePanel.tsx        # Evidence display
    DecisionButtons.tsx      # Accept/Reject/Defer actions
  model/                    # Business logic (hooks, state)
    useReviewQueue.ts        # Fetches + manages review items
    useDecision.ts           # Submit decision logic
    reviewFilters.ts         # Filter/sort logic (pure functions)
  api/                      # Server communication
    reviewApi.ts             # REST endpoints for review
    reviewSocket.ts          # WebSocket subscription for live updates
  index.ts                  # Public exports ONLY
```

### Rules Within Features

1. **ui/** components receive data via props — no direct API calls
2. **model/** hooks return data + handlers — no JSX
3. **api/** functions return typed responses — no React
4. **index.ts** exports only the public surface — internal files are private

### Component Size Rule

Mirroring the backend's 200-LOC gate:
- No component file exceeds **150 lines** (including template)
- No hook file exceeds **100 lines** of logic
- If a component grows, extract sub-components or hooks

### Testing Strategy

| Layer | Test Type | Tool |
|-------|-----------|------|
| ui/ | Component render tests | Vitest + Testing Library |
| model/ | Hook logic tests | Vitest + renderHook |
| api/ | Integration tests (mocked API) | Vitest + MSW |
| Full feature | E2E user flows | Playwright |
| Import rules | Lint enforcement | eslint-plugin-boundaries |

### Type Safety Contract

```
FastAPI (Pydantic models)
    → OpenAPI spec (auto-generated)
    → openapi-typescript (code generation)
    → generated/api-types.ts
    → shared/api/ client uses generated types
    → features consume typed responses
```

No manual type definitions for API responses. If the backend changes, regenerate.

## Consequences

1. **Positive:** Features are independently developable, testable, and replaceable
2. **Positive:** Import rules prevent spaghetti coupling
3. **Positive:** Component size limits prevent god-objects
4. **Positive:** Generated types eliminate backend/frontend drift
5. **Negative:** More files/directories than a flat structure (acceptable trade-off)
6. **Negative:** Need lint rule enforcement for import boundaries (eslint-plugin-boundaries)
7. **Negative:** New contributors need to learn FSD conventions

## Enforcement

- **eslint-plugin-boundaries** — enforces import rules at lint time
- **Component size** — custom ESLint rule or PR review gate
- **No cross-feature imports** — lint error, blocks PR
- **Generated types** — CI step verifies types are up-to-date with OpenAPI spec

## Alternatives Considered

- **MVC/MVP** — doesn't map naturally to React's component/hook model
- **Clean Architecture (flat)** — works but doesn't give vertical feature isolation
- **Container/Presenter** — outdated pattern, hooks replaced this
- **No architecture** — leads to god-components and cross-concern spaghetti within weeks
