"""Query → retrieval → grounded generation (no classifier / orchestration / UI)."""

from __future__ import annotations

import logging
from typing import Any

from app.generation.answer import generate_from_hits
from app.retrieval.search import RetrievalHit, hits_to_payload, search_chunks

_logger = logging.getLogger(__name__)


def run_generation_answer_with_hits(query: str, top_k: int, hits: list[RetrievalHit]) -> dict[str, Any]:
    """Run generation using precomputed retrieval hits (evaluation / experiments)."""
    try:
        gen = generate_from_hits(query, hits)
    except Exception as exc:
        _logger.exception("Generation pipeline failed for query=%r: %s", query, exc)
        return {
            "query": (query or "").strip(),
            "answer": (
                "Не удалось сформировать ответ из найденных источников. "
                "Повторите запрос позже."
            ),
            "fallback": True,
            "fallback_reason": "generation_pipeline_error",
            "sources": [],
            "retrieval": {
                "top_k_requested": top_k,
                "hits_returned": len(hits),
                "results": hits_to_payload(hits),
            },
        }
    return {
        "query": gen["query"],
        "answer": gen["answer"],
        "fallback": gen["fallback"],
        "fallback_reason": gen["fallback_reason"],
        "sources": gen["sources"],
        "retrieval": {
            "top_k_requested": top_k,
            "hits_returned": len(hits),
            "results": hits_to_payload(hits),
        },
    }


def run_retrieval_generation_pipeline(query: str, top_k: int) -> dict[str, Any]:
    """
    End-to-end answer path: retrieval -> grounded generation -> response payload.
    """
    try:
        hits = search_chunks(query, top_k)
    except Exception as exc:
        _logger.exception("Retrieval failed for query=%r: %s", query, exc)
        return {
            "query": (query or "").strip(),
            "answer": (
                "Не удалось выполнить поиск по базе знаний. "
                "Повторите запрос позже."
            ),
            "fallback": True,
            "fallback_reason": "retrieval_error",
            "sources": [],
            "retrieval": {
                "top_k_requested": top_k,
                "hits_returned": 0,
                "results": [],
            },
        }
    return run_generation_answer_with_hits(query, top_k, hits)


def run_generation_answer(query: str, top_k: int) -> dict[str, Any]:
    """
    Backward-compatible public entrypoint for generation answer route.
    """
    return run_retrieval_generation_pipeline(query, top_k)
