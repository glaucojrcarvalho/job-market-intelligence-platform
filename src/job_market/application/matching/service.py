"""Candidate matching service."""

from __future__ import annotations

from job_market.application.ports import (
    EnrichmentRepository,
    JobRepository,
    MatchRepository,
    MatchScorer,
)
from job_market.domain.candidates.models import CandidateProfile
from job_market.domain.matching.models import MatchResult


class CandidateMatchingService:
    """Score candidate-job matches against stored jobs and enrichments."""

    def __init__(
        self,
        *,
        job_repository: JobRepository,
        enrichment_repository: EnrichmentRepository,
        match_repository: MatchRepository,
        scorer: MatchScorer,
    ) -> None:
        self._job_repository = job_repository
        self._enrichment_repository = enrichment_repository
        self._match_repository = match_repository
        self._scorer = scorer

    def match(self, candidate: CandidateProfile) -> list[MatchResult]:
        jobs = self._job_repository.list_all()
        enrichments = self._enrichment_repository.list_all()
        results = self._scorer.score(candidate, jobs, enrichments)
        return [self._match_repository.add(result) for result in results]
