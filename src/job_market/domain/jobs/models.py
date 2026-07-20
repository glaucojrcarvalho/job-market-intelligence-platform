"""Core job-related domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum


class WorkMode(StrEnum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    ONSITE = "onsite"
    UNKNOWN = "unknown"


class EmploymentType(StrEnum):
    FULL_TIME = "full_time"
    CONTRACT = "contract"
    TEMPORARY = "temporary"
    INTERN = "intern"
    UNKNOWN = "unknown"


class Seniority(StrEnum):
    INTERN = "intern"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    STAFF = "staff"
    PRINCIPAL = "principal"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Location:
    country: str | None = None
    region: str | None = None
    city: str | None = None
    raw_text: str | None = None


@dataclass(frozen=True)
class Compensation:
    currency: str | None = None
    minimum: float | None = None
    maximum: float | None = None
    raw_text: str | None = None


@dataclass(frozen=True)
class RawJobRecord:
    source_name: str
    source_job_id: str | None
    source_url: str | None
    payload: str
    observed_at: datetime
    record_id: int | None = None


@dataclass(frozen=True)
class JobPosting:
    title: str
    description: str
    source_name: str
    work_mode: WorkMode = WorkMode.UNKNOWN
    employment_type: EmploymentType = EmploymentType.UNKNOWN
    location: Location = field(default_factory=Location)
    compensation: Compensation = field(default_factory=Compensation)
    company_name: str | None = None
    source_url: str | None = None
    posted_at: datetime | None = None
    seniority_hint: Seniority = Seniority.UNKNOWN
    job_id: int | None = None
    raw_record_id: int | None = None
