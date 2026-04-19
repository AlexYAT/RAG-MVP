---
Project: RAG MVP
Doc type: implementation_snapshot
ID: DOA-IMP-004
Status: draft
Date: 2026-04-19
Parent: DOA-OP-005
---

# Title

Generation layer implementation

## 1. Scope

Реализация Generation layer согласно **DOA-OP-005**: генерация поверх retrieval baseline, извлекательный grounded-ответ только из фрагментов retrieval, предсказуемый fallback, возврат `sources` и полного блока `retrieval` для трассировки. Classifier, scenario routing, orchestration, dialogue handling, UI, policy layer, caching и гибридная бизнес-логика не добавлялись.

## 2. What was implemented

- **Модуль generation:** пакет `backend/app/generation/` — `answer.py` (правила ответа и fallback), `pipeline.py` (цепочка query → `search_chunks` → `generate_from_hits`).
- **Вход generation:** пользовательский `query` и результаты **того же** retrieval baseline (`RetrievalHit`), получаемые внутри pipeline через `search_chunks`; внешних знаний вне переданных фрагментов генератор не подмешивает.
- **Grounded answer:** связный текст на русском языке, собранный **только** из топовых фрагментов (до 3), с усечением длины, явным перечислением пути источника и числовой «релевантности» (score из TF–IDF baseline), дисклеймером демо-режима.
- **Fallback:** `no_hits` — пустая выдача retrieval; `weak_retrieval_score` — максимальный score ниже порога `_MIN_TOP_SCORE` (0.02); `insufficient_context` — суммарная длина топ-фрагментов ниже `_MIN_CONTEXT_CHARS` (80); пустой запрос обрабатывается как `empty_query` (дополнительная защита помимо API).
- **Проверка:** HTTP **`GET /generation/answer?q=...&top_k=...`** возвращает `answer`, `fallback`, `fallback_reason`, `sources`, вложенный объект **`retrieval`** с теми же результатами, что даёт baseline retrieval (для проверки опоры на retrieval без оркестратора).

## 3. Files

**Созданные:**

- `backend/app/generation/__init__.py`
- `backend/app/generation/answer.py`
- `backend/app/generation/pipeline.py`
- `docs/implementation_snapshot/DOA-IMP-004_generation_layer.md`

**Изменённые:**

- `backend/app/main.py` (маршрут `/generation/answer`)

## 4. Verification

- **Запуск:** из каталога `backend`, интерпретатор Python с `PYTHONPATH`/рабочим каталогом `backend` (как и для предыдущих фаз).
- **Проверка generation:** вызов `run_generation_answer("монитор", 3)` — ожидалось **`fallback`: false**, непустой **`answer`**, непустые **`sources`** и блок **`retrieval.results`** с чанками.
- **Тестовые запросы:** `монитор` (нормальный ответ); длинная строка без пересечения с корпусом `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` — ожидался fallback **`weak_retrieval_score`** при низком максимальном score.
- **Ответы:** для успешного пути — многострочный текст с цитированием фрагментов из `equipment/` / `overview/` / `faq/`; для weak — короткое сообщение об ограниченной уверенности, при этом **`sources`** всё же отражают топ retrieval для аудита.
- **Fallback:** подтверждён сценарий `weak_retrieval_score`; сценарии `no_hits` / `insufficient_context` покрыты кодом и ожидаются при пустом корпусе или экстремально коротких чанках (в текущем датасете основной ручной проверкой служит weak-path).
- **Опора на retrieval:** в каждом ответе успешного пути текст фрагментов взят из полей `RetrievalHit.text`; структура **`retrieval`** дублирует выдачу `/retrieval/search` для того же `q` и `top_k`.

## 5. Result

- Generation работает **поверх** retrieval baseline и использует **только** его выдачу.
- Backend возвращает **текстовый `answer`** и **метаданные источников** в `sources`.
- **Fallback** срабатывает предсказуемо при низкой релевантности (проверено на искусственно «чужом» запросе).
- Следующий шаг **orchestration** не блокируется: контракт «query → retrieval → answer» уже доступен для обёртки оркестратором.
