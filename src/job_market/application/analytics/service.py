"""Analytics application service."""

from __future__ import annotations

from job_market.application.ports import AnalyticsReader
from job_market.domain.analytics.models import MetricBucket, SkillCooccurrence


class AnalyticsService:
    """Expose analytics reads through a stable service boundary."""

    def __init__(self, reader: AnalyticsReader) -> None:
        self._reader = reader

    def top_skills(self) -> list[MetricBucket]:
        return list(self._reader.top_skills())

    def top_technologies(self) -> list[MetricBucket]:
        return list(self._reader.top_technologies())

    def skill_cooccurrence(self) -> list[SkillCooccurrence]:
        return list(self._reader.skill_cooccurrence())
