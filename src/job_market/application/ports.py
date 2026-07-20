"""Service ports and repository protocols."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Protocol

from job_market.domain.analytics.models import MetricBucket, SkillCooccurrence
from job_market.domain.candidates.models import CandidateProfile
from job_market.domain.enrichment.models import (
    JobClassification,
    JobEnrichment,
    SkillEvidence,
    TechnologyEvidence,
)
from job_market.domain.jobs.models import JobPosting, RawJobRecord
from job_market.domain.matching.models import MatchResult


class RawJobRepository(Protocol):
    def add(self, record: RawJobRecord) -> RawJobRecord: ...


class JobRepository(Protocol):
    def add(self, job: JobPosting) -> JobPosting: ...
    def list_all(self) -> Sequence[JobPosting]: ...
    def get_by_id(self, job_id: int) -> JobPosting | None: ...


class EnrichmentRepository(Protocol):
    def add(self, enrichment: JobEnrichment) -> JobEnrichment: ...
    def list_all(self) -> Sequence[JobEnrichment]: ...
    def get_by_job_id(self, job_id: int) -> JobEnrichment | None: ...


class MatchRepository(Protocol):
    def add(self, result: MatchResult) -> MatchResult: ...
    def list_all(self) -> Sequence[MatchResult]: ...


class SourceAdapter(Protocol):
    source_name: str

    def fetch(self) -> Iterable[RawJobRecord]: ...


class SkillExtractor(Protocol):
    def extract(self, description: str) -> Sequence[SkillEvidence]: ...


class TechnologyExtractor(Protocol):
    def extract(self, description: str) -> Sequence[TechnologyEvidence]: ...


class RoleClassifier(Protocol):
    def classify(self, title: str, description: str) -> tuple[str, str, float]: ...


class SummaryProvider(Protocol):
    def summarize(
        self,
        job: JobPosting,
        classification: JobClassification | None,
        skills: Sequence[SkillEvidence],
        technologies: Sequence[TechnologyEvidence],
    ) -> str | None: ...


class MatchScorer(Protocol):
    def score(
        self,
        candidate: CandidateProfile,
        jobs: Sequence[JobPosting],
        enrichments: Sequence[JobEnrichment],
    ) -> Sequence[MatchResult]: ...


class AnalyticsReader(Protocol):
    def top_skills(self) -> Sequence[MetricBucket]: ...
    def top_technologies(self) -> Sequence[MetricBucket]: ...
    def skill_cooccurrence(self) -> Sequence[SkillCooccurrence]: ...
