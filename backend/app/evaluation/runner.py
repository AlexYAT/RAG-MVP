"""Evaluation runner: dataset × retrieval modes → metrics + report."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal

from app.evaluation.dataset import load_dataset
from app.evaluation.llm_judge import judge_answer
from app.evaluation.retrieval_metrics import (
    expected_answer_overlap,
    hit_at_k,
    hits_context_text,
)
from app.generation.pipeline import run_generation_answer_with_hits
from app.retrieval.search import RetrievalHit, search_chunks_with_mode

RetrievalMode = Literal["keyword", "semantic"]


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def default_dataset_path() -> Path:
    return _project_root() / "data" / "evaluation" / "eval_dataset.json"


def default_report_path() -> Path:
    return _project_root() / "data" / "evaluation" / "reports" / "eval_report.json"


def _serialize_hit(h: RetrievalHit) -> dict[str, Any]:
    return {
        "text": h.text[:500] + ("…" if len(h.text) > 500 else ""),
        "score": h.score,
        "relative_path": h.relative_path,
        "category": h.category,
        "chunk_index": h.chunk_index,
    }


def _eval_one_row(
    row: dict[str, Any],
    mode: RetrievalMode,
    top_k: int,
) -> dict[str, Any]:
    q = row["question"]
    hits = search_chunks_with_mode(q, top_k, mode)
    gen = run_generation_answer_with_hits(q, top_k, hits)
    ctx = hits_context_text(hits, top_k)
    exp_src = list(row.get("expected_sources") or [])
    exp_ans = row.get("expected_answer")
    exp_ans_str = str(exp_ans).strip() if exp_ans else None

    h_k = hit_at_k(hits, exp_src if exp_src else None, top_k)
    overlap = expected_answer_overlap(exp_ans_str, ctx)
    judge = judge_answer(q, ctx, str(gen.get("answer", "")))

    return {
        "id": row["id"],
        "question": q,
        "mode": mode,
        "has_gold_sources": bool(exp_src),
        "hit_at_k": h_k,
        "expected_source_overlap": overlap,
        "judge": judge,
        "fallback": gen.get("fallback"),
        "hits_preview": [_serialize_hit(h) for h in hits[:5]],
    }


def _aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(rows)
    if n == 0:
        return {
            "n": 0,
            "avg_correctness": None,
            "hit_rate": None,
            "avg_expected_answer_overlap": None,
            "hallucination_rate": None,
        }
    labeled = [r for r in rows if r.get("has_gold_sources")]
    hit_vals = [bool(r["hit_at_k"]) for r in labeled if r.get("hit_at_k") is not None]
    corr = [float(r["judge"]["correctness"]) for r in rows if r["judge"].get("correctness") is not None]
    overlaps = [float(r["expected_source_overlap"]) for r in rows if r["expected_source_overlap"] is not None]
    hall_yes = sum(1 for r in rows if str(r["judge"].get("hallucination")).lower() == "yes")
    return {
        "n": n,
        "n_labeled_sources": len(labeled),
        "avg_correctness": round(sum(corr) / len(corr), 4) if corr else None,
        "hit_rate": round(sum(1 for x in hit_vals if x) / float(len(hit_vals)), 4) if hit_vals else None,
        "avg_expected_answer_overlap": round(sum(overlaps) / len(overlaps), 4) if overlaps else None,
        "hallucination_rate": round(hall_yes / float(n), 4),
    }


def run_evaluation(
    dataset_path: Path | None = None,
    top_k: int = 5,
    report_path: Path | None = None,
) -> dict[str, Any]:
    ds_path = dataset_path or default_dataset_path()
    out_path = report_path or default_report_path()
    items = load_dataset(ds_path)

    per_mode: dict[str, list[dict[str, Any]]] = {"keyword": [], "semantic": []}
    for mode in ("keyword", "semantic"):
        m: RetrievalMode = mode  # type: ignore[assignment]
        for row in items:
            per_mode[mode].append(_eval_one_row(row, m, top_k))

    kw_agg = _aggregate(per_mode["keyword"])
    sem_agg = _aggregate(per_mode["semantic"])

    def _delta(a: float | None, b: float | None) -> float | None:
        if a is None or b is None:
            return None
        return round(b - a, 4)

    report: dict[str, Any] = {
        "dataset_path": str(ds_path),
        "top_k": top_k,
        "summary": {
            "keyword": kw_agg,
            "semantic": sem_agg,
            "comparison_keyword_vs_semantic": {
                "avg_correctness_delta_semantic_minus_keyword": _delta(
                    kw_agg.get("avg_correctness"), sem_agg.get("avg_correctness")
                ),
                "hit_rate_delta_semantic_minus_keyword": _delta(kw_agg.get("hit_rate"), sem_agg.get("hit_rate")),
                "avg_expected_answer_overlap_delta": _delta(
                    kw_agg.get("avg_expected_answer_overlap"),
                    sem_agg.get("avg_expected_answer_overlap"),
                ),
            },
        },
        "per_item": per_mode,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report
