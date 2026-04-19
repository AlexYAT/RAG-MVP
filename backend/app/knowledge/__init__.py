"""Synthetic knowledge base loading (ingest baseline, no retrieval)."""

from app.knowledge.loader import ingest_summary, load_markdown_documents

__all__ = ["ingest_summary", "load_markdown_documents"]
