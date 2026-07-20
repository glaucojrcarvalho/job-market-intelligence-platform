"""Text utilities shared across normalization and enrichment."""

from __future__ import annotations

import re
from collections.abc import Iterable

WHITESPACE_RE = re.compile(r"\s+")
WORD_RE = re.compile(r"[A-Za-zÀ-ÿ0-9_+#.-]+")


def normalize_whitespace(value: str) -> str:
    return WHITESPACE_RE.sub(" ", value).strip()


def tokenize_words(value: str) -> list[str]:
    return [token.lower() for token in WORD_RE.findall(value)]


def find_present_terms(value: str, vocabulary: Iterable[str]) -> list[str]:
    token_set = set(tokenize_words(value))
    return sorted(term for term in vocabulary if term.lower() in token_set)
