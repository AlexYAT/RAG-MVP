---
Project: RAG MVP
Doc type: implementation_snapshot
ID: DOA-IMP-011
Status: accepted
Date: 2026-04-20
Parent: DOA-OP-010
---

# Title

RAG evaluation baseline accepted

## 1. Summary

- Evaluation pipeline реализован и зафиксирован как baseline для последующих итераций.
- Сравнение **keyword** vs **semantic** доступно через явные режимы retrieval и агрегированный отчёт.
- **Hybrid evaluator** реализован: rule-based метрики по retrieval и оценка ответа (LLM judge с эвристическим fallback).
- Сгенерированный **JSON report** доступен по умолчанию в `data/evaluation/reports/eval_report.json` после запуска `python -m app.evaluation`.

## 2. Implemented Components

- **Dataset** — `data/evaluation/eval_dataset.json` (минимальный набор вопросов с опциональными gold-полями).
- **Loader** — `backend/app/evaluation/dataset.py` (JSON и CSV).
- **Runner** — `backend/app/evaluation/runner.py` (цикл по датасету, retrieval + generation по hits).
- **Retrieval mode switch** — `search_chunks_with_mode` в `backend/app/retrieval/search.py` (`keyword` / `semantic`).
- **Rule-based retrieval metrics** — `backend/app/evaluation/retrieval_metrics.py` (hit@k по expected sources, overlap по expected answer vs контекст).
- **LLM judge path with fallback** — `backend/app/evaluation/llm_judge.py` (OpenAI-compatible API при ключе, иначе эвристика).
- **Aggregation and JSON report** — сводка по режимам, сравнение keyword vs semantic, запись отчёта на диск.

Связанные точки входа: `python -m app.evaluation` (`backend/app/evaluation/__main__.py`), генерация по предвычисленным hits — `run_generation_answer_with_hits` в `backend/app/generation/pipeline.py`.

## 3. Verification

- `python -m app.evaluation --top-k 5` из каталога `backend` выполняется успешно.
- Отчёт генерируется (путь по умолчанию: `data/evaluation/reports/eval_report.json`).
- В stdout и в JSON доступен блок **summary** (метрики по keyword и semantic и сравнение).

## 4. Known Limitations

- Минимальный dataset (демо-объём, не покрытие продакшена).
- Без RAGAS и без расширенного набора метрик.
- Без UI для evaluation.
- Без интеграции в CI и без автоматизации по расписанию.
- LLM judge без `OPENAI_API_KEY` переходит на эвристику (корректность/галлюцинации приблизительные).

## 5. Note

- Этот snapshot **accepted** фиксирует каноническое описание принятого baseline по evaluation; для фиксации baseline используется **DOA-IMP-011**, draft **DOA-IMP-010** (`DOA-IMP-010_rag_evaluation_pipeline.md`) **не изменяется** (политика create-only).
- Draft **DOA-IMP-010** по-прежнему отражает историческое описание реализации на момент execution; accepted evidence для baseline — данный документ **DOA-IMP-011**.
