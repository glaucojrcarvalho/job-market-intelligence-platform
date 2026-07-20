# Operational Runbook

## Purpose

This runbook documents the initial operational response model for the Job Market Intelligence Platform.

It is intentionally lightweight and aligned to the current architecture:

- one FastAPI service
- one PostgreSQL database
- deterministic enrichment pipeline
- optional in-memory mode when `DATABASE_URL` is absent

## Service Inventory

### API Service

- runtime: FastAPI + Uvicorn
- primary concerns: request failures, latency spikes, failed uploads, candidate match degradation

### Database

- runtime: PostgreSQL
- primary concerns: connection failures, migration drift, storage saturation, high query latency

## Key Signals

### Logs

Structured JSON logs now include:

- `timestamp`
- `level`
- `logger`
- `message`
- `request_id`

Use the `request_id` to correlate API failures across request lifecycle log lines.

### Metrics

The application exposes lightweight process metrics at `GET /metrics`:

- total requests
- total errors
- per-route request counts
- per-route error counts
- per-route average latency

### Health Endpoints

- `GET /health`: liveness check
- `GET /ready`: readiness check
- `GET /metrics`: lightweight telemetry snapshot

## Alert Recommendations

Initial alert candidates for a hosted environment:

- API error rate above 5% for 5 minutes
- average latency above 1000 ms on `POST /v1/jobs:upload`
- average latency above 750 ms on `POST /v1/candidates/matches`
- repeated database connection failures
- ECS task restarts above baseline
- RDS free storage or CPU pressure above threshold

## Failure Scenarios

### 1. API Returns 5xx Errors

Check:

- recent structured logs for `request_failed`
- deployment or container restart events
- database connectivity
- recent migration changes

Actions:

- confirm `/health` and `/ready`
- inspect CloudWatch logs or container logs by `request_id`
- roll back the latest deployment if the issue is clearly release-related

### 2. Job Uploads Succeed Slowly Or Fail

Check:

- `/metrics` for upload route latency and error counts
- database performance
- enrichment path regressions

Actions:

- inspect recent enrichment changes
- verify database secret and connectivity
- verify migrations are current

### 3. Candidate Matching Quality Drops

Check:

- recent changes to deterministic taxonomy logic
- enrichment summaries and evidence quality
- unit and regression test results

Actions:

- compare recent outputs against prior known-good examples
- revert the latest AI logic change if quality regressed materially

### 4. Database Connection Failures

Check:

- `DATABASE_URL` secret value
- RDS instance health
- security group rules
- ECS task networking

Actions:

- validate secret value and endpoint
- confirm ECS task role can read Secrets Manager
- confirm RDS security group allows ECS service ingress on `5432`

## Deployment Checklist

Before deploying:

- run tests
- run type checks
- verify Docker image build
- verify migrations are correct
- confirm Terraform changes are reviewed separately

After deploying:

- verify `/health`
- verify `/ready`
- verify `/metrics`
- upload a sample job
- run a sample candidate match request

## Known Limitations

- metrics are in-process and reset on restart
- no distributed tracing backend is configured yet
- no external alert manager is configured yet
- no long-term metrics retention exists inside the app
