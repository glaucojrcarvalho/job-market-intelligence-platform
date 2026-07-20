"""FastAPI route definitions."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request, status

from job_market.domain.analytics.models import MetricBucket, SkillCooccurrence
from job_market.interfaces.api.dependencies import ServiceRegistry, get_registry, get_version
from job_market.interfaces.schemas.analytics import (
    MetricBucketResponse,
    SkillCooccurrenceResponse,
)
from job_market.interfaces.schemas.candidates import CandidateProfileRequest
from job_market.interfaces.schemas.jobs import (
    JobResponse,
    JobWithEnrichmentResponse,
    ManualJobUploadRequest,
)
from job_market.interfaces.schemas.matches import MatchResult
from job_market.interfaces.schemas.system import (
    HealthResponse,
    MetricsResponse,
    ReadinessResponse,
    VersionResponse,
)

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/ready", response_model=ReadinessResponse, tags=["system"])
def ready(registry: ServiceRegistry = Depends(get_registry)) -> ReadinessResponse:
    return ReadinessResponse(
        status="ok",
        checks={
            "repositories": "ok",
            "environment": registry.settings.environment,
        },
    )


@router.get("/version", response_model=VersionResponse, tags=["system"])
def version(registry: ServiceRegistry = Depends(get_registry)) -> VersionResponse:
    return VersionResponse(
        app_name=registry.settings.app_name,
        version=get_version(),
        environment=registry.settings.environment,
    )


@router.get("/metrics", response_model=MetricsResponse, tags=["system"])
def metrics(request: Request) -> MetricsResponse:
    return MetricsResponse(**request.app.state.metrics.snapshot())


@router.post(
    "/v1/jobs:upload",
    response_model=JobWithEnrichmentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["jobs"],
)
def upload_job(
    request: ManualJobUploadRequest,
    registry: ServiceRegistry = Depends(get_registry),
) -> JobWithEnrichmentResponse:
    return registry.upload_job(request)


@router.get("/v1/jobs", response_model=list[JobResponse], tags=["jobs"])
def list_jobs(registry: ServiceRegistry = Depends(get_registry)) -> list[JobResponse]:
    return registry.list_jobs()


@router.get("/v1/jobs/{job_id}", response_model=JobWithEnrichmentResponse, tags=["jobs"])
def get_job(job_id: int, registry: ServiceRegistry = Depends(get_registry)) -> JobWithEnrichmentResponse:
    return registry.get_job(job_id)


@router.get(
    "/v1/analytics/skills/top",
    response_model=list[MetricBucketResponse],
    tags=["analytics"],
)
def top_skills(registry: ServiceRegistry = Depends(get_registry)) -> list[MetricBucketResponse]:
    return [metric_bucket_to_response(item) for item in registry.analytics_service.top_skills()]


@router.get(
    "/v1/analytics/technologies/top",
    response_model=list[MetricBucketResponse],
    tags=["analytics"],
)
def top_technologies(registry: ServiceRegistry = Depends(get_registry)) -> list[MetricBucketResponse]:
    return [metric_bucket_to_response(item) for item in registry.analytics_service.top_technologies()]


@router.get(
    "/v1/analytics/skills/cooccurrence",
    response_model=list[SkillCooccurrenceResponse],
    tags=["analytics"],
)
def skill_cooccurrence(
    registry: ServiceRegistry = Depends(get_registry),
) -> list[SkillCooccurrenceResponse]:
    return [
        cooccurrence_to_response(item)
        for item in registry.analytics_service.skill_cooccurrence()
    ]


@router.post(
    "/v1/candidates/matches",
    response_model=list[MatchResult],
    tags=["candidates"],
)
def candidate_matches(
    request: CandidateProfileRequest,
    registry: ServiceRegistry = Depends(get_registry),
) -> list[MatchResult]:
    return [MatchResult.from_domain(result) for result in registry.match_candidate(request)]


def metric_bucket_to_response(metric: MetricBucket) -> MetricBucketResponse:
    return MetricBucketResponse(label=metric.label, value=metric.value)


def cooccurrence_to_response(item: SkillCooccurrence) -> SkillCooccurrenceResponse:
    return SkillCooccurrenceResponse(
        left_skill=item.left_skill,
        right_skill=item.right_skill,
        frequency=item.frequency,
    )
