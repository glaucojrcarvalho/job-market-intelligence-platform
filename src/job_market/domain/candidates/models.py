"""Candidate-related domain models."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CandidateSkill:
    name: str
    proficiency: str | None = None
    evidence: str | None = None


@dataclass(frozen=True)
class CandidateProfile:
    profile_id: str | None
    summary: str
    skills: list[CandidateSkill] = field(default_factory=list)
    location: str | None = None
    years_experience: float | None = None
