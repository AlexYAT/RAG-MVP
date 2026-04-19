---
Project: RAG MVP
Doc type: implementation_snapshot
ID: DOA-IMP-005
Status: draft
Date: 2026-04-19
Parent: DOA-OP-006
---

# Title

Orchestration layer implementation

## 1. Scope

Реализация Orchestration layer согласно **DOA-OP-006**: единый flow **query → retrieval → generation**, единый backend entrypoint, унифицированный response contract и явная **traceability** retrieval-контекста в `retrieval_trace`. Classifier, scenario routing, dialogue handling и UI не добавлялись; алгоритмы retrieval/generation не переопределялись.

## 2. What was implemented

- **Модуль orchestration:** `backend/app/orchestration/service.py` — функция **`run_orchestration(query, top_k)`**, которая **делегирует** выполнение существующему **`run_generation_answer`** из `app.generation.pipeline` (тот же вызов `search_chunks` → `generate_from_hits`), без дублирования TF–IDF или правил генерации.
- **Связь слоёв:** фиксированная последовательность **retrieval → generation** сохраняется внутри `run_generation_answer`; orchestration только **оборачивает** результат в единый контракт и добавляет метаданные оркестрации.
- **Unified response contract:** верхний уровень ответа содержит поля **`request`** (`query`, `top_k`), **`orchestration`** (`pipeline`: `["retrieval", "generation"]`, `version`: 1), **`answer`**, **`fallback`**, **`fallback_reason`**, **`sources`**, **`retrieval_trace`** (полный след retrieval: `chunk_count`, `top_k_requested`, `hits_returned`, `results` с текстами чанков и metadata — тот же контекст, что использовался для генерации).
- **Проверка:** HTTP **`GET /orchestration/query?q=...&top_k=...`** — отдельно от **`/retrieval/search`** и **`/generation/answer`**, для служебной проверки сквозного потока без classifier и UI.

## 3. Files

**Созданные:**

- `backend/app/orchestration/__init__.py`
- `backend/app/orchestration/service.py`
- `docs/implementation_snapshot/DOA-IMP-005_orchestration_layer.md`

**Изменённые:**

- `backend/app/main.py` (маршрут `/orchestration/query`)

## 4. Verification

- **Запуск:** из каталога `backend`, как для предыдущих фаз.
- **Проверка orchestration:** вызов `run_orchestration("монитор", 3)` — наличие ключей `request`, `orchestration`, `answer`, `fallback`, `sources`, **`retrieval_trace`**; в `retrieval_trace.results` — те же элементы, что формируют контекст для `answer`.
- **Тестовые запросы:** `монитор` (успешный путь); HTTP **`GET /orchestration/query`** с параметром `q=УЗИ` (URL UTF-8), `top_k=2` — ответ **200**, непустой `answer`, заполненный `retrieval_trace` (проверка после ожидания готовности dev-сервера, например порт **8032**).
- **Ответы:** структура соответствует unified contract; при fallback поля `fallback` / `fallback_reason` заполняются так же, как в generation pipeline, плюс обёртка `request` / `orchestration`.
- **Unified contract:** проверено наличие стабильных полей верхнего уровня и вложенного **`retrieval_trace`** вместо разрозненного формата только для generation.
- **Traceability:** `retrieval_trace.results` дублирует выдачу retrieval, использованную генератором; `chunk_count` добавлен для полноты картины индекса.

## 5. Result

- Orchestration работает **поверх** существующих retrieval и generation через **единый** вызов pipeline.
- Backend возвращает **единый orchestration response** на **`/orchestration/query`**.
- **Retrieval trace** и **sources** доступны в одном JSON для аудита и следующих фаз.
- Следующий шаг **scenario handling** не блокируется: есть стабильная точка расширения поверх **`/orchestration/query`** и `run_orchestration`.
