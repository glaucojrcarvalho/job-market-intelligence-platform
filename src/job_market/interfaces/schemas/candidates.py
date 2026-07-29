"""Candidate-related API schemas."""

from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints, field_validator

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

    @field_validator("skills")
    @classmethod
    def deduplicate_skills(
        cls,
        skills: list[CandidateSkillInput],
    ) -> list[CandidateSkillInput]:
        unique_skills: list[CandidateSkillInput] = []
        seen_names: set[str] = set()
        for skill in skills:
            normalized_name = skill.name.casefold()
            if normalized_name not in seen_names:
                seen_names.add(normalized_name)
                unique_skills.append(skill)
        return unique_skills
