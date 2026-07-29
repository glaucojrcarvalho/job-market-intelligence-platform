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
    assert body["company_name"] is None
    assert body["description"].startswith("We need Python")
    assert body["employment_type"] == "unknown"
    assert body["location"]["raw_text"] == "Remote - Brazil"
    assert body["observed_at"] is not None
    assert body["enrichment"]["role_family"] == "backend_engineering"
    assert "python" in body["enrichment"]["skills"]
    assert body["enrichment"]["summary"] is not None

    job_response = client.get(f"/v1/jobs/{body['job_id']}")
    assert job_response.status_code == 200
    assert job_response.json()["job_id"] == body["job_id"]


def test_list_jobs_supports_bounded_queries_and_public_fields(client: TestClient) -> None:
    jobs = [
        {
            "title": "Synthetic Remote Engineer",
            "description": "Python and PostgreSQL.",
            "source_name": "manual_upload",
            "source_url": "https://example.invalid/jobs/remote-engineer",
            "company_name": "Example Systems",
            "work_mode": "remote",
        },
        {
            "title": "Synthetic Onsite Engineer",
            "description": "Java and AWS.",
            "source_name": "curated_fixture",
            "work_mode": "onsite",
        },
        {
            "title": "Synthetic Platform Engineer",
            "description": "Go and Docker.",
            "source_name": "manual_upload",
            "work_mode": "hybrid",
        },
    ]
    for job in jobs:
        response = client.post("/v1/jobs:upload", json=job)
        assert response.status_code == 201

    response = client.get(
        "/v1/jobs",
        params={
            "source_name": "manual_upload",
            "limit": 1,
            "offset": 1,
        },
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "job_id": 3,
            "title": "Synthetic Platform Engineer",
            "source_name": "manual_upload",
            "work_mode": "hybrid",
            "location_text": None,
            "salary_text": None,
            "company_name": None,
            "source_url": None,
            "posted_at": None,
            "employment_type": "unknown",
        }
    ]

    filtered_response = client.get("/v1/jobs", params={"work_mode": "onsite"})
    assert filtered_response.status_code == 200
    assert [job["title"] for job in filtered_response.json()] == ["Synthetic Onsite Engineer"]


@pytest.mark.parametrize(
    ("params", "field"),
    [
        ({"limit": 0}, "limit"),
        ({"limit": 101}, "limit"),
        ({"offset": -1}, "offset"),
        ({"work_mode": "flexible"}, "work_mode"),
    ],
)
def test_list_jobs_rejects_invalid_query_values(
    client: TestClient,
    params: dict[str, int | str],
    field: str,
) -> None:
    response = client.get("/v1/jobs", params=params)

    assert response.status_code == 422
    assert response.json()["error"] == "validation_error"
    assert any(error["loc"][-1] == field for error in response.json()["details"])


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
