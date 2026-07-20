# Job Market Intelligence Platform

Job Market Intelligence Platform is a backend-first system that transforms raw software and data job postings into structured market intelligence.

The platform includes a modular Python package, FastAPI API surface, deterministic enrichment, PostgreSQL persistence, containerization, CI/CD workflows, AWS infrastructure definitions, and observability foundations. An exploratory notebook is retained separately from the application runtime.

## Product Scope

The platform is designed to answer questions such as:

- which skills and technologies are most requested
- which skills appear together
- how requirements differ by seniority
- which jobs best match a candidate profile
- why a candidate is or is not a strong fit

## Current Capabilities

- FastAPI application with health, readiness, metrics, jobs, analytics, and candidate match endpoints
- deterministic job enrichment with skill extraction, technology detection, role-family classification, seniority heuristics, and job summaries
- PostgreSQL-ready persistence with SQLAlchemy and Alembic
- in-memory fallback mode when `DATABASE_URL` is not configured
- Docker and Docker Compose for local runtime
- Terraform baseline for AWS deployment
- GitHub Actions for linting, type checks, tests, and Docker build validation
- structured JSON logging and lightweight in-process metrics

## Repository Layout

```text
apps/         Application entrypoints
docs/         Product, architecture, roadmap, and operational docs
notebooks/    Preserved exploratory notebook assets
src/          Production Python package
tests/        Unit and API tests
alembic/      Database migration scripts
docker/       Container runtime notes
terraform/    AWS infrastructure baseline
```

## Core Documents

- [Product Vision](docs/00-product-vision.md)
- [PRD](docs/02-prd.md)
- [Architecture](docs/03-architecture.md)
- [Roadmap](docs/04-roadmap.md)
- [Operational Runbook](docs/05-operational-runbook.md)

## Local Development

### Option 1: Docker Compose

```bash
docker compose up --build
```

This starts:

- the FastAPI service on `http://localhost:8000`
- PostgreSQL on `localhost:5432`

### Option 2: Python Environment

Create a Python environment and install dependencies:

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

Run the API:

```bash
uvicorn apps.api.main:app --host 0.0.0.0 --port 8000 --reload
```

When running without `DATABASE_URL`, the application uses in-memory repositories.

## API Endpoints

### System

- `GET /health`
- `GET /ready`
- `GET /version`
- `GET /metrics`

### Jobs

- `POST /v1/jobs:upload`
- `GET /v1/jobs`
- `GET /v1/jobs/{job_id}`

### Analytics

- `GET /v1/analytics/skills/top`
- `GET /v1/analytics/technologies/top`
- `GET /v1/analytics/skills/cooccurrence`

### Candidate Matching

- `POST /v1/candidates/matches`

## Example Job Upload

```bash
curl -X POST http://localhost:8000/v1/jobs:upload \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Backend Engineer",
    "description": "We need Python, FastAPI, PostgreSQL and AWS experience. Docker is required.",
    "source_name": "manual_upload",
    "work_mode": "remote",
    "location_text": "Remote - Brazil"
  }'
```

## Example Candidate Match Request

```bash
curl -X POST http://localhost:8000/v1/candidates/matches \
  -H "Content-Type: application/json" \
  -d '{
    "summary": "Python engineer with AWS API experience.",
    "skills": [
      {"name": "python"},
      {"name": "sql"}
    ],
    "location": "Brazil",
    "years_experience": 5
  }'
```

## Testing

Run the Python test suite:

```bash
pytest
```

Additional static checks:

```bash
ruff check .
mypy
python -m compileall src apps tests alembic
```

## Deployment Direction

- application runtime: ECS Fargate
- database: RDS PostgreSQL
- secrets: AWS Secrets Manager
- infrastructure: Terraform
- logs: CloudWatch

See [terraform/README.md](terraform/README.md) for the infrastructure baseline.

## Trade-Offs

- modular monolith over microservices
- deterministic enrichment first, optional LLM integration later
- one source and one backend well-implemented over shallow feature breadth
- in-process metrics now, external metrics platform later

## Known Limitations

- running the full application requires Docker Compose or a local Python environment with PostgreSQL configured
- metrics are process-local and reset on restart
- no tracing backend is configured yet
- current analytics scope is intentionally narrow and API-first
- the exploratory notebook is not part of the production runtime
