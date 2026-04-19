"""TF–IDF cosine baseline retrieval over chunk corpus (no LLM)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.knowledge.loader import load_markdown_full_documents
from app.retrieval.chunks import build_chunk_records

_MAX_TOP_K = 20


@dataclass(frozen=True)
class RetrievalHit:
    text: str
    score: float
    relative_path: str
    category: str
    chunk_index: int
    chunk_id: int


class TfidfChunkIndex:
    """Sparse vector space over chunk texts."""

    def __init__(self) -> None:
        docs = load_markdown_full_documents()
        self._records = build_chunk_records(docs)
        texts = [str(r["text"]) for r in self._records]
        # Character n-grams: robust baseline for Russian morphology without stemming.
        self._vectorizer = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(3, 5),
            min_df=1,
            max_df=1.0,
        )
        if not texts:
            self._matrix = None
        else:
            self._matrix = self._vectorizer.fit_transform(texts)

    @property
    def chunk_count(self) -> int:
        return len(self._records)

    def search(self, query: str, top_k: int) -> list[RetrievalHit]:
        if self._matrix is None or not self._records:
            return []
        k = max(1, min(top_k, _MAX_TOP_K, len(self._records)))
        q = (query or "").strip()
        if not q:
            return []
        q_vec = self._vectorizer.transform([q])
        sims = cosine_similarity(q_vec, self._matrix).ravel()
        top_idx = np.argsort(-sims)[:k]
        out: list[RetrievalHit] = []
        for i in top_idx:
            rec = self._records[int(i)]
            out.append(
                RetrievalHit(
                    text=str(rec["text"]),
                    score=float(sims[int(i)]),
                    relative_path=str(rec["relative_path"]),
                    category=str(rec["category"]),
                    chunk_index=int(rec["chunk_index"]),
                    chunk_id=int(i),
                )
            )
        return out


_index: TfidfChunkIndex | None = None


def get_retrieval_index() -> TfidfChunkIndex:
    global _index
    if _index is None:
        _index = TfidfChunkIndex()
    return _index


def search_chunks(query: str, top_k: int) -> list[RetrievalHit]:
    return get_retrieval_index().search(query, top_k)


def hits_to_payload(hits: list[RetrievalHit]) -> list[dict[str, object]]:
    return [
        {
            "text": h.text,
            "score": round(h.score, 6),
            "metadata": {
                "relative_path": h.relative_path,
                "category": h.category,
                "chunk_index": h.chunk_index,
                "chunk_id": h.chunk_id,
            },
        }
        for h in hits
    ]
