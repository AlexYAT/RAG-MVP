"""Semantic retrieval via VectorStore (Chroma) with TF-IDF fallback."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Literal

import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.core.vectorstore.base import VectorDocument, VectorStore
from app.core.vectorstore.chroma_store import ChromaVectorStore
from app.knowledge.loader import load_markdown_full_documents
from app.retrieval.chunks import build_chunk_records

_MAX_TOP_K = 20
_CHROMA_PATH_ENV = "CHROMA_PATH"
_COLLECTION_ENV = "COLLECTION_NAME"


def _project_root() -> Path:
    # backend/app/retrieval/search.py -> parents[3] == repository root
    return Path(__file__).resolve().parents[3]


def _default_chroma_path() -> str:
    return str(_project_root() / ".chroma")


def _collection_name() -> str:
    return os.getenv(_COLLECTION_ENV, "rag_mvp_chunks")


@dataclass(frozen=True)
class RetrievalHit:
    text: str
    score: float
    relative_path: str
    category: str
    chunk_index: int
    chunk_id: int


class TfidfKeywordIndex:
    """Legacy keyword fallback index."""

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


class SemanticVectorIndex:
    """Primary semantic index backed by VectorStore abstraction."""

    def __init__(self, store: VectorStore) -> None:
        self._store = store
        self._records = build_chunk_records(load_markdown_full_documents())
        self._embedder = HashingVectorizer(
            analyzer="char_wb",
            ngram_range=(3, 5),
            n_features=512,
            alternate_sign=False,
            norm="l2",
        )
        self._upsert_records()

    @property
    def chunk_count(self) -> int:
        return len(self._records)

    def _embed_text(self, text: str) -> list[float]:
        vec = self._embedder.transform([text]).toarray()[0]
        return [float(v) for v in vec]

    @staticmethod
    def _to_chunk_id(relative_path: str, chunk_index: int) -> str:
        return f"{relative_path}::chunk::{chunk_index}"

    def _upsert_records(self) -> None:
        docs: list[VectorDocument] = []
        for rec in self._records:
            relative_path = str(rec["relative_path"])
            category = str(rec["category"])
            chunk_index = int(rec["chunk_index"])
            text = str(rec["text"])
            docs.append(
                {
                    "id": self._to_chunk_id(relative_path, chunk_index),
                    "embedding": self._embed_text(text),
                    "text": text,
                    "metadata": {
                        "relative_path": relative_path,
                        "category": category,
                        "chunk_index": chunk_index,
                        "source": relative_path,
                    },
                }
            )
        self._store.upsert(docs)

    def search(self, query: str, top_k: int) -> list[RetrievalHit]:
        q = (query or "").strip()
        if not q:
            return []
        k = max(1, min(top_k, _MAX_TOP_K))
        res = self._store.query(self._embed_text(q), k)
        out: list[RetrievalHit] = []
        for i, item in enumerate(res):
            metadata = item.get("metadata", {})
            out.append(
                RetrievalHit(
                    text=str(item.get("text", "")),
                    score=float(item.get("score", 0.0)),
                    relative_path=str(metadata.get("relative_path", "")),
                    category=str(metadata.get("category", "unknown")),
                    chunk_index=int(metadata.get("chunk_index", i)),
                    chunk_id=i,
                )
            )
        return out


_semantic_index: SemanticVectorIndex | None = None
_keyword_index: TfidfKeywordIndex | None = None


def _get_keyword_index() -> TfidfKeywordIndex:
    global _keyword_index
    if _keyword_index is None:
        _keyword_index = TfidfKeywordIndex()
    return _keyword_index


def get_retrieval_index() -> SemanticVectorIndex:
    global _semantic_index
    if _semantic_index is None:
        _semantic_index = SemanticVectorIndex(
            store=ChromaVectorStore(
                persist_path=os.getenv(_CHROMA_PATH_ENV, _default_chroma_path()),
                collection_name=_collection_name(),
            )
        )
    return _semantic_index


RetrievalMode = Literal["keyword", "semantic"]


def search_chunks_with_mode(query: str, top_k: int, mode: RetrievalMode) -> list[RetrievalHit]:
    """
    Explicit retrieval mode for evaluation (no silent fallback in semantic mode).
    """
    m = (mode or "semantic").lower()
    if m == "keyword":
        return _get_keyword_index().search(query, top_k)
    if m == "semantic":
        try:
            return get_retrieval_index().search(query, top_k)
        except Exception:
            return []
    raise ValueError(f"Unknown retrieval mode: {mode!r}")


def search_chunks(query: str, top_k: int) -> list[RetrievalHit]:
    try:
        hits = get_retrieval_index().search(query, top_k)
        if hits:
            return hits
    except Exception:
        # Keep existing MVP behavior if semantic path is not available.
        pass
    return _get_keyword_index().search(query, top_k)


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
