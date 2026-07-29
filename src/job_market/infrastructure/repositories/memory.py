"""In-memory repositories for local development and early tests."""

from __future__ import annotations

from collections import Counter

from job_market.domain.analytics.models import MetricBucket, SkillCooccurrence
from job_market.domain.enrichment.models import JobEnrichment
from job_market.domain.jobs.models import JobPosting, RawJobRecord, WorkMode
from job_market.domain.matching.models import MatchResult


class InMemoryRawJobRepository:
    def __init__(self) -> None:
        self._records: list[RawJobRecord] = []
        self._next_id = 1

    def add(self, record: RawJobRecord) -> RawJobRecord:
        stored = RawJobRecord(
            record_id=self._next_id,
            source_name=record.source_name,
            source_job_id=record.source_job_id,
            source_url=record.source_url,
            payload=record.payload,
            observed_at=record.observed_at,
        )
        self._next_id += 1
        self._records.append(stored)
        return stored

    def get_by_id(self, record_id: int) -> RawJobRecord | None:
        return next((record for record in self._records if record.record_id == record_id), None)


class InMemoryJobRepository:
    def __init__(self) -> None:
        self._jobs: list[JobPosting] = []
        self._next_id = 1

    def add(self, job: JobPosting) -> JobPosting:
        stored = JobPosting(
            job_id=self._next_id,
            raw_record_id=job.raw_record_id,
            title=job.title,
            description=job.description,
            source_name=job.source_name,
            work_mode=job.work_mode,
            employment_type=job.employment_type,
            location=job.location,
            compensation=job.compensation,
            company_name=job.company_name,
            source_url=job.source_url,
            posted_at=job.posted_at,
            seniority_hint=job.seniority_hint,
        )
        self._next_id += 1
        self._jobs.append(stored)
        return stored

    def list_all(
        self,
        *,
        limit: int | None = None,
        offset: int = 0,
        source_name: str | None = None,
        work_mode: WorkMode | None = None,
    ) -> list[JobPosting]:
        jobs = self._jobs
        if source_name is not None:
            jobs = [job for job in jobs if job.source_name == source_name]
        if work_mode is not None:
            jobs = [job for job in jobs if job.work_mode == work_mode]

        bounded_jobs = jobs[offset:]
        if limit is not None:
            bounded_jobs = bounded_jobs[:limit]
        return list(bounded_jobs)

    def get_by_id(self, job_id: int) -> JobPosting | None:
        return next((job for job in self._jobs if job.job_id == job_id), None)


class InMemoryEnrichmentRepository:
    def __init__(self) -> None:
        self._enrichments: list[JobEnrichment] = []

    def add(self, enrichment: JobEnrichment) -> JobEnrichment:
        self._enrichments.append(enrichment)
        return enrichment

    def list_all(self) -> list[JobEnrichment]:
        return list(self._enrichments)

    def get_by_job_id(self, job_id: int) -> JobEnrichment | None:
        return next((item for item in self._enrichments if item.job_id == job_id), None)


class InMemoryMatchRepository:
    def __init__(self) -> None:
        self._results: list[MatchResult] = []

    def add(self, result: MatchResult) -> MatchResult:
        self._results.append(result)
        return result

    def list_all(self) -> list[MatchResult]:
        return list(self._results)


class InMemoryAnalyticsReader:
    def __init__(self, enrichment_repository: InMemoryEnrichmentRepository) -> None:
        self._enrichment_repository = enrichment_repository

    def top_skills(self) -> list[MetricBucket]:
        counter = Counter(
            skill.name
            for enrichment in self._enrichment_repository.list_all()
            for skill in enrichment.skills
        )
        return [MetricBucket(label=label, value=value) for label, value in counter.most_common()]

    def top_technologies(self) -> list[MetricBucket]:
        counter = Counter(
            technology.name
            for enrichment in self._enrichment_repository.list_all()
            for technology in enrichment.technologies
        )
        return [MetricBucket(label=label, value=value) for label, value in counter.most_common()]

    def skill_cooccurrence(self) -> list[SkillCooccurrence]:
        pairs: Counter[tuple[str, str]] = Counter()
        for enrichment in self._enrichment_repository.list_all():
            skills = sorted({skill.name for skill in enrichment.skills})
            for index, left_skill in enumerate(skills):
                for right_skill in skills[index + 1 :]:
                    pairs[(left_skill, right_skill)] += 1

        return [
            SkillCooccurrence(left_skill=left, right_skill=right, frequency=frequency)
            for (left, right), frequency in pairs.most_common()
        ]
