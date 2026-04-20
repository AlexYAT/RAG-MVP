"""ChromaDB-backed VectorStore implementation."""

from __future__ import annotations

from typing import Any

import chromadb

from app.core.vectorstore.base import VectorDocument, VectorSearchResult, VectorStore


def _to_score(distance: float) -> float:
    # Chroma cosine distance: 0 is best; convert to larger-is-better score.
    return max(0.0, 1.0 - float(distance))


class ChromaVectorStore(VectorStore):
    """Persistent Chroma adapter for VectorStore abstraction."""

    def __init__(self, persist_path: str, collection_name: str) -> None:
        self._client = chromadb.PersistentClient(path=persist_path)
        self._collection = self._client.get_or_create_collection(name=collection_name)

    def upsert(self, documents: list[VectorDocument]) -> None:
        if not documents:
            return
        ids = [d["id"] for d in documents]
        embeddings = [d["embedding"] for d in documents]
        docs = [d["text"] for d in documents]
        metadatas = [d["metadata"] for d in documents]
        self._collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=docs,
            metadatas=metadatas,
        )

    def query(self, query_embedding: list[float], top_k: int) -> list[VectorSearchResult]:
        res = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=max(1, int(top_k)),
        )
        ids = res.get("ids", [[]])[0]
        docs = res.get("documents", [[]])[0]
        metadatas = res.get("metadatas", [[]])[0]
        distances = res.get("distances", [[]])[0]

        out: list[VectorSearchResult] = []
        for i, item_id in enumerate(ids):
            metadata: dict[str, Any] = metadatas[i] if i < len(metadatas) and metadatas[i] else {}
            distance = distances[i] if i < len(distances) else 1.0
            out.append(
                {
                    "id": str(item_id),
                    "text": str(docs[i]) if i < len(docs) else "",
                    "score": _to_score(float(distance)),
                    "metadata": metadata,
                }
            )
        return out

    def reset(self) -> None:
        self._client.delete_collection(self._collection.name)
        self._collection = self._client.get_or_create_collection(name=self._collection.name)
