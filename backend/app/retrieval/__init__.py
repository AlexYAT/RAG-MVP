"""Baseline text retrieval (TF–IDF over synthetic knowledge chunks)."""

from app.retrieval.search import get_retrieval_index, search_chunks

__all__ = ["get_retrieval_index", "search_chunks"]
