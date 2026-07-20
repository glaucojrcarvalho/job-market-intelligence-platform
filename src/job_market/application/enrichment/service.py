"""Deterministic enrichment service."""

from __future__ import annotations

from job_market.application.ports import (
    EnrichmentRepository,
    RoleClassifier,
    SkillExtractor,
    SummaryProvider,
    TechnologyExtractor,
)
from job_market.domain.enrichment.models import (
    JobClassification,
    JobEnrichment,
)
from job_market.domain.jobs.models import JobPosting, Seniority


class JobEnrichmentService:
    """Build structured enrichment outputs from normalized jobs."""

    def __init__(
        self,
        *,
        enrichment_repository: EnrichmentRepository,
        skill_extractor: SkillExtractor,
        technology_extractor: TechnologyExtractor,
        role_classifier: RoleClassifier,
        summary_provider: SummaryProvider,
    ) -> None:
        self._enrichment_repository = enrichment_repository
        self._skill_extractor = skill_extractor
        self._technology_extractor = technology_extractor
        self._role_classifier = role_classifier
        self._summary_provider = summary_provider

    def enrich(self, job: JobPosting) -> JobEnrichment:
        skills = list(self._skill_extractor.extract(job.description))
        technologies = list(self._technology_extractor.extract(job.description))
        role_family, seniority_name, confidence = self._role_classifier.classify(
            job.title,
            job.description,
        )
        classification = JobClassification(
            role_family=role_family,
            seniority=Seniority(seniority_name),
            confidence=confidence,
        )
        summary = self._summary_provider.summarize(
            job,
            classification,
            skills,
            technologies,
        )
        return self._enrichment_repository.add(
            JobEnrichment(
                job_id=job.job_id,
                skills=skills,
                technologies=technologies,
                classification=classification,
                summary=summary,
            )
        )
