# Local Development

## Overview

The repository supports two main local workflows:

- Docker Compose for the most complete stack
- direct Python execution for faster iteration

## Option 1: Docker Compose

Start the API and PostgreSQL locally:

```bash
docker compose up --build
```

Services:

- API: `http://localhost:8000`
- PostgreSQL: `localhost:5432`

Behavior:

- the API container runs `alembic upgrade head`
- the development compose file enables reload mode
- source directories are mounted into the API container for iteration

## Option 2: Direct Python Runtime

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

Run the API:

```bash
uvicorn apps.api.main:app --host 0.0.0.0 --port 8000 --reload
```

## Environment Variables

Common variables:

- `APP_NAME`
- `APP_ENV`
- `LOG_LEVEL`
- `API_VERSION`
- `DATABASE_URL`

If `DATABASE_URL` is absent, the API uses in-memory repositories.

## Database Workflow

Run migrations manually:

```bash
alembic upgrade head
```

If you later add migrations:

```bash
alembic revision -m "describe_change"
```

## Testing Workflow

Run tests:

```bash
pytest
```

Static checks:

```bash
ruff check .
mypy
python -m compileall src apps tests alembic
```

## Notebook Workflow

Exploratory assets live in `notebooks/`.

They remain useful for:

- provenance
- exploratory analysis
- comparing production behavior with the original proof of concept

They should not be treated as the application runtime.
