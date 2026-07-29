# ADR 0005: Evolve From A Single-Source Analytics Project To A Multi-Source Market Intelligence Platform

## Status

Accepted

## Context

The project began as a data science and market-analysis notebook using job data from GeekHunter.
It explored a real problem—turning job postings into evidence about technology demand, job
characteristics, and the software-engineering market—and established the product’s analytical
foundation.

The repository now also contains a modular FastAPI application, raw and normalized persistence,
deterministic enrichment and matching, automated tests, container support, CI, and an AWS
infrastructure baseline. Product expectations have also changed: a useful market-intelligence
product needs supported data acquisition, multiple-source extensibility, provenance, reliable
operations, and user-facing discovery workflows.

The current GeekHunter production adapter is not operational: it parses supplied HTML but does not
retrieve live records. GeekHunter’s current terms prohibit automated scraping without prior
written authorization. It therefore cannot be treated as an active V2 source.

## Original project scope

Version 1 used a browser-driven, source-specific notebook flow to collect and analyze GeekHunter
job cards. The notebook, its Portuguese field names, parsing assumptions, and exploratory
dependencies represent historical behavior rather than the production domain contract.

## Decision

Evolve the repository incrementally into a **Software Engineering Market Intelligence Platform**.

- Preserve Version 1 as documented history and analytical provenance.
- Keep the Version 2 backend as a modular monolith.
- Make normalized jobs independent of any source schema.
- Isolate permitted source retrieval, validation, and mapping behind connector boundaries.
- Implement one validated real connector before expanding the generic adapter contract.
- Prefer supported public APIs, feeds, and company-hosted ATS endpoints.
- Treat public job discovery, production deployment, and scheduled acquisition as product work,
  not as already-delivered capabilities.
- Add AI-assisted insights only after grounded data workflows and evaluation exist.

This is an evolution, not a rewrite.

## Preserved assets

- the original exploratory notebook and helpers
- Git history and the documented GeekHunter origin
- the modular monolith and application service boundaries
- raw-versus-normalized storage
- deterministic enrichment, analytics, and matching
- FastAPI, SQLAlchemy, Alembic, Docker, CI, and Terraform foundations

## Deprecated assumptions

- GeekHunter scraping is an operational or permitted production source
- one provider’s HTML or vocabulary can define the canonical job model
- an API and infrastructure definition alone constitute a production product
- every repeated ingestion request may safely create a new canonical job
- candidate match scores are calibrated for high-stakes decisions

“Deprecated” here describes product assumptions, not the deletion of historical artifacts.

## Consequences

### Positive

- the project’s origin remains credible and inspectable
- new sources can be added without leaking provider fields through the system
- supported integration methods reduce legal and operational risk
- public claims distinguish working code from roadmap intent
- delivery can focus on one end-to-end user outcome

### Negative

- the platform cannot yet claim live market coverage
- the existing source port will likely evolve with the first real connector
- provenance and job-lifecycle schema changes remain before scheduled ingestion
- source evaluation and authorization add lead time

## Migration strategy

1. Reposition public documentation and label capability status.
2. Preserve the GeekHunter notebook and parser as unsupported historical artifacts.
3. Evaluate a supported source and document its identifier, update, rate-limit, and retention
   semantics.
4. Evolve the connector contract while implementing that source, with fixture-based contract
   tests.
5. Add the smallest provenance and lifecycle migration required, including compatibility defaults.
6. Add idempotent ingestion, update detection, failure isolation, and observability.
7. Deploy a production-safe vertical slice and add a minimal public interface.
8. Add further connectors only after the first connector is measurable and operable.

## Alternatives considered

### Rewrite the repository around a new distributed architecture

Rejected. The current modular backend is reusable, and a rewrite would obscure the original
history while adding risk without a validated workload.

### Continue treating GeekHunter as the primary production source

Rejected unless written authorization and technical revalidation are obtained. Live fetching is
not implemented, historical selectors are unverified, and current terms restrict scraping.

### Build generic connectors for several providers immediately

Rejected. Empty or speculative adapters would create false capability claims and premature
interfaces.

### Remain a notebook-only analytics project

Rejected as the forward product direction, while preserving the notebook. It cannot provide the
reliable ingestion, API, and user workflows required by Version 2.

## Risks

- supported sources may change contracts, quotas, or commercial terms
- deduplication can create either duplicate jobs or incorrect cross-source merges
- raw job content may carry copyright, retention, and privacy obligations
- candidate data introduces heightened privacy and security requirements
- analytics can mislead when coverage, freshness, and sample bias are not visible
- matching and future AI explanations can appear more authoritative than their evaluation supports

## Revisit triggers

Revisit this decision if source authorization changes, a validated workload requires service
separation, or measured user outcomes show that the proposed public product does not solve the
target problem.
