---
Project: RAG MVP
Doc type: implementation_snapshot
ID: DOA-IMP-010
Status: draft
Date: 2026-04-20
Parent: DOA-OP-010
---

# Title

RAG evaluation pipeline with hybrid evaluator

## 1. Scope

Реализация согласно DOA-OP-010: минимальный dataset, loader (JSON/CSV), runner, режимы keyword/semantic, rule-based метрики (hit@k, overlap по expected_answer), LLM judge с эвристическим fallback, агрегация и JSON report.

## 2. What was implemented

- `data/evaluation/eval_dataset.json` — 8 вопросов с опциональными `expected_answer` / `expected_sources`.
- `app/evaluation/` — dataset loader, retrieval metrics, judge (`OPENAI_API_KEY` опционально), runner, CLI `python -m app.evaluation`.
- `search_chunks_with_mode` — явные режимы `keyword` и `semantic` (semantic без silent fallback на keyword).
- `run_generation_answer_with_hits` — генерация по заранее полученным hits.
- Отчёт: `data/evaluation/reports/eval_report.json` + summary (avg correctness, hit rate на размеченных источниках, overlap, сравнение keyword vs semantic).

## 3. Files

- `data/evaluation/eval_dataset.json`
- `data/evaluation/reports/eval_report.json` (артефакт прогона)
- `backend/app/evaluation/*`
- `backend/app/retrieval/search.py`
- `backend/app/generation/pipeline.py`
- `docs/implementation_snapshot/DOA-IMP-010_rag_evaluation_pipeline.md`

## 4. Verification

- Из каталога `backend`: `python -m app.evaluation --top-k 5` завершился успешно, summary выведен в stdout, отчёт записан в `data/evaluation/reports/eval_report.json`.
