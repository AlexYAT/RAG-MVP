"""ASGI application entry: minimal API for bootstrap phase."""

from fastapi import FastAPI, Query

from app.generation.pipeline import run_generation_answer
from app.knowledge.loader import ingest_summary
from app.retrieval.search import get_retrieval_index, hits_to_payload, search_chunks

app = FastAPI(title="RAG MVP", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness check for local development."""
    return {"status": "ok"}


@app.get("/ingest/status")
def ingest_status() -> dict[str, object]:
    """Ingest baseline check: loaded synthetic documents metadata (no retrieval)."""
    return ingest_summary()


@app.get("/retrieval/search")
def retrieval_search(
    q: str = Query(..., min_length=1, description="Retrieval query (baseline TF–IDF)."),
    top_k: int = Query(5, ge=1, le=20, description="Max hits to return."),
) -> dict[str, object]:
    """Baseline retrieval check: top-k chunks with metadata (no generation)."""
    index = get_retrieval_index()
    hits = search_chunks(q, top_k)
    return {
        "query": q.strip(),
        "top_k_requested": top_k,
        "top_k_returned": len(hits),
        "chunk_count": index.chunk_count,
        "results": hits_to_payload(hits),
    }


@app.get("/generation/answer")
def generation_answer(
    q: str = Query(..., min_length=1, description="User query: retrieval → grounded answer."),
    top_k: int = Query(5, ge=1, le=20, description="Retrieval depth for generation context."),
) -> dict[str, object]:
    """Generation baseline: query → retrieval → extractive grounded answer (no orchestration)."""
    return run_generation_answer(q.strip(), top_k)
