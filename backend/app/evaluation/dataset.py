"""Load evaluation items from JSON or CSV."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

QUERY_TYPES: frozenset[str] = frozenset({"lexical", "paraphrase", "noisy", "scenario"})
QUERY_TYPE_ORDER: tuple[str, ...] = ("lexical", "paraphrase", "noisy", "scenario")


def _parse_query_type(raw: object, *, where: str) -> str:
    if raw is None:
        raise ValueError(f"{where}: field 'type' is required")
    s = str(raw).strip().lower()
    if not s:
        raise ValueError(f"{where}: field 'type' must be non-empty")
    if s not in QUERY_TYPES:
        allowed = ", ".join(sorted(QUERY_TYPES))
        raise ValueError(f"{where}: unknown query type {raw!r}; allowed: {allowed}")
    return s


def _parse_sources_cell(raw: str | None) -> list[str]:
    if raw is None or str(raw).strip() == "":
        return []
    s = str(raw).strip()
    if s.startswith("["):
        try:
            v = json.loads(s)
            return [str(x).strip() for x in v if str(x).strip()]
        except json.JSONDecodeError:
            pass
    return [p.strip() for p in s.split(";") if p.strip()]


def load_dataset_json(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    items = data.get("items")
    if not isinstance(items, list):
        raise ValueError("JSON dataset must contain an 'items' array")
    out: list[dict[str, Any]] = []
    for i, row in enumerate(items):
        if not isinstance(row, dict):
            raise ValueError(f"items[{i}] must be an object")
        q = str(row.get("question", "")).strip()
        if not q:
            raise ValueError(f"items[{i}].question is required")
        qtype = _parse_query_type(row.get("type"), where=f"items[{i}]")
        exp_src = row.get("expected_sources")
        if exp_src is None:
            sources: list[str] = []
        elif isinstance(exp_src, list):
            sources = [str(x).strip() for x in exp_src if str(x).strip()]
        else:
            sources = _parse_sources_cell(str(exp_src))
        out.append(
            {
                "id": str(row.get("id", f"row_{i}")),
                "type": qtype,
                "question": q,
                "expected_answer": row.get("expected_answer"),
                "expected_sources": sources,
            }
        )
    return out


def load_dataset_csv(path: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or "question" not in reader.fieldnames:
            raise ValueError("CSV must have a 'question' column")
        if "type" not in reader.fieldnames:
            raise ValueError("CSV must have a 'type' column")
        for i, row in enumerate(reader):
            q = (row.get("question") or "").strip()
            if not q:
                continue
            qtype = _parse_query_type(row.get("type"), where=f"CSV row {i + 2}")
            ea = row.get("expected_answer")
            out.append(
                {
                    "id": (row.get("id") or "").strip() or f"row_{i}",
                    "type": qtype,
                    "question": q,
                    "expected_answer": ea.strip() if isinstance(ea, str) and ea.strip() else None,
                    "expected_sources": _parse_sources_cell(row.get("expected_sources")),
                }
            )
    return out


def load_dataset(path: Path) -> list[dict[str, Any]]:
    suf = path.suffix.lower()
    if suf == ".json":
        return load_dataset_json(path)
    if suf == ".csv":
        return load_dataset_csv(path)
    raise ValueError(f"Unsupported dataset format: {path}")
