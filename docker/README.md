# Docker

## Local Development

Start the API and PostgreSQL locally:

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`.

## Production-Oriented Compose Profile

Run the non-reload variant:

```bash
export POSTGRES_DB=job_market
export POSTGRES_USER=job_market
export POSTGRES_PASSWORD="choose-a-local-password"
export DATABASE_URL="postgresql+psycopg://job_market:${POSTGRES_PASSWORD}@db:5432/job_market"
docker compose -f docker-compose.prod.yml up --build
```

For a hosted environment, provide these values through the deployment platform's secret-management mechanism rather than a committed environment file.

## Notes

- The API container runs `alembic upgrade head` before starting the web server.
- The development compose file mounts `apps/`, `src/`, and `alembic/` for live iteration.
- The production-oriented compose file does not mount source code and does not enable reload mode.
