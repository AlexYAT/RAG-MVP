"""Grounded LLM generation from retrieval hits."""

from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.request
from typing import Any

from app.retrieval.search import RetrievalHit

_MIN_TOP_SCORE = 0.02
_MIN_CONTEXT_CHARS = 80
_MAX_FRAGMENTS = 3
_MAX_EXCERPT_CHARS = 650
_OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
_OPENAI_API_BASE_ENV = "OPENAI_API_BASE"
_OPENAI_TIMEOUT_SEC_ENV = "OPENAI_TIMEOUT_SEC"
_OPENAI_GENERATION_MODEL_ENV = "OPENAI_GENERATION_MODEL"
_DEFAULT_GENERATION_MODEL = "gpt-4o-mini"
_SAFE_LLM_ERROR_MESSAGE = (
    "Не удалось сформировать ответ на основе найденного контекста. "
    "Повторите запрос позже или уточните формулировку."
)
_SYSTEM_PROMPT = (
    "Ты ассистент по подбору медицинского оборудования. "
    "Отвечай только на основе переданного контекста. "
    "Если данных недостаточно, прямо скажи, что в контексте нет информации. "
    "Не придумывай факты вне контекста. Ответ дай кратко и по делу."
)
_logger = logging.getLogger(__name__)


def _trim(text: str, limit: int) -> str:
    t = text.strip()
    if len(t) <= limit:
        return t
    return t[: limit - 1].rstrip() + "…"


class OpenAIGenerationError(RuntimeError):
    """Raised when OpenAI generation cannot produce a valid answer."""


def hit_to_source(hit: RetrievalHit) -> dict[str, Any]:
    return {
        "relative_path": hit.relative_path,
        "category": hit.category,
        "chunk_index": hit.chunk_index,
        "chunk_id": hit.chunk_id,
        "score": round(hit.score, 6),
    }


def _api_key() -> str:
    key = os.getenv(_OPENAI_API_KEY_ENV, "").strip()
    if not key:
        raise OpenAIGenerationError("OPENAI_API_KEY is not set for LLM generation.")
    return key


def _api_base() -> str:
    return os.getenv(_OPENAI_API_BASE_ENV, "https://api.openai.com/v1").rstrip("/")


def _generation_model() -> str:
    return os.getenv(_OPENAI_GENERATION_MODEL_ENV, _DEFAULT_GENERATION_MODEL).strip() or _DEFAULT_GENERATION_MODEL


def _timeout_sec() -> float:
    raw = os.getenv(_OPENAI_TIMEOUT_SEC_ENV, "60").strip()
    try:
        timeout = float(raw)
    except ValueError:
        raise OpenAIGenerationError(
            f"Invalid {_OPENAI_TIMEOUT_SEC_ENV}={raw!r}; expected numeric seconds."
        ) from None
    if timeout <= 0:
        raise OpenAIGenerationError(f"Invalid {_OPENAI_TIMEOUT_SEC_ENV}={raw!r}; must be > 0.")
    return timeout


def _build_context(hits: list[RetrievalHit]) -> str:
    lines: list[str] = []
    for i, h in enumerate(hits[:_MAX_FRAGMENTS], start=1):
        lines.append(f"[SOURCE {i}] {h.relative_path} (score={h.score:.3f})")
        lines.append(_trim(h.text, _MAX_EXCERPT_CHARS))
        lines.append("")
    return "\n".join(lines).strip()


def _grounded_llm_answer(query: str, context: str) -> str:
    body = {
        "model": _generation_model(),
        "temperature": 0,
        "messages": [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Вопрос пользователя:\n{query}\n\n"
                    f"Контекст из retrieval:\n{context}\n\n"
                    "Сформируй ответ только на основе этого контекста."
                ),
            },
        ],
    }
    req = urllib.request.Request(
        f"{_api_base()}/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {_api_key()}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=_timeout_sec()) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        details = ""
        try:
            details = exc.read().decode("utf-8", errors="replace")
        except Exception:
            details = str(exc)
        raise OpenAIGenerationError(
            f"OpenAI generation request failed with HTTP {exc.code}: {details}"
        ) from exc
    except urllib.error.URLError as exc:
        raise OpenAIGenerationError(f"OpenAI generation network error: {exc}") from exc
    except TimeoutError as exc:
        raise OpenAIGenerationError("OpenAI generation request timed out.") from exc
    except json.JSONDecodeError as exc:
        raise OpenAIGenerationError("OpenAI generation returned invalid JSON.") from exc

    try:
        content = str(payload["choices"][0]["message"]["content"]).strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise OpenAIGenerationError("OpenAI generation returned unexpected response shape.") from exc
    if not content:
        raise OpenAIGenerationError("OpenAI generation returned empty answer.")
    return content


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

    context = _build_context(top)
    try:
        answer = _grounded_llm_answer(q, context)
    except OpenAIGenerationError as exc:
        _logger.exception("LLM generation failed for query=%r: %s", q, exc)
        return {
            "query": q,
            "answer": _SAFE_LLM_ERROR_MESSAGE,
            "fallback": True,
            "fallback_reason": "llm_generation_error",
            "sources": [hit_to_source(h) for h in top],
        }
    except Exception as exc:
        _logger.exception("Unexpected generation error for query=%r: %s", q, exc)
        return {
            "query": q,
            "answer": _SAFE_LLM_ERROR_MESSAGE,
            "fallback": True,
            "fallback_reason": "generation_internal_error",
            "sources": [hit_to_source(h) for h in top],
        }

    return {
        "query": q,
        "answer": answer,
        "fallback": False,
        "fallback_reason": None,
        "sources": [hit_to_source(h) for h in top],
    }
