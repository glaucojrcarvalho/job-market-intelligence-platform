"""Analytics response schemas."""

from __future__ import annotations

from pydantic import BaseModel


class MetricBucketResponse(BaseModel):
    label: str
    value: int


class SkillCooccurrenceResponse(BaseModel):
    left_skill: str
    right_skill: str
    frequency: int
