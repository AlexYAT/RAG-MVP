"""OpenAI embeddings helper for baseline LLM integration (T1 only)."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

_OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
_OPENAI_API_BASE_ENV = "OPENAI_API_BASE"
_OPENAI_EMBEDDING_MODEL_ENV = "OPENAI_EMBEDDING_MODEL"
_OPENAI_TIMEOUT_SEC_ENV = "OPENAI_TIMEOUT_SEC"


class OpenAIEmbeddingError(RuntimeError):
    """Raised when embedding request cannot be completed."""


def _require_api_key() -> str:
    api_key = os.getenv(_OPENAI_API_KEY_ENV, "").strip()
    if not api_key:
        raise OpenAIEmbeddingError(
            "OPENAI_API_KEY is not set. Provide OpenAI API key in environment variables."
        )
    return api_key


def _api_base() -> str:
    return os.getenv(_OPENAI_API_BASE_ENV, "https://api.openai.com/v1").rstrip("/")


def _embedding_model() -> str:
    return os.getenv(_OPENAI_EMBEDDING_MODEL_ENV, "text-embedding-3-small").strip() or "text-embedding-3-small"


def _timeout_sec() -> float:
    raw = os.getenv(_OPENAI_TIMEOUT_SEC_ENV, "60").strip()
    try:
        timeout = float(raw)
    except ValueError:
        raise OpenAIEmbeddingError(
            f"Invalid {_OPENAI_TIMEOUT_SEC_ENV}={raw!r}; expected numeric seconds."
        ) from None
    if timeout <= 0:
        raise OpenAIEmbeddingError(f"Invalid {_OPENAI_TIMEOUT_SEC_ENV}={raw!r}; must be > 0.")
    return timeout


def _request_embeddings(inputs: list[str]) -> list[list[float]]:
    if not inputs:
        raise OpenAIEmbeddingError("Embedding input list is empty.")
    if any(not (x or "").strip() for x in inputs):
        raise OpenAIEmbeddingError("Embedding inputs must be non-empty strings.")

    body = {
        "model": _embedding_model(),
        "input": inputs,
    }
    req = urllib.request.Request(
        f"{_api_base()}/embeddings",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {_require_api_key()}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=_timeout_sec()) as resp:
            payload: dict[str, Any] = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        details = ""
        try:
            details = exc.read().decode("utf-8", errors="replace")
        except Exception:
            details = str(exc)
        raise OpenAIEmbeddingError(
            f"OpenAI embeddings API request failed with HTTP {exc.code}: {details}"
        ) from exc
    except urllib.error.URLError as exc:
        raise OpenAIEmbeddingError(f"OpenAI embeddings API network error: {exc}") from exc
    except TimeoutError as exc:
        raise OpenAIEmbeddingError("OpenAI embeddings API request timed out.") from exc
    except json.JSONDecodeError as exc:
        raise OpenAIEmbeddingError("OpenAI embeddings API returned invalid JSON.") from exc

    data = payload.get("data")
    if not isinstance(data, list) or not data:
        raise OpenAIEmbeddingError("OpenAI embeddings API returned empty or invalid 'data'.")

    out: list[list[float]] = []
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            raise OpenAIEmbeddingError(f"OpenAI embeddings API data[{i}] has invalid shape.")
        emb = item.get("embedding")
        if not isinstance(emb, list) or not emb:
            raise OpenAIEmbeddingError(f"OpenAI embeddings API data[{i}] missing non-empty embedding.")
        try:
            out.append([float(v) for v in emb])
        except (TypeError, ValueError) as exc:
            raise OpenAIEmbeddingError(f"OpenAI embeddings API data[{i}] contains non-numeric values.") from exc
    return out


def get_text_embedding(text: str) -> list[float]:
    """Get single embedding vector for one input text."""
    t = (text or "").strip()
    if not t:
        raise OpenAIEmbeddingError("Embedding input text must be non-empty.")
    vecs = _request_embeddings([t])
    return vecs[0]


def get_text_embeddings(texts: list[str]) -> list[list[float]]:
    """Batch helper for later ingestion/indexing integration."""
    return _request_embeddings([(t or "").strip() for t in texts])


def _manual_probe(text: str) -> int:
    vec = get_text_embedding(text)
    print(f"Embedding dimension: {len(vec)}")
    print(f"First values: {vec[:8]}")
    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="OpenAI embeddings manual probe (T1).")
    parser.add_argument(
        "--text",
        default="Тестовая строка для проверки embeddings.",
        help="Input text for embedding request.",
    )
    args = parser.parse_args()
    raise SystemExit(_manual_probe(args.text))
