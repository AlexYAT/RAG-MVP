---
Project: RAG MVP
Doc type: operational
ID: DOA-OP-004
Status: draft
Date: 2026-04-19
Parent: DOA-OP-001
---

# Title

Retrieval baseline execution

## 1. Context

- Документ — execution-шаг в рамках **DOA-OP-001** (MVP initial execution plan).
- Покрывает **только Phase 3 — Retrieval baseline**.
- Опирается на **DOA-DEC-001** (vector-based retrieval baseline, без hybrid/rerank/cache/taxonomy) и на **DOA-IMP-002**: synthetic dataset создан, документы доступны через ingest/loading path.

## 2. Objective

- Реализовать **базовый retrieval** поверх уже загружаемого synthetic dataset.
- Обеспечить **программный** отбор релевантных фрагментов по пользовательскому запросу в объёме baseline.
- Подготовить **вход для следующего шага** — generation layer — без реализации генерации в этом шаге.

## 3. Scope

**Включить:**

- Подготовку **retrieval-ready** представления документов (разбиение/чанки или эквивалент, достаточный для поиска по тексту — без фиксации формата в этом документе).
- Минимальную логику **поиска** по knowledge base в границах baseline.
- Возврат **top-k** результатов с ограничением размера выдачи.
- **Служебный** способ проверки retrieval baseline через backend (endpoint или эквивалент), **без** вызова generation.

**Не включать:**

- Generation, LLM, prompt construction.
- Classifier, orchestration, dialogue handling.
- Web UI.
- Hybrid search, reranking, caching, taxonomy filtering.

## 4. Retrieval Baseline

Зафиксировать свойства baseline:

- Retrieval опирается **только** на synthetic dataset и существующий ingest path.
- Выдача **ограничена top-k**; число k задаётся явно и остаётся небольшим для демо.
- Результаты **проверяемы**: видно, из какого источника/фрагмента получен ответ кандидата.
- У каждого элемента выдачи сохраняется **metadata** (например источник документа, позиция/идентификатор фрагмента — детали фиксируются в implementation snapshot, не здесь).
- Baseline **достаточен** для последующего использования в сценариях FAQ / selection / overview на этапе оркестрации, **без** реализации сценариев в этом шаге.

## 5. Tasks

На уровне намерений, без кода и без перечисления библиотек:

1. Подготовить документы к виду, пригодному для retrieval baseline (единый pipeline от загруженных документов к поисковым единицам).
2. Реализовать механизм отбора релевантных фрагментов по **текстовому запросу** пользователя в рамках выбранного baseline-подхода.
3. Реализовать **top-k** выдачу; каждый элемент — фрагмент текста плюс metadata.
4. Добавить **служебную проверку** retrieval (например запрос с параметром top-k), не смешивая с generation.
5. Обеспечить **воспроизводимую проверку** на текущем synthetic dataset (ожидаемые свойства: непустая выдача на тестовых запросах, соблюдение top-k).

## 6. Expected Result

- Backend **принимает** вход для retrieval baseline (запрос и параметры выдачи в объёме, достаточном для проверки).
- Система возвращает **top-k** релевантных кандидатов с **metadata**.
- Результат пригоден как **вход для generation** на следующей фазе.
- Шаг generation **не блокируется** отсутствием retrieval.

## 7. Validation

Критерии приёмки:

- Retrieval выполняется **на synthetic dataset**, загружаемом тем же контуром, что и после DOA-IMP-002.
- На тестовом запросе возвращаются **релевантные** в смысле baseline фрагменты (проверка зафиксируется в implementation snapshot).
- **Top-k** ограничение **соблюдается**.
- Retrieval **проверяем отдельно** от generation и UI.
- Для признания шага выполненным **не требуются** LLM, orchestration и classifier.

## 8. Out of Scope

- Generation и построение prompt.
- Scenario routing и выбор сценария.
- Dialogue management.
- User interface.
- Улучшения retrieval сверх baseline (hybrid, rerank, кэш, сложная фильтрация).
- Production-оптимизация и нагрузочное тестирование.
