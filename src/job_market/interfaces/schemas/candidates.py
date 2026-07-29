"""Candidate-related API schemas."""

from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints

CandidateSummary = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=10, max_length=2000),
]
CandidateSkillName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=100),
]
SkillProficiency = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=50),
]
CandidateLocation = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=255),
]


class CandidateSkillInput(BaseModel):
    name: CandidateSkillName
    proficiency: SkillProficiency | None = None


class CandidateProfileRequest(BaseModel):
    summary: CandidateSummary
    skills: list[CandidateSkillInput] = Field(..., min_length=1, max_length=50)
    location: CandidateLocation | None = None
    years_experience: float | None = Field(default=None, ge=0, le=80)
