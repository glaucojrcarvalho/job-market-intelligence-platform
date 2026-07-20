# ADR 0004: Start Synchronously With Clear Async Seams

## Status

Accepted

## Context

The MVP needs ingestion and candidate matching, but there is no current queue infrastructure, worker runtime, or operational monitoring stack in the repository.

Adding asynchronous infrastructure immediately would slow delivery and create operational burden before the actual load profile is known.

## Decision

Start with synchronous execution for MVP workflows where response times remain acceptable, while designing service boundaries that can later be moved behind background workers or queue consumers.

Examples:

- API-triggered ingestion can begin synchronously
- enrichment orchestration should be encapsulated in services
- heavy recomputation can later move to async jobs without changing public contracts

## Consequences

### Positive

- simpler implementation path
- easier local development
- fewer moving parts in early phases

### Negative

- long-running imports may eventually outgrow synchronous execution
- some operations may need later refactoring into job-based workflows

## Revisit Trigger

Revisit when ingestion volume, latency, or operational isolation makes synchronous execution unacceptable.
