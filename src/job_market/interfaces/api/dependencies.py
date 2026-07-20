"""Dependency wiring for the FastAPI application."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from functools import lru_cache

from job_market import __version__
from job_market.application.analytics.service import AnalyticsService
from job_market.application.enrichment.service import JobEnrichmentService
from job_market.application.ingestion.service import JobIngestionService
from job_market.application.matching.service import CandidateMatchingService
from job_market.application.normalization.service import JobNormalizationService
from job_market.application.ports import (
    AnalyticsReader,
    EnrichmentRepository,
    JobRepository,
    MatchRepository,
    RawJobRepository,
)
from job_market.config.settings import Settings
from job_market.domain.candidates.models import CandidateProfile, CandidateSkill
from job_market.domain.enrichment.models import JobEnrichment
from job_market.domain.jobs.models import (
    Compensation,
    JobPosting,
    Location,
    RawJobRecord,
    Seniority,
    WorkMode,
)
from job_market.domain.matching.models import MatchResult as DomainMatchResult
from job_market.infrastructure.ai.deterministic import (
    HeuristicRoleClassifier,
    HeuristicSummaryProvider,
    OverlapMatchScorer,
    TaxonomySkillExtractor,
    TaxonomyTechnologyExtractor,
)
from job_market.infrastructure.repositories.memory import (
    InMemoryAnalyticsReader,
    InMemoryEnrichmentRepository,
    InMemoryJobRepository,
    InMemoryMatchRepository,
    InMemoryRawJobRepository,
)
from job_market.interfaces.schemas.candidates import CandidateProfileRequest
from job_market.interfaces.schemas.jobs import (
    JobEnrichmentResponse,
    JobResponse,
    JobWithEnrichmentResponse,
    ManualJobUploadRequest,
)
from job_market.shared.exceptions import InvalidStateError, ResourceNotFoundError


@dataclass
class ServiceRegistry:
    settings: Settings
    raw_job_repository: RawJobRepository
    job_repository: JobRepository
    enrichment_repository: EnrichmentRepository
    match_repository: MatchRepository
    normalization_service: JobNormalizationService
    ingestion_service: JobIngestionService
    enrichment_service: JobEnrichmentService
    analytics_service: AnalyticsService
    matching_service: CandidateMatchingService

    def upload_job(self, request: ManualJobUploadRequest) -> JobWithEnrichmentResponse:
        raw_record = RawJobRecord(
            source_name=request.source_name,
            source_job_id=None,
            source_url=request.source_url,
            payload=request.description,
            observed_at=datetime.now(UTC),
        )

        def normalize_record(record: RawJobRecord) -> JobPosting:
            work_mode = WorkMode(request.work_mode) if request.work_mode else WorkMode.UNKNOWN
            return JobPosting(
                raw_record_id=record.record_id,
                title=request.title,
                description=request.description,
                source_name=record.source_name,
                source_url=request.source_url,
                company_name=request.company_name,
                work_mode=work_mode,
                location=Location(raw_text=request.location_text),
                compensation=Compensation(raw_text=request.salary_text),
                seniority_hint=Seniority.UNKNOWN,
            )

        job = self.ingestion_service.ingest(
            raw_records=[raw_record],
            normalize_record=normalize_record,
        )[0]
        enrichment = self.enrichment_service.enrich(job)
        if job.job_id is None:
            raise InvalidStateError("The stored job did not receive an identifier.")
        return build_job_with_enrichment_response(job, enrichment)

    def list_jobs(self) -> list[JobResponse]:
        jobs = self.job_repository.list_all()
        return [build_job_response(job) for job in jobs]

    def get_job(self, job_id: int) -> JobWithEnrichmentResponse:
        job = self.job_repository.get_by_id(job_id)
        if job is None:
            raise ResourceNotFoundError(f"Job {job_id} was not found.")
        enrichment = self.enrichment_repository.get_by_job_id(job_id)
        return build_job_with_enrichment_response(job, enrichment)

    def match_candidate(self, request: CandidateProfileRequest) -> list[DomainMatchResult]:
        candidate = CandidateProfile(
            profile_id=None,
            summary=request.summary,
            skills=[
                CandidateSkill(name=skill.name, proficiency=skill.proficiency)
                for skill in request.skills
            ],
            location=request.location,
            years_experience=request.years_experience,
        )
        return self.matching_service.match(candidate)


def build_job_response(job: JobPosting) -> JobResponse:
    if job.job_id is None:
        raise InvalidStateError("Job responses require a persisted job identifier.")

    return JobResponse(
        job_id=job.job_id,
        title=job.title,
        source_name=job.source_name,
        work_mode=job.work_mode.value,
        location_text=job.location.raw_text,
        salary_text=job.compensation.raw_text,
    )


def build_job_enrichment_response(enrichment: JobEnrichment | None) -> JobEnrichmentResponse | None:
    if enrichment is None:
        return None

    return JobEnrichmentResponse(
        job_id=enrichment.job_id,
        role_family=enrichment.classification.role_family if enrichment.classification else None,
        seniority=enrichment.classification.seniority.value if enrichment.classification else None,
        confidence=enrichment.classification.confidence if enrichment.classification else None,
        skills=[skill.name for skill in enrichment.skills],
        technologies=[technology.name for technology in enrichment.technologies],
        skill_details=[
            {
                "name": skill.name,
                "evidence": skill.evidence,
                "confidence": skill.confidence,
                "is_required": skill.is_required,
            }
            for skill in enrichment.skills
        ],
        technology_details=[
            {
                "name": technology.name,
                "category": technology.category,
                "evidence": technology.evidence,
                "confidence": technology.confidence,
            }
            for technology in enrichment.technologies
        ],
        summary=enrichment.summary,
    )


def build_job_with_enrichment_response(
    job: JobPosting,
    enrichment: JobEnrichment | None,
) -> JobWithEnrichmentResponse:
    return JobWithEnrichmentResponse(
        **build_job_response(job).model_dump(),
        enrichment=build_job_enrichment_response(enrichment),
    )


@lru_cache(maxsize=1)
def get_registry() -> ServiceRegistry:
    settings = Settings.from_env()
    raw_job_repository: RawJobRepository
    job_repository: JobRepository
    enrichment_repository: EnrichmentRepository
    match_repository: MatchRepository
    analytics_reader: AnalyticsReader
    if settings.database_url:
        from job_market.infrastructure.db.session import session_factory_from_url
        from job_market.infrastructure.repositories.sqlalchemy import (
            SqlAlchemyAnalyticsReader,
            SqlAlchemyEnrichmentRepository,
            SqlAlchemyJobRepository,
            SqlAlchemyMatchRepository,
            SqlAlchemyRawJobRepository,
        )

        session_factory = session_factory_from_url(settings.database_url)
        raw_job_repository = SqlAlchemyRawJobRepository(session_factory)
        job_repository = SqlAlchemyJobRepository(session_factory)
        enrichment_repository = SqlAlchemyEnrichmentRepository(session_factory)
        match_repository = SqlAlchemyMatchRepository(session_factory)
        analytics_reader = SqlAlchemyAnalyticsReader(session_factory)
    else:
        raw_job_repository = InMemoryRawJobRepository()
        job_repository = InMemoryJobRepository()
        enrichment_repository = InMemoryEnrichmentRepository()
        match_repository = InMemoryMatchRepository()
        analytics_reader = InMemoryAnalyticsReader(enrichment_repository)
    normalization_service = JobNormalizationService()
    ingestion_service = JobIngestionService(
        raw_repository=raw_job_repository,
        job_repository=job_repository,
    )
    enrichment_service = JobEnrichmentService(
        enrichment_repository=enrichment_repository,
        skill_extractor=TaxonomySkillExtractor(),
        technology_extractor=TaxonomyTechnologyExtractor(),
        role_classifier=HeuristicRoleClassifier(),
        summary_provider=HeuristicSummaryProvider(),
    )
    analytics_service = AnalyticsService(analytics_reader)
    matching_service = CandidateMatchingService(
        job_repository=job_repository,
        enrichment_repository=enrichment_repository,
        match_repository=match_repository,
        scorer=OverlapMatchScorer(),
    )
    return ServiceRegistry(
        settings=settings,
        raw_job_repository=raw_job_repository,
        job_repository=job_repository,
        enrichment_repository=enrichment_repository,
        match_repository=match_repository,
        normalization_service=normalization_service,
        ingestion_service=ingestion_service,
        enrichment_service=enrichment_service,
        analytics_service=analytics_service,
        matching_service=matching_service,
    )


def get_version() -> str:
    return __version__
