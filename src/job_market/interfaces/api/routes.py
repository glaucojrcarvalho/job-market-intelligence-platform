"""FastAPI route definitions."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, status

from job_market.domain.analytics.models import MetricBucket, SkillCooccurrence
from job_market.domain.jobs.models import WorkMode
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
RegistryDependency = Annotated[ServiceRegistry, Depends(get_registry)]


@router.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/ready", response_model=ReadinessResponse, tags=["system"])
def ready(registry: RegistryDependency) -> ReadinessResponse:
    return ReadinessResponse(
        status="ok",
        checks={
            "repositories": "ok",
            "environment": registry.settings.environment,
        },
    )


@router.get("/version", response_model=VersionResponse, tags=["system"])
def version(registry: RegistryDependency) -> VersionResponse:
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
    registry: RegistryDependency,
) -> JobWithEnrichmentResponse:
    return registry.upload_job(request)


@router.get("/v1/jobs", response_model=list[JobResponse], tags=["jobs"])
def list_jobs(
    registry: RegistryDependency,
    limit: Annotated[int | None, Query(ge=1, le=100)] = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    source_name: Annotated[str | None, Query(min_length=1, max_length=100)] = None,
    work_mode: WorkMode | None = None,
) -> list[JobResponse]:
    return registry.list_jobs(
        limit=limit,
        offset=offset,
        source_name=source_name,
        work_mode=work_mode,
    )


@router.get("/v1/jobs/{job_id}", response_model=JobWithEnrichmentResponse, tags=["jobs"])
def get_job(job_id: int, registry: RegistryDependency) -> JobWithEnrichmentResponse:
    return registry.get_job(job_id)


@router.get(
    "/v1/analytics/skills/top",
    response_model=list[MetricBucketResponse],
    tags=["analytics"],
)
def top_skills(registry: RegistryDependency) -> list[MetricBucketResponse]:
    return [metric_bucket_to_response(item) for item in registry.analytics_service.top_skills()]


@router.get(
    "/v1/analytics/technologies/top",
    response_model=list[MetricBucketResponse],
    tags=["analytics"],
)
def top_technologies(
    registry: RegistryDependency,
) -> list[MetricBucketResponse]:
    return [
        metric_bucket_to_response(item) for item in registry.analytics_service.top_technologies()
    ]


@router.get(
    "/v1/analytics/skills/cooccurrence",
    response_model=list[SkillCooccurrenceResponse],
    tags=["analytics"],
)
def skill_cooccurrence(
    registry: RegistryDependency,
) -> list[SkillCooccurrenceResponse]:
    return [
        cooccurrence_to_response(item) for item in registry.analytics_service.skill_cooccurrence()
    ]


@router.post(
    "/v1/candidates/matches",
    response_model=list[MatchResult],
    tags=["candidates"],
)
def candidate_matches(
    request: CandidateProfileRequest,
    registry: RegistryDependency,
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
