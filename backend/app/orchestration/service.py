"""Unified orchestration: query → retrieval → generation (reuses existing layers)."""

from __future__ import annotations

from typing import Any

from app.generation.pipeline import run_generation_answer
from app.retrieval.search import get_retrieval_index


def run_orchestration(query: str, top_k: int) -> dict[str, Any]:
    """
    Single orchestration entry: delegates to generation pipeline (retrieval then generation).
    Response contract is stable for scenario handling on top.
    """
    inner = run_generation_answer(query, top_k)
    retrieval = inner["retrieval"]
    index = get_retrieval_index()
    return {
        "request": {
            "query": inner["query"],
            "top_k": top_k,
        },
        "orchestration": {
            "pipeline": ["retrieval", "generation"],
            "version": 1,
        },
        "answer": inner["answer"],
        "fallback": inner["fallback"],
        "fallback_reason": inner["fallback_reason"],
        "sources": inner["sources"],
        "retrieval_trace": {
            "chunk_count": index.chunk_count,
            "top_k_requested": retrieval["top_k_requested"],
            "hits_returned": retrieval["hits_returned"],
            "results": retrieval["results"],
        },
    }
