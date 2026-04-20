"""Vector storage abstraction for semantic retrieval."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, TypedDict


class VectorDocument(TypedDict):
    """Single vectorized chunk payload."""

    id: str
    embedding: list[float]
    text: str
    metadata: dict[str, Any]


class VectorSearchResult(TypedDict):
    """Single retrieval result from vector storage."""

    id: str
    score: float
    text: str
    metadata: dict[str, Any]


class VectorStore(ABC):
    """Minimal VectorStore interface for MVP semantic retrieval."""

    @abstractmethod
    def upsert(self, documents: list[VectorDocument]) -> None:
        """Insert/update vectorized documents."""

    @abstractmethod
    def query(self, query_embedding: list[float], top_k: int) -> list[VectorSearchResult]:
        """Fetch top-k nearest documents for query embedding."""

    def reset(self) -> None:
        """Optional clear/reset hook."""
