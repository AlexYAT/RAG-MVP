"""Split ingested markdown into retrieval-ready chunks (no embeddings)."""

from __future__ import annotations

import re

_MAX_CHUNK_CHARS = 900
_MIN_CHUNK_CHARS = 20


def _split_oversized(paragraph: str) -> list[str]:
    paragraph = paragraph.strip()
    if len(paragraph) <= _MAX_CHUNK_CHARS:
        return [paragraph] if paragraph else []
    chunks: list[str] = []
    start = 0
    while start < len(paragraph):
        piece = paragraph[start : start + _MAX_CHUNK_CHARS]
        chunks.append(piece.strip())
        start += _MAX_CHUNK_CHARS
    return [c for c in chunks if len(c) >= _MIN_CHUNK_CHARS]


def chunk_markdown_text(text: str) -> list[str]:
    """Split document text into paragraph-based chunks; oversized paragraphs are sliced."""
    normalized = text.replace("\r\n", "\n").strip()
    if not normalized:
        return []
    parts = re.split(r"\n\s*\n+", normalized)
    chunks: list[str] = []
    for raw in parts:
        for piece in _split_oversized(raw):
            if len(piece) >= _MIN_CHUNK_CHARS:
                chunks.append(piece)
    return chunks


def build_chunk_records(
    documents: list[dict[str, str]],
) -> list[dict[str, str | int]]:
    """Flatten documents to chunk records with stable chunk_index per file."""
    records: list[dict[str, str | int]] = []
    for doc in documents:
        rel = doc["relative_path"]
        cat = doc["category"]
        for idx, chunk_text in enumerate(chunk_markdown_text(doc["text"])):
            records.append(
                {
                    "relative_path": rel,
                    "category": cat,
                    "chunk_index": idx,
                    "text": chunk_text,
                }
            )
    return records
