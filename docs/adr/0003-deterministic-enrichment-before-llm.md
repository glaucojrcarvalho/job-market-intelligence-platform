# ADR 0003: Prefer Deterministic Enrichment Before LLM Features

## Status

Accepted

## Context

The product needs skill extraction, classification, and candidate matching, but the repository currently has no evaluation framework, no provider abstraction, and no production controls around AI usage.

An LLM-first architecture would increase:

- cost
- latency
- operational complexity
- explainability risk
- vendor dependence

## Decision

Implement the initial enrichment pipeline using deterministic techniques first:

- controlled vocabularies
- token and regex matching
- heuristic classification
- canonical normalization tables

LLM usage is allowed later only behind explicit provider interfaces and only where it adds clear value, such as summarization or higher-quality explanation generation.

## Consequences

### Positive

- easier testing
- lower cost
- better reproducibility
- better explanation of extracted facts

### Negative

- some edge cases may have lower recall than a strong LLM pipeline
- taxonomy maintenance becomes important

## Revisit Trigger

Revisit when deterministic extraction quality is measured and found insufficient for specific product outcomes.
