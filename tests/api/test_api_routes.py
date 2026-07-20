from __future__ import annotations

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("pydantic")
pytest.importorskip("starlette.testclient")

from starlette.testclient import TestClient

from job_market.interfaces.api.app import create_app
from job_market.interfaces.api.dependencies import get_registry


@pytest.fixture
def client():
    app = create_app()
    get_registry.cache_clear()
    with TestClient(app) as test_client:
        yield test_client
    get_registry.cache_clear()


def test_health_endpoint(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_upload_job_and_query_enrichment(client: TestClient) -> None:
    upload_response = client.post(
        "/v1/jobs:upload",
        json={
            "title": "Senior Backend Engineer",
            "description": (
                "We need Python, FastAPI, PostgreSQL and AWS experience. Docker is required."
            ),
            "source_name": "manual_upload",
            "work_mode": "remote",
            "location_text": "Remote - Brazil",
            "salary_text": "10000-15000 USD",
        },
    )

    assert upload_response.status_code == 201
    body = upload_response.json()
    assert body["title"] == "Senior Backend Engineer"
    assert body["enrichment"]["role_family"] == "backend_engineering"
    assert "python" in body["enrichment"]["skills"]
    assert body["enrichment"]["summary"] is not None

    job_response = client.get(f"/v1/jobs/{body['job_id']}")
    assert job_response.status_code == 200
    assert job_response.json()["job_id"] == body["job_id"]


def test_candidate_matches_endpoint(client: TestClient) -> None:
    client.post(
        "/v1/jobs:upload",
        json={
            "title": "Backend Engineer",
            "description": "Python SQL AWS Docker required.",
            "source_name": "manual_upload",
        },
    )

    response = client.post(
        "/v1/candidates/matches",
        json={
            "summary": "Python engineer with AWS API experience.",
            "skills": [{"name": "python"}, {"name": "sql"}],
            "location": "Brazil",
            "years_experience": 5,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["match_score"] == pytest.approx(0.55)
    assert any(reason["type"] == "technology_alignment" for reason in body[0]["reasons"])
