"""Rule-based retrieval metrics: hit@k and simple text overlap."""

from __future__ import annotations

import re
from app.retrieval.search import RetrievalHit


def _norm_path(p: str) -> str:
    return p.replace("\\", "/").strip().lower()


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[\w\d]+", text.lower(), flags=re.UNICODE)


def hit_at_k(hits: list[RetrievalHit], expected_sources: list[str] | None, k: int) -> bool | None:
    """
    If expected_sources is non-empty: True if any top-k hit path matches an expected source.
    If empty: not applicable (None) — do not mix into labeled hit@k.
    """
    top = hits[: max(1, k)]
    if not top:
        return False
    if not expected_sources:
        return None
    exp_norm = {_norm_path(s) for s in expected_sources if s.strip()}
    for h in top:
        hp = _norm_path(h.relative_path)
        for e in exp_norm:
            if hp == e or hp.endswith(e) or e.endswith(hp):
                return True
    return False


def expected_answer_overlap(expected_answer: str | None, context_text: str) -> float | None:
    """Fraction of expected tokens that appear in context (0..1). None if no expected_answer."""
    if not expected_answer or not str(expected_answer).strip():
        return None
    exp_toks = set(_tokenize(expected_answer))
    if not exp_toks:
        return None
    ctx_toks = set(_tokenize(context_text))
    if not ctx_toks:
        return 0.0
    inter = len(exp_toks & ctx_toks)
    return inter / float(len(exp_toks))


def hits_context_text(hits: list[RetrievalHit], k: int) -> str:
    parts = [h.text for h in hits[:k]]
    return "\n".join(parts)
