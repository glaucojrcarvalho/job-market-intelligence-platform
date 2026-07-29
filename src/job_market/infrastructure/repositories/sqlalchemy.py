"""SQLAlchemy-backed repository implementations."""

from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime

from job_market.domain.analytics.models import MetricBucket, SkillCooccurrence
from job_market.domain.enrichment.models import (
    JobClassification,
    JobEnrichment,
    SkillEvidence,
    TechnologyEvidence,
)
from job_market.domain.jobs.models import (
    Compensation,
    EmploymentType,
    JobPosting,
    Location,
    RawJobRecord,
    Seniority,
    WorkMode,
)
from job_market.domain.matching.models import MatchReason, MatchResult
from job_market.infrastructure.db.models import (
    CandidateMatchModel,
    JobEnrichmentModel,
    JobModel,
    RawJobRecordModel,
)
from job_market.infrastructure.db.session import SessionFactory


class SqlAlchemyRawJobRepository:
    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory

    def add(self, record: RawJobRecord) -> RawJobRecord:
        with self._session_factory() as session:
            model = RawJobRecordModel(
                source_name=record.source_name,
                source_job_id=record.source_job_id,
                source_url=record.source_url,
                payload=record.payload,
                observed_at=record.observed_at,
            )
            session.add(model)
            session.commit()
            session.refresh(model)
            return RawJobRecord(
                record_id=model.id,
                source_name=model.source_name,
                source_job_id=model.source_job_id,
                source_url=model.source_url,
                payload=model.payload,
                observed_at=model.observed_at,
            )

    def get_by_id(self, record_id: int) -> RawJobRecord | None:
        with self._session_factory() as session:
            model = session.get(RawJobRecordModel, record_id)
            if model is None:
                return None
            return RawJobRecord(
                record_id=model.id,
                source_name=model.source_name,
                source_job_id=model.source_job_id,
                source_url=model.source_url,
                payload=model.payload,
                observed_at=model.observed_at,
            )


class SqlAlchemyJobRepository:
    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory

    def add(self, job: JobPosting) -> JobPosting:
        with self._session_factory() as session:
            model = JobModel(
                raw_job_record_id=job.raw_record_id,
                title=job.title,
                description=job.description,
                source_name=job.source_name,
                company_name=job.company_name,
                source_url=job.source_url,
                posted_at=job.posted_at,
                work_mode=job.work_mode.value,
                employment_type=job.employment_type.value,
                seniority_hint=job.seniority_hint.value,
                location_country=job.location.country,
                location_region=job.location.region,
                location_city=job.location.city,
                location_raw_text=job.location.raw_text,
                compensation_currency=job.compensation.currency,
                compensation_minimum=job.compensation.minimum,
                compensation_maximum=job.compensation.maximum,
                compensation_raw_text=job.compensation.raw_text,
            )
            session.add(model)
            session.commit()
            session.refresh(model)
            return _to_job_posting(model)

    def list_all(
        self,
        *,
        limit: int | None = None,
        offset: int = 0,
        source_name: str | None = None,
        work_mode: WorkMode | None = None,
    ) -> list[JobPosting]:
        with self._session_factory() as session:
            query = session.query(JobModel)
            if source_name is not None:
                query = query.filter(JobModel.source_name == source_name)
            if work_mode is not None:
                query = query.filter(JobModel.work_mode == work_mode.value)
            query = query.order_by(JobModel.id.asc()).offset(offset)
            if limit is not None:
                query = query.limit(limit)
            models = query.all()
            return [_to_job_posting(model) for model in models]

    def get_by_id(self, job_id: int) -> JobPosting | None:
        with self._session_factory() as session:
            model = session.get(JobModel, job_id)
            return _to_job_posting(model) if model else None


class SqlAlchemyEnrichmentRepository:
    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory

    def add(self, enrichment: JobEnrichment) -> JobEnrichment:
        if enrichment.job_id is None:
            raise ValueError("A persisted enrichment requires a job_id.")

        with self._session_factory() as session:
            model = (
                session.query(JobEnrichmentModel).filter_by(job_id=enrichment.job_id).one_or_none()
            )
            if model is None:
                model = JobEnrichmentModel(job_id=enrichment.job_id, skills=[], technologies=[])
                session.add(model)

            model.role_family = (
                enrichment.classification.role_family if enrichment.classification else None
            )
            model.seniority = (
                enrichment.classification.seniority.value if enrichment.classification else None
            )
            model.classification_confidence = (
                enrichment.classification.confidence if enrichment.classification else None
            )
            model.classification_evidence = (
                enrichment.classification.evidence if enrichment.classification else None
            )
            model.summary = enrichment.summary
            model.skills = [
                {
                    "name": skill.name,
                    "evidence": skill.evidence,
                    "confidence": skill.confidence,
                    "is_required": skill.is_required,
                }
                for skill in enrichment.skills
            ]
            model.technologies = [
                {
                    "name": technology.name,
                    "category": technology.category,
                    "evidence": technology.evidence,
                    "confidence": technology.confidence,
                }
                for technology in enrichment.technologies
            ]
            session.commit()
            session.refresh(model)
            return _to_job_enrichment(model)

    def list_all(self) -> list[JobEnrichment]:
        with self._session_factory() as session:
            models = (
                session.query(JobEnrichmentModel).order_by(JobEnrichmentModel.job_id.asc()).all()
            )
            return [_to_job_enrichment(model) for model in models]

    def get_by_job_id(self, job_id: int) -> JobEnrichment | None:
        with self._session_factory() as session:
            model = session.query(JobEnrichmentModel).filter_by(job_id=job_id).one_or_none()
            return _to_job_enrichment(model) if model else None


class SqlAlchemyMatchRepository:
    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory

    def add(self, result: MatchResult) -> MatchResult:
        with self._session_factory() as session:
            model = CandidateMatchModel(
                candidate_profile_id=None,
                job_id=result.job_id,
                job_title=result.job_title,
                source_name=result.source_name,
                match_score=result.match_score,
                confidence=result.confidence,
                matching_skills=result.matching_skills,
                missing_skills=result.missing_skills,
                reasons=[
                    {"type": reason.type, "message": reason.message} for reason in result.reasons
                ],
                created_at=datetime.now(UTC),
            )
            session.add(model)
            session.commit()
            session.refresh(model)
            return _to_match_result(model)

    def list_all(self) -> list[MatchResult]:
        with self._session_factory() as session:
            models = session.query(CandidateMatchModel).order_by(CandidateMatchModel.id.asc()).all()
            return [_to_match_result(model) for model in models]


class SqlAlchemyAnalyticsReader:
    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory

    def top_skills(self) -> list[MetricBucket]:
        counter: Counter[str] = Counter()
        with self._session_factory() as session:
            for enrichment in session.query(JobEnrichmentModel).all():
                counter.update(skill["name"] for skill in enrichment.skills)
        return [MetricBucket(label=label, value=value) for label, value in counter.most_common()]

    def top_technologies(self) -> list[MetricBucket]:
        counter: Counter[str] = Counter()
        with self._session_factory() as session:
            for enrichment in session.query(JobEnrichmentModel).all():
                counter.update(technology["name"] for technology in enrichment.technologies)
        return [MetricBucket(label=label, value=value) for label, value in counter.most_common()]

    def skill_cooccurrence(self) -> list[SkillCooccurrence]:
        pairs: Counter[tuple[str, str]] = Counter()
        with self._session_factory() as session:
            for enrichment in session.query(JobEnrichmentModel).all():
                skills = sorted({skill["name"] for skill in enrichment.skills})
                for index, left_skill in enumerate(skills):
                    for right_skill in skills[index + 1 :]:
                        pairs[(left_skill, right_skill)] += 1
        return [
            SkillCooccurrence(left_skill=left, right_skill=right, frequency=frequency)
            for (left, right), frequency in pairs.most_common()
        ]


def _to_job_posting(model: JobModel) -> JobPosting:
    return JobPosting(
        job_id=model.id,
        raw_record_id=model.raw_job_record_id,
        title=model.title,
        description=model.description,
        source_name=model.source_name,
        work_mode=WorkMode(model.work_mode),
        employment_type=EmploymentType(model.employment_type),
        location=Location(
            country=model.location_country,
            region=model.location_region,
            city=model.location_city,
            raw_text=model.location_raw_text,
        ),
        compensation=Compensation(
            currency=model.compensation_currency,
            minimum=model.compensation_minimum,
            maximum=model.compensation_maximum,
            raw_text=model.compensation_raw_text,
        ),
        company_name=model.company_name,
        source_url=model.source_url,
        posted_at=model.posted_at,
        seniority_hint=Seniority(model.seniority_hint),
    )


def _to_job_enrichment(model: JobEnrichmentModel) -> JobEnrichment:
    classification = None
    if model.role_family and model.seniority:
        classification = JobClassification(
            role_family=model.role_family,
            seniority=Seniority(model.seniority),
            confidence=model.classification_confidence or 0.0,
            evidence=model.classification_evidence,
        )
    return JobEnrichment(
        job_id=model.job_id,
        skills=[
            SkillEvidence(
                name=skill["name"],
                evidence=skill.get("evidence"),
                confidence=skill.get("confidence", 1.0),
                is_required=skill.get("is_required", True),
            )
            for skill in model.skills
        ],
        technologies=[
            TechnologyEvidence(
                name=technology["name"],
                category=technology["category"],
                evidence=technology.get("evidence"),
                confidence=technology.get("confidence", 1.0),
            )
            for technology in model.technologies
        ],
        classification=classification,
        summary=model.summary,
    )


def _to_match_result(model: CandidateMatchModel) -> MatchResult:
    return MatchResult(
        match_id=model.id,
        job_id=model.job_id,
        job_title=model.job_title,
        source_name=model.source_name,
        match_score=model.match_score,
        matching_skills=list(model.matching_skills),
        missing_skills=list(model.missing_skills),
        confidence=model.confidence,
        reasons=[
            MatchReason(type=reason["type"], message=reason["message"]) for reason in model.reasons
        ],
    )
