"""ASGI application entry: minimal API for bootstrap phase."""

from fastapi import FastAPI

app = FastAPI(title="RAG MVP", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness check for local development."""
    return {"status": "ok"}
