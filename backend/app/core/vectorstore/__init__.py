"""VectorStore abstraction and adapters."""

from app.core.vectorstore.base import VectorDocument, VectorSearchResult, VectorStore
from app.core.vectorstore.chroma_store import ChromaVectorStore

__all__ = [
    "VectorDocument",
    "VectorSearchResult",
    "VectorStore",
    "ChromaVectorStore",
]
