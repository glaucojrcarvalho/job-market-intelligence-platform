"""Candidate-related API schemas."""

from __future__ import annotations

from pydantic import BaseModel


class CandidateSkillInput(BaseModel):
    name: str
    proficiency: str | None = None


class CandidateProfileRequest(BaseModel):
    summary: str
    skills: list[CandidateSkillInput]
    location: str | None = None
    years_experience: float | None = None
