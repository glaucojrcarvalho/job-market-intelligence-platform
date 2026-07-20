from __future__ import annotations

from job_market.application.enrichment.service import JobEnrichmentService
from job_market.domain.jobs.models import JobPosting
from job_market.infrastructure.ai.deterministic import (
    HeuristicRoleClassifier,
    HeuristicSummaryProvider,
    TaxonomySkillExtractor,
    TaxonomyTechnologyExtractor,
)
from job_market.infrastructure.repositories.memory import InMemoryEnrichmentRepository


def test_enrichment_service_persists_structured_enrichment() -> None:
    repository = InMemoryEnrichmentRepository()
    service = JobEnrichmentService(
        enrichment_repository=repository,
        skill_extractor=TaxonomySkillExtractor(),
        technology_extractor=TaxonomyTechnologyExtractor(),
        role_classifier=HeuristicRoleClassifier(),
        summary_provider=HeuristicSummaryProvider(),
    )
    job = JobPosting(
        job_id=7,
        title="Senior Data Engineer",
        description="Required: Python, SQL, AWS and Airflow. Build pipelines with Spark.",
        source_name="manual",
    )

    enrichment = service.enrich(job)

    assert enrichment.job_id == 7
    assert enrichment.classification is not None
    assert enrichment.classification.role_family == "data_engineering"
    assert enrichment.summary is not None
    assert repository.get_by_job_id(7) == enrichment
    assert any(skill.name == "airflow" for skill in enrichment.skills)
    assert any(technology.name == "spark" for technology in enrichment.technologies)
