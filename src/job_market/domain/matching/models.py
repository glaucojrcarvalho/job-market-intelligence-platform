"""Domain models for candidate-job matching."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class MatchReason:
    type: str
    message: str


@dataclass(frozen=True)
class MatchResult:
    job_title: str
    source_name: str
    match_score: float
    matching_skills: list[str] = field(default_factory=list)
    missing_skills: list[str] = field(default_factory=list)
    confidence: float = 0.0
    reasons: list[MatchReason] = field(default_factory=list)
    match_id: int | None = None
    job_id: int | None = None
