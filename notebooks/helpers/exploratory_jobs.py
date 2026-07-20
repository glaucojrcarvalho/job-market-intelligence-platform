"""Reusable helpers extracted from the exploratory job-market notebook.

These utilities preserve the notebook's current behavior while moving parsing
and text-cleaning logic into importable functions. They are intentionally
lightweight and transitional; the production package will be introduced later.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable, Sequence

import pandas as pd
from bs4 import BeautifulSoup


@dataclass(frozen=True)
class ExploratoryJobRecord:
    """Flat exploratory job record matching the notebook's current schema."""

    titulo: str
    local: str
    tipo_trabalho: str
    salario: str
    detalhes: str


def _clean_text(value: str) -> str:
    return value.replace("\n", "").replace("  ", "").strip()


def parse_geekhunter_job_html(job_html: str) -> ExploratoryJobRecord:
    """Parse one scraped job card into the notebook's tabular schema."""

    soup = BeautifulSoup(job_html, "html.parser")

    title_link = soup.find("a")
    location_tag = soup.find(class_="city")
    remote_tag = soup.find(class_="badge badge-secondary badge-remote")
    salary_tag = soup.find(class_="job-salary")
    description_tag = soup.find(class_="description")

    titulo = title_link.text.strip() if title_link else "Nao informado"
    local = (
        _clean_text(location_tag.text.replace("place", "").replace("Remoto", ""))
        if location_tag
        else "Nao informado"
    )
    tipo_trabalho = remote_tag.text.strip() if remote_tag else "Presencial"
    salario = (
        _clean_text(salary_tag.text).replace("R$", "").strip()
        if salary_tag
        else "Nao informado"
    )
    detalhes = _clean_text(description_tag.text) if description_tag else ""

    return ExploratoryJobRecord(
        titulo=titulo,
        local=local,
        tipo_trabalho=tipo_trabalho,
        salario=salario,
        detalhes=detalhes,
    )


def build_jobs_dataframe(job_cards_html: Iterable[str]) -> pd.DataFrame:
    """Convert scraped HTML snippets into the notebook's DataFrame layout."""

    records = [asdict(parse_geekhunter_job_html(job_html)) for job_html in job_cards_html]
    dataframe = pd.DataFrame.from_records(records)
    return dataframe.rename(
        columns={
            "titulo": "Titulo",
            "local": "Local",
            "tipo_trabalho": "Tipo_Trabalho",
            "salario": "Salario",
            "detalhes": "Detalhes",
        }
    )


def clean_description_tokens(
    description: str,
    *,
    stopwords_pt: Sequence[str],
    stopwords_en: Sequence[str],
    minimum_token_length: int = 4,
    tokenizer=None,
) -> list[str]:
    """Replicate the notebook's token cleanup with injectable dependencies."""

    tokenize = tokenizer or str.split
    stopwords_pt_set = set(stopwords_pt)
    stopwords_en_set = set(stopwords_en)

    tokens = tokenize(description)
    lowered_tokens = (
        token.lower()
        for token in tokens
        if token.isalpha() and len(token) >= minimum_token_length
    )

    return [
        token
        for token in lowered_tokens
        if token not in stopwords_pt_set and token not in stopwords_en_set
    ]


def summarize_salary_disclosure(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Compute the same salary disclosure grouping used by the notebook."""

    disclosure = dataframe["Salario"].apply(
        lambda salary: "Nao" if salary == "Nao informado" else "Sim"
    )
    return (
        disclosure.to_frame(name="Divulga")
        .groupby("Divulga")
        .size()
        .to_frame("Quantidade")
        .sort_values("Quantidade", ascending=False)
        .reset_index()
    )
