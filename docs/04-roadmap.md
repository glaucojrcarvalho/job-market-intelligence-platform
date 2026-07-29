# Product Roadmap

Status labels reflect repository evidence as of July 29, 2026:

- **Completed** — implemented and covered by the repository
- **In progress** — a usable foundation exists, but the product outcome is incomplete
- **Planned** — no operational implementation is claimed

## Phase 1 — Historical foundation

- **Completed:** single-source GeekHunter exploratory analysis
- **Completed:** original notebook and analysis helpers preserved as historical assets
- **Completed:** initial parsing and data-analysis workflow

## Phase 2 — Product foundation

- **Completed:** modular FastAPI backend and generated OpenAPI contract
- **Completed:** manual ingestion with separate raw and normalized persistence
- **Completed:** deterministic enrichment, API analytics, and request-scoped candidate matching
- **Completed:** PostgreSQL models, initial Alembic migration, automated tests, Docker, and CI
- **In progress:** normalized multi-source domain model and minimal `SourceAdapter` seam
- **Planned:** one authorized, operational external connector
- **Planned:** connector validation, deterministic deduplication, and update detection
- **Planned:** scheduled ingestion with bounded retries and rate-limit handling
- **Planned:** ingestion health, stale-job lifecycle, retention, and replay workflows

## Phase 3 — Public product

- **In progress:** AWS Terraform deployment baseline
- **Planned:** hardened production deployment and verified demo URL
- **Planned:** public landing page and minimal job explorer
- **Planned:** market dashboard with skill, technology, salary, location, and time trends
- **Planned:** filtering, pagination, and complete public API documentation
- **Planned:** durable monitoring, alerting, tracing, backups, and rollback

## Phase 4 — Personalized intelligence

- **In progress:** deterministic request-scoped job matching with matched and missing skill reasons
- **Planned:** user accounts and persisted candidate profiles with deletion controls
- **Planned:** ranked job discovery and calibrated matching
- **Planned:** skill-gap explanations and evidence-backed recommendations
- **Planned:** evaluation datasets and quality metrics for matching

## Phase 5 — Applied AI

- **Planned:** natural-language market queries grounded in normalized data
- **Planned:** AI-assisted career insights and explanation generation
- **Planned:** model/provider controls, evaluation, monitoring, cost limits, and safety guardrails

## Next product milestone

Deliver one public vertical slice:

1. select a supported real source with documented integration permission
2. implement its connector, provenance, idempotency, update, and expiration semantics
3. deploy the existing backend with production safeguards
4. add a minimal public job explorer and market summary
5. publish a monitored, working demo URL

This milestone takes priority over adding more speculative connectors or another broad internal
refactor.
