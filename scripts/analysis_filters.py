"""Canonical sample filters for the replication archive.

The Note's headline empirical claims use T2-disjunctive as the disability
population. T2-narrow remains available as a robustness filter.
"""
from __future__ import annotations

from datetime import date
from typing import Any

P1_START = date(2022, 1, 1)
P2_START = date(2024, 6, 28)
P3_START = date(2025, 2, 5)
P3_END = date(2026, 7, 1)

DECIDED_OUTCOMES = {"PLAINTIFF_WIN", "DEFENDANT_WIN", "MIXED"}
NON_DECISIVE_OUTCOMES = {"PROCEDURAL", "SETTLEMENT", "UNDETERMINED"}


def protected_classes(record: dict[str, Any]) -> list[str]:
    value = record.get("protected_classes") or []
    if isinstance(value, str):
        value = [value]
    return [str(item).strip().lower() for item in value if str(item).strip()]


def is_screened_in(record: dict[str, Any]) -> bool:
    return record.get("screening_result") != "NO" and bool(record.get("case_name"))


def is_t2_canonical(record: dict[str, Any]) -> bool:
    if not is_screened_in(record):
        return False
    return (
        bool(record.get("disability_alleged"))
        or bool(record.get("is_ra_case"))
        or "disability" in protected_classes(record)
    )


def is_t2_narrow(record: dict[str, Any]) -> bool:
    return is_screened_in(record) and "disability" in protected_classes(record)


def parse_opinion_date(raw: Any) -> date | None:
    if not raw:
        return None
    try:
        return date.fromisoformat(str(raw)[:10])
    except ValueError:
        return None


def assign_period(record: dict[str, Any]) -> str | None:
    opinion_date = parse_opinion_date(record.get("date_filed"))
    if opinion_date is None or opinion_date < P1_START:
        return None
    if opinion_date < P2_START:
        return "P1"
    if opinion_date < P3_START:
        return "P2"
    if opinion_date > P3_END:
        return None
    return "P3"


def is_decided(record: dict[str, Any]) -> bool:
    return record.get("outcome") in DECIDED_OUTCOMES


def is_non_decisive(record: dict[str, Any]) -> bool:
    return record.get("outcome") in NON_DECISIVE_OUTCOMES or record.get("outcome") is None
