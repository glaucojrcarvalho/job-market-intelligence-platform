"""Source-specific parser for the original GeekHunter notebook flow."""

from __future__ import annotations

from datetime import UTC, datetime

from bs4 import BeautifulSoup

from job_market.domain.jobs.models import RawJobRecord
from job_market.shared.text import normalize_whitespace


class GeekHunterHtmlAdapter:
    """Convert scraped GeekHunter job-card HTML into raw source records."""

    source_name = "geekhunter"

    def fetch(self) -> list[RawJobRecord]:
        raise NotImplementedError("Live fetching remains in the exploratory notebook for now.")

    def parse_job_card(self, job_html: str, *, source_url: str | None = None) -> RawJobRecord:
        soup = BeautifulSoup(job_html, "html.parser")
        title_link = soup.find("a")
        href = title_link.get("href") if title_link else None
        source_job_id = href if isinstance(href, str) else None

        return RawJobRecord(
            source_name=self.source_name,
            source_job_id=source_job_id,
            source_url=source_url,
            payload=normalize_whitespace(job_html),
            observed_at=datetime.now(UTC),
        )
