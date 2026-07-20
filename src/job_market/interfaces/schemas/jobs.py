"""Job-related API schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field

from job_market.domain.jobs.models import WorkMode


class JobIngestRequest(BaseModel):
    source_name: str = Field(..., examples=["manual_upload"])
    source_url: str | None = None
    payload: str = Field(..., min_length=1)


class ManualJobUploadRequest(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    source_name: str = Field(default="manual_upload")
    source_url: str | None = None
    company_name: str | None = None
    location_text: str | None = None
    salary_text: str | None = None
    work_mode: WorkMode | None = None


class JobResponse(BaseModel):
    job_id: int
    title: str
    source_name: str
    work_mode: str
    location_text: str | None = None
    salary_text: str | None = None


class JobEnrichmentResponse(BaseModel):
    job_id: int | None = None
    role_family: str | None = None
    seniority: str | None = None
    confidence: float | None = None
    skills: list[str]
    technologies: list[str]
    skill_details: list[dict[str, str | float | bool | None]]
    technology_details: list[dict[str, str | float | None]]
    summary: str | None = None


class JobWithEnrichmentResponse(JobResponse):
    enrichment: JobEnrichmentResponse | None = None
