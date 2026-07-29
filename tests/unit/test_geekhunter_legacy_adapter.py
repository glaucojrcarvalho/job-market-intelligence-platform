from __future__ import annotations

from datetime import UTC

import pytest

from job_market.infrastructure.ingestion.geekhunter import GeekHunterHtmlAdapter


def test_legacy_adapter_does_not_fetch_live_geekhunter_data() -> None:
    adapter = GeekHunterHtmlAdapter()

    with pytest.raises(NotImplementedError, match="unsupported"):
        adapter.fetch()


def test_legacy_adapter_preserves_source_provenance_for_supplied_html() -> None:
    adapter = GeekHunterHtmlAdapter()
    html = '<article class="job"><a href="/vagas/backend-123">Backend Engineer</a></article>'

    before_parse = adapter.parse_job_card(html).observed_at
    record = adapter.parse_job_card(html, source_url="https://example.invalid/historical-fixture")

    assert record.source_name == "geekhunter"
    assert record.source_job_id == "/vagas/backend-123"
    assert record.source_url == "https://example.invalid/historical-fixture"
    assert record.payload == html
    assert record.observed_at.tzinfo == UTC
    assert record.observed_at >= before_parse
