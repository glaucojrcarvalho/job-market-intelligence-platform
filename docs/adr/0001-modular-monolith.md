# ADR 0001: Adopt A Modular Monolith For The MVP

## Status

Accepted

## Context

The project is evolving from a single notebook into a backend platform. The domain is still being shaped, the implementation team is small, and the MVP requires fast iteration across ingestion, normalization, enrichment, analytics, and candidate matching.

Microservices would add:

- distributed deployment complexity
- more CI/CD overhead
- networked failure modes
- harder local development
- premature service boundaries

## Decision

Build the MVP as a modular monolith with:

- one FastAPI deployable
- clear internal modules
- repository and provider interfaces
- infrastructure dependencies isolated from domain logic

## Consequences

### Positive

- faster implementation
- simpler testing
- easier refactoring while the domain is still evolving
- lower operational complexity

### Negative

- less independent scaling by subsystem
- code discipline is required to keep module boundaries healthy

## Revisit Trigger

Revisit if ingestion volume, team size, or deployment independence requirements justify splitting bounded contexts into separate services.
