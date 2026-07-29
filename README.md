# Software Engineering Market Intelligence Platform

A backend-first platform for understanding the software-engineering labor market through
normalized job data, analytics, job discovery, and explainable candidate matching.

The project is for engineers exploring market demand, recruiters and hiring managers comparing
role requirements, and contributors building reliable labor-market data products.

> **Status:** Version 2 is under active development. The API, manual job ingestion, deterministic
> enrichment, analytics, and matching workflows run locally. No external job-source connector,
> scheduled ingestion, public web interface, production deployment, or live demo is currently
> verified.

## What works today

- FastAPI endpoints for health, readiness, process-local metrics, jobs, analytics, and matching
- typed manual job upload with separate raw and normalized persistence
- deterministic skill and technology extraction, role and seniority classification, and summaries
- explainable, deterministic candidate-to-job matching
- PostgreSQL persistence with SQLAlchemy and Alembic, plus an in-memory local/test mode
- Docker and Docker Compose development support
- CI checks for Ruff, formatting, mypy, pytest, compileall, and image builds
- an unprovisioned Terraform baseline for an AWS ECS, RDS, ALB, and CloudWatch topology

The API is currently a product foundation, not a complete public market-data product. In
particular, analytics operate only on records submitted to the running instance.

## Project evolution

### Version 1 — Single-source market analysis

The project began as a data science and market-analysis initiative based on job data from
GeekHunter. Its original notebook explored technology demand, job characteristics, salary
disclosure, and software-engineering market patterns. That work remains preserved under
[`notebooks/`](notebooks/) as the historical and analytical foundation of the product.

### Version 2 — Multi-source market intelligence platform

The project is now evolving incrementally into a production-oriented Software Engineering Market
Intelligence Platform. The target product will ingest normalized job data from multiple supported
and authorized sources, then provide market analytics, job discovery, candidate matching, and
future AI-assisted career insights.

Version 2 does not erase Version 1 or claim that its historical scraper is a current connector.
GeekHunter live ingestion is not supported: the preserved parser has no live retrieval
implementation, is not exercised by CI against the site, and must not be operationalized without
written authorization and revalidation.

## Implemented and planned capabilities

| Area | Implemented now | Planned |
| --- | --- | --- |
| Ingestion | Manual API upload; raw and normalized record storage; basic source provenance | Authorized external connectors, scheduling, retries, source health, deduplication, update detection |
| Intelligence | Deterministic enrichment and summaries; aggregate skill/technology analytics | Salary and time-series trends, richer filters, durable analytical views |
| Product | REST API and generated OpenAPI docs; deterministic candidate matching | Public landing page, job explorer, market dashboard, candidate profiles, ranked explanations |
| Operations | Local containers, CI, structured logs, process-local metrics, Terraform baseline | Production deployment, live demo, monitoring, alerting, backups, retention workflows |
| AI | No LLM dependency; deterministic heuristics only | Grounded career insights and natural-language market queries with evaluation and guardrails |

See the evidence-based status in the [roadmap](docs/04-roadmap.md) and the current-versus-target
boundaries in the [architecture](docs/03-architecture.md).

## Run locally

### Docker Compose

```bash
docker compose up --build
```

This starts the API at `http://localhost:8000` and PostgreSQL at `localhost:5432`.
Interactive API documentation is available locally at `http://localhost:8000/docs`.

### Python environment

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
uvicorn apps.api.main:app --host 0.0.0.0 --port 8000 --reload
```

Without `DATABASE_URL`, the application uses in-memory repositories and loses data on restart.
For database-backed local development, use Docker Compose or configure PostgreSQL and run
`alembic upgrade head`.

## Try the current workflow

```bash
curl -X POST http://localhost:8000/v1/jobs:upload \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Backend Engineer",
    "description": "Python, FastAPI, PostgreSQL, AWS, and Docker are required.",
    "source_name": "manual_upload",
    "work_mode": "remote",
    "location_text": "Remote - Brazil"
  }'
```

The stored job then appears in the jobs and analytics endpoints and can participate in candidate
matching. See [API examples](docs/07-api-examples.md) for the complete local workflow.

## API surface

- System: `GET /health`, `/ready`, `/version`, and `/metrics`
- Jobs: `POST /v1/jobs:upload`, `GET /v1/jobs`, and `GET /v1/jobs/{job_id}`
- Analytics: top skills, top technologies, and skill co-occurrence
- Matching: `POST /v1/candidates/matches`

## Documentation

- [Product vision](docs/00-product-vision.md)
- [Product requirements](docs/02-prd.md)
- [Frontend product scope](docs/09-frontend-product-scope.md)
- [Current and target architecture](docs/03-architecture.md)
- [Evidence-based roadmap](docs/04-roadmap.md)
- [Operational runbook](docs/05-operational-runbook.md)
- [Local development](docs/06-local-development.md)
- [Deployment guide](docs/08-deployment-guide.md)
- [Architecture decisions](docs/adr/)

## Quality checks

```bash
ruff check .
ruff format --check .
mypy
pytest
python -m compileall src apps tests alembic
```

## Live demo

There is no verified live deployment or demo URL yet.

Deployment milestone checklist:

- [ ] select and validate an authorized real job source
- [ ] deploy the API and PostgreSQL with production safeguards
- [ ] add a minimal public job explorer and market view
- [ ] configure monitoring, retention, backups, and a rollback path
- [ ] publish and continuously verify the live URL

## Repository layout

```text
apps/         Application entrypoints
docs/         Product, architecture, roadmap, and operational documentation
notebooks/    Preserved Version 1 exploratory assets
src/          Version 2 application package
tests/        Unit and API tests
alembic/      Database migrations
docker/       Container runtime notes
terraform/    Unprovisioned AWS infrastructure baseline
```
