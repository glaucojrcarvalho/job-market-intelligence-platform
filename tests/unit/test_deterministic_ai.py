from __future__ import annotations

from job_market.domain.candidates.models import CandidateProfile, CandidateSkill
from job_market.domain.enrichment.models import (
    JobClassification,
    JobEnrichment,
    SkillEvidence,
    TechnologyEvidence,
)
from job_market.domain.jobs.models import JobPosting, Seniority
from job_market.infrastructure.ai.deterministic import (
    HeuristicRoleClassifier,
    HeuristicSummaryProvider,
    OverlapMatchScorer,
    TaxonomySkillExtractor,
    TaxonomyTechnologyExtractor,
)


def test_skill_extractor_returns_evidence_and_required_flags() -> None:
    extractor = TaxonomySkillExtractor()

    extracted = extractor.extract(
        "We need Python and PostgreSQL experience. Docker is required. Nice to have Terraform."
    )

    extracted_by_name = {item.name: item for item in extracted}
    assert {"python", "sql", "postgresql", "docker", "terraform"} <= set(extracted_by_name)
    assert extracted_by_name["docker"].is_required is True
    assert "Docker is required." == extracted_by_name["docker"].evidence
    assert extracted_by_name["terraform"].confidence == 0.7


def test_technology_extractor_returns_categories() -> None:
    extractor = TaxonomyTechnologyExtractor()

    extracted = extractor.extract("Build APIs with FastAPI on AWS and PostgreSQL.")

    extracted_by_name = {item.name: item for item in extracted}
    assert extracted_by_name["fastapi"].category == "framework"
    assert extracted_by_name["aws"].category == "cloud"
    assert extracted_by_name["postgresql"].category == "database"


def test_role_classifier_detects_role_and_seniority() -> None:
    classifier = HeuristicRoleClassifier()

    role_family, seniority, confidence = classifier.classify(
        "Senior Backend Engineer",
        "Design APIs and microservices with FastAPI and Docker.",
    )

    assert role_family == "backend_engineering"
    assert seniority == "senior"
    assert confidence >= 0.8


def test_summary_provider_creates_readable_summary() -> None:
    provider = HeuristicSummaryProvider()
    job = JobPosting(
        job_id=1,
        title="Senior Backend Engineer",
        description="Python FastAPI PostgreSQL AWS",
        source_name="manual",
    )
    classification = JobClassification(
        role_family="backend_engineering",
        seniority=Seniority.SENIOR,
        confidence=0.82,
    )
    summary = provider.summarize(
        job,
        classification,
        skills=[
            SkillEvidence(name="python"),
            SkillEvidence(name="fastapi"),
            SkillEvidence(name="postgresql"),
        ],
        technologies=[
            TechnologyEvidence(name="aws", category="cloud"),
            TechnologyEvidence(name="docker", category="devops"),
        ],
    )

    assert summary is not None
    assert "Senior Backend Engineer" in summary
    assert "backend engineering" in summary
    assert "aws" in summary


def test_overlap_match_scorer_uses_skill_overlap_and_technology_bonus() -> None:
    scorer = OverlapMatchScorer()
    candidate = CandidateProfile(
        profile_id="candidate-1",
        summary="Experienced with AWS APIs and Python services.",
        skills=[CandidateSkill(name="python"), CandidateSkill(name="sql")],
    )
    job = JobPosting(
        job_id=101,
        title="Backend Engineer",
        description="Python SQL AWS",
        source_name="manual",
    )
    enrichment = JobEnrichment(
        job_id=101,
        skills=[
            SkillEvidence(name="python"),
            SkillEvidence(name="sql"),
            SkillEvidence(name="aws"),
        ],
        technologies=[TechnologyEvidence(name="aws", category="cloud")],
        classification=JobClassification(
            role_family="backend_engineering",
            seniority=Seniority.MID,
            confidence=0.75,
        ),
    )

    results = scorer.score(candidate, [job], [enrichment])

    assert len(results) == 1
    assert results[0].job_id == 101
    assert results[0].match_score > 0.66
    assert any(reason.type == "technology_alignment" for reason in results[0].reasons)
