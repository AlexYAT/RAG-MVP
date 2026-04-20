---
Project: RAG MVP
Doc type: implementation_snapshot
ID: DOA-IMP-014
Status: accepted
Date: 2026-04-20
Parent: DOA-OP-012
---

# Title

LLM baseline pipeline enabled for RAG MVP

## 1. Summary

В рамках `DOA-OP-012` завершена интеграция LLM baseline: добавлены embeddings и grounded generation через единый provider, retrieval стал semantic-aware, а ответный путь собран в рабочий end-to-end pipeline.

## 2. Scope of implementation

Реализовано по шагам `T1–T5`:

- **T1 — Embeddings integration:** добавлен рабочий OpenAI embeddings helper (single/batch), env-конфигурация и явные ошибки при отсутствии ключа/ошибках API.
- **T2 — Retrieval update:** semantic retrieval использует embeddings helper; keyword path сохранён как отдельный режим/контролируемый fallback.
- **T3 — Generation integration:** generation path переведён на grounded LLM-ответ с контекстом из retrieval hits и явной обработкой ошибок generation.
- **T4 — Pipeline integration:** retrieval и generation соединены в единую цепочку ответа (`query -> retrieval -> generation -> response`) без переписывания orchestration.
- **T5 — Smoke validation:** выполнена ручная проверка основных сценариев и fallback-поведения.

## 3. Files changed

Файлы, затронутые в цикле `DOA-OP-012`:

- `backend/app/core/llm/openai_embeddings.py`
- `backend/app/core/llm/__init__.py`
- `backend/app/retrieval/search.py`
- `backend/app/generation/answer.py`
- `backend/app/generation/pipeline.py`
- `backend/app/main.py`
- `backend/.env.example`

## 4. Validation

Smoke validation выполнена вручную на end-to-end контуре:

- **FAQ:** запросы по гарантийным/справочным вопросам возвращают grounded ответ на основе retrieval-контекста.
- **Selection:** сценарий выбора проходит через clarify step и затем формирует ответ по найденным источникам.
- **Overview:** обзорные запросы обрабатываются по тому же pipeline и возвращают ответ с источниками.

Fallback-поведение подтверждено:

- при нехватке контекста или слабом retrieval-сигнале возвращается контролируемый fallback;
- при проблемах LLM generation (например, отсутствует `OPENAI_API_KEY`) возвращается явная причина (`fallback_reason`) без фальшивого success.

## 5. Resulting system state

После завершения `DOA-OP-012` система поддерживает:

- retrieval в двух режимах: **keyword + semantic**;
- generation через **grounded LLM**;
- end-to-end pipeline от запроса до ответа;
- fallback/clarify поведение в существующем MVP-контуре.

## 6. Non-goals / out of scope

В цикл не входили и не реализовывались:

- reranking;
- caching;
- multi-provider;
- agent orchestration.
