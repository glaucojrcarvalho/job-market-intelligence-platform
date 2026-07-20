from __future__ import annotations

from datetime import UTC, datetime

from job_market.domain.enrichment.models import JobEnrichment, SkillEvidence
from job_market.domain.jobs.models import JobPosting, RawJobRecord
from job_market.infrastructure.repositories.memory import (
    InMemoryAnalyticsReader,
    InMemoryEnrichmentRepository,
    InMemoryJobRepository,
    InMemoryRawJobRepository,
)


def test_memory_repositories_assign_ids_and_support_lookup() -> None:
    raw_repository = InMemoryRawJobRepository()
    job_repository = InMemoryJobRepository()

    raw_record = raw_repository.add(
        RawJobRecord(
            source_name="manual",
            source_job_id=None,
            source_url=None,
            payload="description",
            observed_at=datetime.now(UTC),
        )
    )
    job = job_repository.add(
        JobPosting(
            raw_record_id=raw_record.record_id,
            title="Backend Engineer",
            description="Python SQL",
            source_name="manual",
        )
    )

    assert raw_record.record_id == 1
    assert job.job_id == 1
    assert job.raw_record_id == raw_record.record_id
    assert job_repository.get_by_id(1) == job


def test_memory_analytics_reader_aggregates_skill_metrics() -> None:
    enrichment_repository = InMemoryEnrichmentRepository()
    enrichment_repository.add(
        JobEnrichment(job_id=1, skills=[SkillEvidence(name="python"), SkillEvidence(name="sql")])
    )
    enrichment_repository.add(
        JobEnrichment(job_id=2, skills=[SkillEvidence(name="python"), SkillEvidence(name="aws")])
    )
    reader = InMemoryAnalyticsReader(enrichment_repository)

    top_skills = reader.top_skills()
    cooccurrence = reader.skill_cooccurrence()

    assert top_skills[0].label == "python"
    assert top_skills[0].value == 2
    assert any(
        pair.left_skill == "python" and pair.right_skill in {"aws", "sql"}
        for pair in cooccurrence
    )
