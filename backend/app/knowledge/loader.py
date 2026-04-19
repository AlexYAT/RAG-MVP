"""Load markdown documents from repository data/knowledge (ingest path only)."""

from pathlib import Path

_PREVIEW_LEN = 240


def _project_root() -> Path:
    # backend/app/knowledge/loader.py -> parents[3] == repository root
    return Path(__file__).resolve().parents[3]


def knowledge_root() -> Path:
    return _project_root() / "data" / "knowledge"


def load_markdown_documents() -> list[dict[str, str | int]]:
    """Read all *.md under knowledge root; return metadata and previews."""
    root = knowledge_root()
    if not root.is_dir():
        return []

    out: list[dict[str, str | int]] = []
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        category = rel.parts[0] if rel.parts else "unknown"
        text = path.read_text(encoding="utf-8")
        preview = text.strip()
        if len(preview) > _PREVIEW_LEN:
            preview = preview[:_PREVIEW_LEN] + "..."
        out.append(
            {
                "relative_path": rel.as_posix(),
                "category": category,
                "char_count": len(text),
                "preview": preview,
            }
        )
    return out


def ingest_summary() -> dict[str, object]:
    """Aggregated ingest check: counts, categories, per-document previews."""
    docs = load_markdown_documents()
    by_category: dict[str, int] = {}
    for d in docs:
        cat = str(d["category"])
        by_category[cat] = by_category.get(cat, 0) + 1
    return {
        "knowledge_root": str(knowledge_root()),
        "document_count": len(docs),
        "by_category": by_category,
        "documents": docs,
    }
