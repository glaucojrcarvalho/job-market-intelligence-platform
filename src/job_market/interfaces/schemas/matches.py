"""Candidate match schemas."""

from __future__ import annotations

from pydantic import BaseModel

from job_market.domain.matching.models import MatchResult as DomainMatchResult


class MatchReason(BaseModel):
    type: str
    message: str


class MatchResult(BaseModel):
    match_id: int | None = None
    job_id: int | None = None
    job_title: str
    source_name: str
    match_score: float
    matching_skills: list[str]
    missing_skills: list[str]
    confidence: float
    reasons: list[MatchReason]

    @classmethod
    def from_domain(cls, result: DomainMatchResult) -> "MatchResult":
        return cls(
            match_id=result.match_id,
            job_id=result.job_id,
            job_title=result.job_title,
            source_name=result.source_name,
            match_score=result.match_score,
            matching_skills=result.matching_skills,
            missing_skills=result.missing_skills,
            confidence=result.confidence,
            reasons=[
                MatchReason(type=reason.type, message=reason.message)
                for reason in result.reasons
            ],
        )
