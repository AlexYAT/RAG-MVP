"""Scenario handling layer on top of orchestration (demo-first baseline)."""

from __future__ import annotations

from typing import Any, Literal

from app.orchestration.service import run_orchestration

ScenarioName = Literal["faq", "selection", "overview"]

_OVERVIEW_HINTS = (
    "обзор",
    "overview",
    "направлен",
    "линейк",
    "каталог",
    "категори",
    "ассортимент",
)
_SELECTION_HINTS = (
    "подб",
    "выб",
    "рекоменд",
    "selection",
    "какое оборудование",
    "нужен",
    "нужна",
    "сравн",
)
_SELECTION_SPECIFICITY_HINTS = (
    "для ",
    "отделен",
    "кабинет",
    "монитор",
    "узи",
    "ультразв",
    "стерилиз",
    "реабил",
    "парам",
    "экран",
    "взросл",
    "дет",
    "кг",
    "ват",
    "бюджет",
)


def detect_scenario(query: str) -> ScenarioName:
    """Minimal rule-based classifier for three MVP scenarios."""
    q = (query or "").strip().lower()
    if any(h in q for h in _OVERVIEW_HINTS):
        return "overview"
    if any(h in q for h in _SELECTION_HINTS):
        return "selection"
    return "faq"


def _needs_selection_clarify(query: str) -> bool:
    q = (query or "").strip().lower()
    words = [w for w in q.replace("?", " ").replace(",", " ").split() if w]
    if len(words) < 3:
        return True
    return not any(h in q for h in _SELECTION_SPECIFICITY_HINTS)


def _clarify_selection_response(query: str, top_k: int) -> dict[str, Any]:
    return {
        "request": {"query": query.strip(), "top_k": top_k},
        "scenario": {"name": "selection", "classifier": "rules_v1"},
        "mode": "clarify",
        "answer": (
            "Для подбора оборудования недостаточно входных данных. "
            "Уточните направление, условия применения и 1-2 ключевых параметра "
            "(например: отделение/кабинет, портативность, базовые функции)."
        ),
        "fallback": True,
        "fallback_reason": "selection_needs_clarification",
        "sources": [],
        "retrieval_trace": {
            "executed": False,
            "reason": "selection_needs_clarification",
            "top_k_requested": top_k,
            "results": [],
        },
        "orchestration_trace": {
            "executed": False,
            "pipeline": ["retrieval", "generation"],
        },
    }


def run_scenario_flow(query: str, top_k: int) -> dict[str, Any]:
    """
    Scenario handling layer over existing orchestration.
    FAQ/overview: direct answer path.
    Selection: direct path or one-step clarify.
    """
    q = (query or "").strip()
    scenario = detect_scenario(q)
    if scenario == "selection" and _needs_selection_clarify(q):
        return _clarify_selection_response(q, top_k)

    orchestrated = run_orchestration(q, top_k)
    return {
        "request": orchestrated["request"],
        "scenario": {"name": scenario, "classifier": "rules_v1"},
        "mode": "answer",
        "answer": orchestrated["answer"],
        "fallback": orchestrated["fallback"],
        "fallback_reason": orchestrated["fallback_reason"],
        "sources": orchestrated["sources"],
        "retrieval_trace": orchestrated["retrieval_trace"],
        "orchestration_trace": orchestrated["orchestration"],
    }
