"""Enrichment outputs for jobs and candidates."""

from __future__ import annotations

from dataclasses import dataclass, field

from job_market.domain.jobs.models import Seniority


@dataclass(frozen=True)
class SkillEvidence:
    name: str
    evidence: str | None = None
    confidence: float = 1.0
    is_required: bool = True


@dataclass(frozen=True)
class TechnologyEvidence:
    name: str
    category: str
    evidence: str | None = None
    confidence: float = 1.0


@dataclass(frozen=True)
class JobClassification:
    role_family: str
    seniority: Seniority
    confidence: float = 1.0
    evidence: str | None = None


@dataclass(frozen=True)
class JobEnrichment:
    job_id: int | None = None
    skills: list[SkillEvidence] = field(default_factory=list)
    technologies: list[TechnologyEvidence] = field(default_factory=list)
    classification: JobClassification | None = None
    summary: str | None = None
