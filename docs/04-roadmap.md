# Roadmap

This roadmap tracks product and operational outcomes that are not part of the current release. Priorities may change as ingestion volume, data quality, and user feedback become measurable.

## Data Acquisition

- Add scheduled ingestion with bounded retries and idempotent execution.
- Evaluate additional sources for data quality, stability, and permitted use.
- Add source-health reporting and parser regression fixtures.

## Intelligence Quality

- Expand the controlled skill and technology taxonomy.
- Establish labeled evaluation datasets for extraction and classification.
- Calibrate candidate-match scores and confidence values.
- Add trend analysis across time, region, role family, and seniority.

## API And Product Delivery

- Add filtering and pagination consistently across collection endpoints.
- Define data-retention and candidate-profile deletion workflows.
- Evaluate semantic search after relevance and evaluation criteria are defined.

## Reliability And Operations

- Move long-running ingestion behind queue-backed workers when volume requires it.
- Replace process-local metrics with a durable telemetry backend.
- Add alerting, distributed tracing, and service-level objectives.
- Add backup, restore, disaster-recovery, and secret-rotation procedures.

## Infrastructure

- Introduce remote Terraform state with locking and recovery documentation.
- Separate development, staging, and production environments.
- Add deployment rollback or blue/green support.
- Review capacity, cost controls, network boundaries, and least-privilege IAM.

## Delivery Principles

- Prioritize measurable product outcomes and operational risks.
- Keep changes reviewable and maintainable.
- Prefer deterministic behavior until an alternative demonstrates better measured quality.
- Record material architectural changes in ADRs.
