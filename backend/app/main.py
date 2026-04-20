"""ASGI application entry with demo UI endpoints."""

from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# Keep system env precedence (override=False by default); .env is for local dev convenience.
load_dotenv()

from app.generation.pipeline import run_generation_answer
from app.knowledge.loader import ingest_summary
from app.orchestration.service import run_orchestration
from app.retrieval.search import get_retrieval_index, hits_to_payload, search_chunks
from app.scenarios.service import run_scenario_flow

app = FastAPI(title="RAG MVP", version="0.1.0")
_UI_DIR = Path(__file__).resolve().parent / "ui"
app.mount("/ui/static", StaticFiles(directory=_UI_DIR), name="ui-static")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness check for local development."""
    return {"status": "ok"}


@app.get("/ui")
def web_ui() -> FileResponse:
    """Demo-first web UI entrypoint."""
    return FileResponse(_UI_DIR / "index.html")


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


@app.get("/orchestration/query")
def orchestration_query(
    q: str = Query(..., min_length=1, description="Unified flow: query → retrieval → answer."),
    top_k: int = Query(5, ge=1, le=20, description="Retrieval depth for the pipeline."),
) -> dict[str, object]:
    """Orchestration layer: unified response contract; same pipeline as generation, stable extension point."""
    return run_orchestration(q.strip(), top_k)


@app.get("/scenarios/handle")
def scenario_handle(
    q: str = Query(..., min_length=1, description="Scenario flow over orchestration."),
    top_k: int = Query(5, ge=1, le=20, description="Retrieval depth for answer path."),
) -> dict[str, object]:
    """Scenario handling baseline: FAQ/selection/overview with one-step clarify for selection."""
    return run_scenario_flow(q.strip(), top_k)
