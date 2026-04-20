"""Minimal LLM-as-judge (OpenAI-compatible) with heuristic fallback."""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from typing import Any


_JUDGE_SYSTEM = (
    "You evaluate RAG answers. Reply with a single JSON object only, no markdown. "
    'Schema: {"correctness": number from 0 to 1, "hallucination": "yes" or "no"}. '
    "hallucination=yes if the answer states facts not supported by the context."
)


def _heuristic_judge(question: str, context: str, answer: str) -> dict[str, Any]:
    ctx = (context + "\n" + question).lower()
    ans = answer.lower()
    ans_words = set(re.findall(r"[\w\d]{4,}", ans, flags=re.UNICODE))
    ctx_words = set(re.findall(r"[\w\d]{4,}", ctx, flags=re.UNICODE))
    if not ans_words:
        correctness = 0.0
        hallucination = "no"
    else:
        supported = len(ans_words & ctx_words) / float(len(ans_words))
        correctness = round(min(1.0, max(0.0, supported)), 3)
        hallucination = "yes" if supported < 0.35 else "no"
    return {
        "correctness": correctness,
        "hallucination": hallucination,
        "judge_backend": "heuristic",
    }


def _openai_judge(question: str, context: str, answer: str) -> dict[str, Any] | None:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini"
    base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1").rstrip("/")
    url = f"{base}/chat/completions"
    user_content = (
        f"Question:\n{question}\n\nContext:\n{context[:12000]}\n\nAnswer:\n{answer[:8000]}"
    )
    body = {
        "model": model,
        "temperature": 0,
        "messages": [
            {"role": "system", "content": _JUDGE_SYSTEM},
            {"role": "user", "content": user_content},
        ],
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, TimeoutError):
        return None
    try:
        content = payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        return None
    content = (content or "").strip()
    m = re.search(r"\{[\s\S]*\}", content)
    if m:
        content = m.group(0)
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        return None
    corr = parsed.get("correctness")
    hall = str(parsed.get("hallucination", "")).lower()
    try:
        c = float(corr)
    except (TypeError, ValueError):
        c = 0.0
    c = max(0.0, min(1.0, c))
    h = "yes" if hall in ("yes", "true", "1") else "no"
    return {"correctness": round(c, 4), "hallucination": h, "judge_backend": "openai"}


def judge_answer(question: str, context: str, answer: str) -> dict[str, Any]:
    """Returns correctness (0..1), hallucination yes/no, and judge_backend."""
    llm = _openai_judge(question, context, answer)
    if llm is not None:
        return llm
    h = _heuristic_judge(question, context, answer)
    return h
