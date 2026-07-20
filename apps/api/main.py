"""Application entrypoint for local FastAPI execution."""

from job_market.interfaces.api.app import create_app

app = create_app()
