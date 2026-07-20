"""Analytics read models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MetricBucket:
    label: str
    value: int


@dataclass(frozen=True)
class SkillCooccurrence:
    left_skill: str
    right_skill: str
    frequency: int
