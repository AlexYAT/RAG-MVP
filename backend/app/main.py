"""ASGI application entry: minimal API for bootstrap phase."""

from fastapi import FastAPI

from app.knowledge.loader import ingest_summary

app = FastAPI(title="RAG MVP", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness check for local development."""
    return {"status": "ok"}


@app.get("/ingest/status")
def ingest_status() -> dict[str, object]:
    """Ingest baseline check: loaded synthetic documents metadata (no retrieval)."""
    return ingest_summary()
