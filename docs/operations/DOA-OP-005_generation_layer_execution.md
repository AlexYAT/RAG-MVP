---
Project: RAG MVP
Doc type: operational
ID: DOA-OP-005
Status: draft
Date: 2026-04-19
Parent: DOA-OP-001
---

# Title

Generation layer execution

## 1. Context

- Документ — execution-шаг в рамках **DOA-OP-001** (MVP initial execution plan).
- Покрывает **только Phase 4 — Generation layer**.
- Опирается на **DOA-DEC-001** и на **DOA-IMP-003**: synthetic dataset и **retrieval baseline** уже существуют и доступны backend; retrieval возвращает фрагменты с metadata.

## 2. Objective

- Добавить **generation layer** поверх результатов retrieval baseline.
- Формировать **текстовый ответ** на основе пользовательского запроса и найденного контекста (retrieved fragments).
- Подготовить **основу для следующего шага** — orchestration layer — **без** реализации оркестрации, сценарной маршрутизации и UI в этом шаге.

## 3. Scope

**Включить:**

- Приём **пользовательского query** и **retrieval context** (результаты baseline retrieval) как входа в generation.
- Минимальные правила **grounded** ответа: опора на переданные фрагменты, без выдумывания фактов сверх явно доступного контекста в рамках MVP.
- Формирование **связного текстового ответа** на основе retrieved fragments и запроса.
- **Fallback** при отсутствии или недостаточности контекста (честное ограничение, отказ или краткое уточнение — формулировка фиксируется в implementation snapshot, не здесь).
- **Служебный** способ проверки generation layer через backend (endpoint или эквивалент), **отдельно** от classifier, orchestration и UI.

**Не включать:**

- Classifier и определение сценария.
- Scenario routing и orchestration end-to-end.
- Dialogue management (многоходовый диалог).
- Web UI.
- Продвинутый prompt engineering, policy layer, кэширование.
- Смешанную «гибридную» бизнес-логику поверх generation.

## 4. Generation Baseline

Зафиксировать свойства baseline:

- Generation использует **только** пользовательский запрос и **выход retrieval baseline** (тексты фрагментов и сопутствующая metadata, доступная на входе).
- Ответ должен быть **grounded** в retrieved context в объёме, согласованном с demo-first MVP.
- При **недостаточном контексте** — предсказуемое **fallback**-поведение без имитации полноты знаний.
- Baseline **достаточен** для последующего использования в сценариях FAQ / selection / overview на этапе оркестрации, **без** реализации этих сценариев здесь.
- **Metadata источников** (путь, категория, идентификаторы чанков и т.п.) **сохраняется или доступна** для следующих фаз (цитирование, объяснение, логирование) — без обязательного показа пользователю в этом шаге.

## 5. Tasks

На уровне намерений, без кода:

1. Определить и реализовать **вход generation layer**: query + результаты retrieval baseline в согласованном виде.
2. Реализовать **формирование ответа** поверх найденного контекста с минимальными правилами grounded generation.
3. Реализовать **fallback** при пустой выдаче retrieval, нулевой релевантности или явной нехватке оснований для ответа.
4. Добавить **служебную проверку** generation (например единый endpoint «query → retrieval → answer» или отдельный вызов generation с заранее заданным контекстом) так, чтобы слой можно было валидировать **изолированно** от classifier/orchestration/UI.
5. Обеспечить **проверяемый результат** на текущем synthetic dataset и существующем retrieval baseline.

## 6. Expected Result

- Backend **принимает** вход, достаточный для generation (query + retrieval context по правилам проекта).
- Система возвращает **связный текстовый ответ**, согласованный с baseline generation.
- Ответ **опирается** на retrieval baseline, а не на произвольные внешние знания вне переданного контекста.
- Следующий шаг **orchestration** **не блокируется** отсутствием generation.

## 7. Validation

Критерии приёмки:

- Generation работает **поверх** retrieval baseline (тот же контур данных и поиска, что после DOA-IMP-003).
- На **тестовых запросах** система возвращает **текстовый ответ** (не только сырой retrieval).
- При **недостатке контекста** срабатывает **корректный fallback** по заранее определённым правилам.
- Generation **можно проверить отдельно** от scenario routing и UI.
- Для признания шага выполненным **не требуются** classifier, orchestration и Web UI.

## 8. Out of Scope

- Scenario routing и выбор сценария.
- Dialogue handling и уточняющие вопросы как продуктовая логика.
- User interface.
- Улучшения retrieval сверх уже зафиксированного baseline.
- Policy / security hardening и production-оптимизация generation.
