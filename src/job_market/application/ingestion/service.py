"""Job ingestion orchestration."""

from __future__ import annotations

from collections.abc import Iterable

from job_market.application.ports import JobRepository, RawJobRepository
from job_market.domain.jobs.models import JobPosting, RawJobRecord


class JobIngestionService:
    """Persist raw source records and normalized jobs in one flow."""

    def __init__(
        self,
        *,
        raw_repository: RawJobRepository,
        job_repository: JobRepository,
    ) -> None:
        self._raw_repository = raw_repository
        self._job_repository = job_repository

    def ingest(
        self,
        *,
        raw_records: Iterable[RawJobRecord],
        normalize_record,
    ) -> list[JobPosting]:
        jobs: list[JobPosting] = []

        for raw_record in raw_records:
            stored_record = self._raw_repository.add(raw_record)
            normalized_job = normalize_record(stored_record)
            jobs.append(self._job_repository.add(normalized_job))

        return jobs
