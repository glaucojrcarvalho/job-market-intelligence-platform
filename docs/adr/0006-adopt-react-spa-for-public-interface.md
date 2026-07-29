# ADR 0006: Adopt A Small React SPA For The Public Interface

## Status

Accepted

## Context

The repository currently exposes a FastAPI backend and generated OpenAPI documentation but no
browser product. The first public interface needs four modest workflows: product orientation,
market analytics, job exploration, and request-scoped candidate matching.

The interface must remain maintainable by a small project, support accessible interactive states,
consume the existing JSON API, and run beside the API and PostgreSQL in Docker Compose. The phase
does not require authentication, server-side rendering, a design system, or independent
micro-frontends.

## Decision

Build a client-rendered single-page application using:

- React for component composition and interactive state;
- TypeScript for API and component contracts;
- Vite for development and production builds;
- React Router for the four documented product routes;
- native CSS or CSS Modules for a restrained responsive presentation;
- a small typed API client based on the browser `fetch` API;
- a lightweight charting library only if it provides accessible output without replacing simple
  semantic HTML that would communicate the data better.

Keep state local to pages and focused reusable hooks. Do not add global state management,
authentication, server-side rendering, a UI framework, or a custom design system in this phase.

Configure the API base URL through a Vite environment variable with a documented local default.
Runtime topology, CORS, and Docker Compose integration will be handled after the standalone
frontend works.

## Application boundaries

- FastAPI remains the source of truth for jobs, analytics, matching, and system status.
- The frontend may derive small presentation values, such as total jobs and work-mode counts, from
  current API responses.
- The frontend must not reproduce enrichment or matching business rules.
- API contract changes remain explicit backend work with tests.
- The browser stores no candidate profile beyond transient form and response state.

## Consequences

### Positive

- The selected stack is widely understood and appropriate for the existing interactive workflows.
- TypeScript makes incomplete or changing API contracts visible during development.
- Vite keeps local startup and production builds small and straightforward.
- The SPA can be served as a static artifact and developed independently from FastAPI.
- Minimal dependencies reduce maintenance and supply-chain surface.

### Negative

- Client-side rendering provides limited search-engine rendering compared with SSR.
- A separate JavaScript toolchain and dependency update process are introduced.
- Direct browser-to-API calls require deliberate CORS and environment configuration.
- API response compatibility must be managed across two typed codebases.

## Alternatives considered

### Server-rendered FastAPI templates

Rejected for this phase. Templates would minimize tooling but make the planned interactive
dashboard, partial loading states, and matching workflow less cohesive, while coupling frontend
delivery to the API deployable.

### Next.js or another SSR framework

Rejected. Server rendering, framework routing conventions, and an additional server runtime add
complexity without a validated SEO or authenticated application requirement.

### Large component framework and global state library

Rejected. Four routes and request-local state do not justify the dependency weight or abstraction
surface. Native semantic elements and restrained CSS are sufficient.

### Independent micro-frontends

Rejected. The product scope and team size do not require deployment independence between pages.

## Revisit triggers

Revisit if measured requirements establish a need for server rendering, strong public search
indexing, authenticated sessions, substantial cross-route client state, or independently deployed
frontend domains.
