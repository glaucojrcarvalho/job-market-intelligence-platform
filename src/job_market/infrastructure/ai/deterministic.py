"""Deterministic AI and NLP components for the MVP."""

from __future__ import annotations

import re
from collections.abc import Sequence

from job_market.domain.candidates.models import CandidateProfile
from job_market.domain.enrichment.models import (
    JobClassification,
    JobEnrichment,
    SkillEvidence,
    TechnologyEvidence,
)
from job_market.domain.jobs.models import JobPosting
from job_market.domain.matching.models import MatchReason, MatchResult
from job_market.shared.text import normalize_whitespace, tokenize_words

SENTENCE_RE = re.compile(r"(?<=[.!?])\s+|\n+")

SKILL_TAXONOMY = {
    "python": {"aliases": ("python",), "category": "language"},
    "sql": {"aliases": ("sql", "postgresql", "mysql", "sql server"), "category": "query_language"},
    "aws": {"aliases": ("aws", "amazon web services"), "category": "cloud"},
    "azure": {"aliases": ("azure", "microsoft azure"), "category": "cloud"},
    "gcp": {"aliases": ("gcp", "google cloud", "google cloud platform"), "category": "cloud"},
    "docker": {"aliases": ("docker",), "category": "devops"},
    "kubernetes": {"aliases": ("kubernetes", "k8s"), "category": "devops"},
    "java": {"aliases": ("java",), "category": "language"},
    "postgresql": {"aliases": ("postgresql", "postgres"), "category": "database"},
    "fastapi": {"aliases": ("fastapi",), "category": "framework"},
    "django": {"aliases": ("django",), "category": "framework"},
    "pandas": {"aliases": ("pandas",), "category": "library"},
    "spark": {"aliases": ("spark", "apache spark", "pyspark"), "category": "data"},
    "airflow": {"aliases": ("airflow", "apache airflow"), "category": "orchestration"},
    "terraform": {"aliases": ("terraform",), "category": "infrastructure"},
}

TECHNOLOGY_TAXONOMY = {
    "aws": {"aliases": ("aws", "amazon web services"), "category": "cloud"},
    "azure": {"aliases": ("azure", "microsoft azure"), "category": "cloud"},
    "gcp": {"aliases": ("gcp", "google cloud", "google cloud platform"), "category": "cloud"},
    "docker": {"aliases": ("docker",), "category": "devops"},
    "kubernetes": {"aliases": ("kubernetes", "k8s"), "category": "devops"},
    "postgresql": {"aliases": ("postgresql", "postgres"), "category": "database"},
    "mysql": {"aliases": ("mysql",), "category": "database"},
    "fastapi": {"aliases": ("fastapi",), "category": "framework"},
    "django": {"aliases": ("django",), "category": "framework"},
    "spark": {"aliases": ("spark", "apache spark", "pyspark"), "category": "data"},
    "airflow": {"aliases": ("airflow", "apache airflow"), "category": "orchestration"},
    "terraform": {"aliases": ("terraform",), "category": "infrastructure"},
}

ROLE_HINTS = {
    "data_engineering": ("data engineer", "etl", "pipeline", "airflow", "spark"),
    "backend_engineering": ("backend", "api", "microservice", "fastapi", "django"),
    "data_science": ("data scientist", "machine learning", "statistics", "model"),
    "machine_learning": ("ml engineer", "machine learning engineer", "mlops"),
    "platform_engineering": ("platform engineer", "devops", "terraform", "kubernetes"),
}

SENIORITY_HINTS = {
    "principal": ("principal",),
    "staff": ("staff",),
    "senior": ("senior", "sênior"),
    "mid": ("pleno", "mid-level", "mid level"),
    "junior": ("junior", "júnior"),
    "intern": ("intern", "internship", "estágio"),
}


class TaxonomySkillExtractor:
    def extract(self, description: str) -> list[SkillEvidence]:
        return [
            SkillEvidence(
                name=canonical_name,
                evidence=evidence,
                confidence=0.85 if required else 0.7,
                is_required=required,
            )
            for canonical_name, evidence, required in _extract_taxonomy_terms(
                description,
                taxonomy=SKILL_TAXONOMY,
            )
        ]


class TaxonomyTechnologyExtractor:
    def extract(self, description: str) -> list[TechnologyEvidence]:
        extracted_terms = []
        for canonical_name, evidence, _ in _extract_taxonomy_terms(
            description,
            taxonomy=TECHNOLOGY_TAXONOMY,
        ):
            extracted_terms.append(
                TechnologyEvidence(
                    name=canonical_name,
                    category=TECHNOLOGY_TAXONOMY[canonical_name]["category"],
                    evidence=evidence,
                    confidence=0.8,
                )
            )
        return extracted_terms


class HeuristicRoleClassifier:
    def classify(self, title: str, description: str) -> tuple[str, str, float]:
        combined_text = normalize_whitespace(f"{title} {description}").lower()

        role_family = "software_engineering"
        role_confidence = 0.55
        for candidate_role, hints in ROLE_HINTS.items():
            if any(hint in combined_text for hint in hints):
                role_family = candidate_role
                role_confidence = 0.8
                break

        seniority = "unknown"
        seniority_confidence = 0.5
        for candidate_seniority, hints in SENIORITY_HINTS.items():
            if any(hint in combined_text for hint in hints):
                seniority = candidate_seniority
                seniority_confidence = 0.85
                break

        return (role_family, seniority, round((role_confidence + seniority_confidence) / 2, 2))


class HeuristicSummaryProvider:
    def summarize(
        self,
        job: JobPosting,
        classification: JobClassification | None,
        skills: Sequence[SkillEvidence],
        technologies: Sequence[TechnologyEvidence],
    ) -> str | None:
        skill_names = ", ".join(skill.name for skill in skills[:4]) or "general engineering skills"
        technology_names = ", ".join(technology.name for technology in technologies[:3])
        role_family = classification.role_family.replace("_", " ") if classification else "software engineering"
        seniority = classification.seniority.value if classification else "unknown"

        summary = f"{job.title} is a {seniority} {role_family} role emphasizing {skill_names}"
        if technology_names:
            summary += f" with technology focus on {technology_names}"
        return summary + "."


class NullSummaryProvider:
    def summarize(
        self,
        job: JobPosting,
        classification: JobClassification | None,
        skills: Sequence[SkillEvidence],
        technologies: Sequence[TechnologyEvidence],
    ) -> str | None:
        return None


class OverlapMatchScorer:
    def score(
        self,
        candidate: CandidateProfile,
        jobs: Sequence[JobPosting],
        enrichments: Sequence[JobEnrichment],
    ) -> list[MatchResult]:
        candidate_skills = {skill.name.lower() for skill in candidate.skills}
        candidate_summary_tokens = set(tokenize_words(candidate.summary))
        results: list[MatchResult] = []
        enrichment_by_job_id = {
            enrichment.job_id: enrichment
            for enrichment in enrichments
            if enrichment.job_id is not None
        }

        for job in jobs:
            enrichment = enrichment_by_job_id.get(job.job_id)
            if enrichment is None:
                continue
            required_skills = {skill.name.lower() for skill in enrichment.skills}
            if not required_skills:
                continue

            matches = sorted(candidate_skills & required_skills)
            missing = sorted(required_skills - candidate_skills)
            technology_bonus = 0.0
            technology_hits = sorted(
                technology.name
                for technology in enrichment.technologies
                if technology.name.lower() in candidate_summary_tokens
            )
            if technology_hits:
                technology_bonus = min(0.15, 0.05 * len(technology_hits))

            base_score = len(matches) / len(required_skills)
            score = min(1.0, base_score + technology_bonus)
            classification_text = (
                f"{enrichment.classification.seniority.value} {enrichment.classification.role_family.replace('_', ' ')}"
                if enrichment.classification
                else "unclassified role"
            )

            results.append(
                MatchResult(
                    job_id=job.job_id,
                    job_title=job.title,
                    source_name=job.source_name,
                    match_score=round(score, 3),
                    matching_skills=matches,
                    missing_skills=missing,
                    confidence=round(0.55 + min(0.35, 0.05 * len(required_skills)), 2),
                    reasons=[
                        MatchReason(
                            type="matching_skills",
                            message=f"Matched {len(matches)} required skills for this {classification_text}.",
                        ),
                        MatchReason(
                            type="missing_skills",
                            message=f"Missing {len(missing)} required skills.",
                        ),
                        MatchReason(
                            type="technology_alignment",
                            message=(
                                f"Candidate summary aligns with technologies: {', '.join(technology_hits)}."
                                if technology_hits
                                else "No direct technology alignment found in the candidate summary."
                            ),
                        ),
                    ],
                )
            )

        return sorted(results, key=lambda result: result.match_score, reverse=True)


def _extract_taxonomy_terms(
    text: str,
    *,
    taxonomy: dict[str, dict[str, object]],
) -> list[tuple[str, str | None, bool]]:
    normalized_text = normalize_whitespace(text)
    lowered_text = normalized_text.lower()
    extracted: list[tuple[str, str | None, bool]] = []

    for canonical_name, metadata in taxonomy.items():
        aliases = metadata["aliases"]
        matched_alias = next((alias for alias in aliases if alias in lowered_text), None)
        if matched_alias is None:
            continue
        evidence = _find_evidence_sentence(normalized_text, matched_alias)
        required = _is_requirement_sentence(evidence or "")
        extracted.append((canonical_name, evidence, required))

    return extracted


def _find_evidence_sentence(text: str, term: str) -> str | None:
    for sentence in _split_sentences(text):
        if term.lower() in sentence.lower():
            return sentence.strip()
    return None


def _split_sentences(text: str) -> list[str]:
    return [sentence for sentence in SENTENCE_RE.split(text) if sentence.strip()]


def _is_requirement_sentence(sentence: str) -> bool:
    lowered = sentence.lower()
    requirement_markers = ("required", "must", "need", "necessário", "obrigatório", "experience with")
    return any(marker in lowered for marker in requirement_markers)
