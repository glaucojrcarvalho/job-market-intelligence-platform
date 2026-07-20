"""Normalization service for raw job records."""

from __future__ import annotations

from job_market.domain.jobs.models import (
    Compensation,
    JobPosting,
    Location,
    RawJobRecord,
    Seniority,
    WorkMode,
)
from job_market.shared.text import normalize_whitespace


class JobNormalizationService:
    """Convert raw source records into canonical job postings."""

    def normalize(self, record: RawJobRecord) -> JobPosting:
        title = "Unknown title"
        description = normalize_whitespace(record.payload)

        return JobPosting(
            raw_record_id=record.record_id,
            title=title,
            description=description,
            source_name=record.source_name,
            source_url=record.source_url,
            location=Location(raw_text=None),
            compensation=Compensation(raw_text=None),
            work_mode=WorkMode.UNKNOWN,
            seniority_hint=Seniority.UNKNOWN,
        )
