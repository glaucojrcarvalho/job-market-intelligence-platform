# ADR 0002: Store Raw And Normalized Job Data Separately

## Status

Accepted

## Context

The current notebook extracts a small set of fields directly from scraped HTML and immediately analyzes them in-memory. That approach loses provenance and makes it difficult to debug parsing quality, re-run normalization, or compare source changes over time.

## Decision

Persist raw job records separately from normalized job entities.

Use:

- raw payload storage for source provenance
- normalized relational tables for canonical queryable records
- foreign-key linkage between raw and normalized records

## Consequences

### Positive

- easier parser debugging
- easier reprocessing when normalization rules improve
- traceability from API output back to source payload
- safer support for multiple ingestion sources

### Negative

- more storage usage
- more schema complexity than a single flattened jobs table

## Revisit Trigger

Revisit only if a later data-platform architecture introduces a more specialized raw-data lake or archival strategy.
