"""Grounded, extractive generation from retrieval hits (no LLM, no external knowledge)."""

from __future__ import annotations

from typing import Any

from app.retrieval.search import RetrievalHit

# Baseline thresholds for char n-gram TF–IDF scores (see DOA-IMP-003).
_MIN_TOP_SCORE = 0.02
_MIN_CONTEXT_CHARS = 80
_MAX_FRAGMENTS = 3
_MAX_EXCERPT_CHARS = 650


def _trim(text: str, limit: int) -> str:
    t = text.strip()
    if len(t) <= limit:
        return t
    return t[: limit - 1].rstrip() + "…"


def hit_to_source(hit: RetrievalHit) -> dict[str, Any]:
    return {
        "relative_path": hit.relative_path,
        "category": hit.category,
        "chunk_index": hit.chunk_index,
        "chunk_id": hit.chunk_id,
        "score": round(hit.score, 6),
    }


def generate_from_hits(query: str, hits: list[RetrievalHit]) -> dict[str, Any]:
    """
    Build a grounded answer from retrieved chunks only.
    Returns answer text, fallback flags, and structured sources.
    """
    q = (query or "").strip()
    if not q:
        return {
            "query": query,
            "answer": "Пустой запрос: введите текст для поиска по базе знаний.",
            "fallback": True,
            "fallback_reason": "empty_query",
            "sources": [],
        }

    if not hits:
        return {
            "query": q,
            "answer": (
                "По запросу не найдено фрагментов в демонстрационной базе знаний "
                "(возможно, корпус пуст или индекс не построен)."
            ),
            "fallback": True,
            "fallback_reason": "no_hits",
            "sources": [],
        }

    top_score = max(h.score for h in hits)
    if top_score < _MIN_TOP_SCORE:
        return {
            "query": q,
            "answer": (
                "Найденные фрагменты имеют слишком низкую сходство с запросом для "
                "уверенного ответа в режиме демо. Уточните формулировку или используйте "
                "ключевые слова из карточек оборудования и FAQ."
            ),
            "fallback": True,
            "fallback_reason": "weak_retrieval_score",
            "sources": [hit_to_source(h) for h in hits[:_MAX_FRAGMENTS]],
        }

    top = hits[:_MAX_FRAGMENTS]
    total_chars = sum(len(h.text) for h in top)
    if total_chars < _MIN_CONTEXT_CHARS:
        return {
            "query": q,
            "answer": (
                "Недостаточно содержательного контекста в топовых фрагментах для "
                "связного ответа (слишком короткие совпадения)."
            ),
            "fallback": True,
            "fallback_reason": "insufficient_context",
            "sources": [hit_to_source(h) for h in top],
        }

    lines: list[str] = [
        "Ниже — ответ, собранный только из найденных фрагментов синтетической базы знаний (демо). "
        "Факты вне этих фрагментов не добавляются.",
        "",
        f"Запрос: {q}",
        "",
    ]
    for i, h in enumerate(top, start=1):
        excerpt = _trim(h.text, _MAX_EXCERPT_CHARS)
        src = h.relative_path
        lines.append(f"{i}. {src} (релевантность {h.score:.3f})")
        lines.append(excerpt)
        lines.append("")

    lines.append(
        "Источники перечислены в поле sources; при следующих фазах оркестрации "
        "их можно использовать для объяснения и трассировки."
    )

    return {
        "query": q,
        "answer": "\n".join(lines).strip(),
        "fallback": False,
        "fallback_reason": None,
        "sources": [hit_to_source(h) for h in top],
    }
