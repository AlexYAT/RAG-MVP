"""Query → retrieval → grounded generation (no classifier / orchestration / UI)."""

from __future__ import annotations

from typing import Any

from app.generation.answer import generate_from_hits
from app.retrieval.search import hits_to_payload, search_chunks


def run_generation_answer(query: str, top_k: int) -> dict[str, Any]:
    """
    Service check: run retrieval baseline, then generation layer.
    """
    hits = search_chunks(query, top_k)
    gen = generate_from_hits(query, hits)
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
