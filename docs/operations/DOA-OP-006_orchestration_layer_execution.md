---
Project: RAG MVP
Doc type: operational
ID: DOA-OP-006
Status: draft
Date: 2026-04-19
Parent: DOA-OP-001
---

# Title

Orchestration layer execution

## 1. Context

- Документ — execution-шаг в рамках **DOA-OP-001** (MVP initial execution plan).
- Покрывает **только Phase 5 — Orchestration layer**.
- Опирается на **DOA-DEC-001**, **DOA-IMP-003** и **DOA-IMP-004**: retrieval baseline и generation layer уже реализованы и доступны backend как самостоятельные слои.

## 2. Objective

- **Связать** retrieval и generation в **единый orchestration flow** (одна последовательность вызовов на один пользовательский запрос).
- Обеспечить **единый backend entrypoint** для цепочки **query → retrieval → answer** (без дублирования разрозненных контрактов для продуктового клиента).
- Подготовить **основу для следующего шага** — scenario handling — **без** внедрения classifier и ветвления по сценариям в этом шаге.

## 3. Scope

**Включить:**

- **Orchestration flow** поверх существующих модулей retrieval и generation (повторное использование логики, а не копирование правил поиска/генерации).
- **Единый вход** для пользовательского запроса на уровне API/сервиса оркестрации.
- **Единый формат** backend-ответа orchestration layer (согласованные поля для ответа, контекста retrieval, источников и признаков fallback).
- **Передачу** одного и того же query через retrieval к generation в **фиксированном порядке**.
- **Возврат** `answer`, данных retrieval и **source metadata** в структуре, пригодной для последующего сценарного слоя и аудита.
- **Служебную** проверку orchestration через backend **без** classifier и **без** UI.

**Не включать:**

- Classifier и определение сценария (FAQ / selection / overview).
- Scenario routing и ветвление логики.
- Dialogue management и многоходовый диалог.
- Web UI.
- Расширенную бизнес-логику, policy layer, кэширование.
- Улучшения retrieval/generation сверх уже зафиксированного baseline.

## 4. Orchestration Baseline

Зафиксировать свойства baseline:

- Orchestration **использует** существующие retrieval и generation как **подчинённые** шаги; не заменяет их внутренние правила.
- Orchestration **не принимает решений о сценарии** и не подменяет собой следующий этап scenario handling.
- Orchestration **не добавляет** многоходовый диалог и не управляет историей беседы в продуктовом смысле.
- Orchestration **минимально достаточен** для последующего подключения scenario handling (единая точка расширения без переписывания retrieval/generation).
- Сохраняется **traceability**: в ответе или сопутствующей структуре **видно**, какой **retrieval-контекст** использовался при формировании ответа (ссылки на фрагменты, scores, пути — в объёме, согласованном с текущими IMP).

## 5. Tasks

На уровне намерений, без кода:

1. Определить **единый orchestration input** (параметры пользовательского запроса и, при необходимости, технические параметры глубины retrieval — в рамках уже принятого baseline).
2. **Связать** вызов retrieval и generation в **одном** backend flow без расхождения порядка шагов.
3. Сформировать **единый response contract** orchestration layer (имена полей и вложенность — на уровне соглашения проекта; детали — в implementation snapshot).
4. Добавить **служебную проверку** orchestration (отдельный маршрут или явное разделение от прямых вызовов `/retrieval/search` и legacy-пути generation), проверяемую **без** classifier и UI.
5. Обеспечить **проверяемый результат** на текущем synthetic dataset и существующих IMP-слоях.

## 6. Expected Result

- Backend **принимает** пользовательский query через **единый** orchestration entrypoint.
- Orchestration **вызывает** retrieval и generation в **правильной последовательности** (сначала контекст, затем ответ).
- Система возвращает **унифицированный** ответ orchestration layer.
- Следующий шаг **scenario handling** **не блокируется** отсутствием orchestration: есть стабильная «сквозная» точка для надстройки сценариев.

## 7. Validation

Критерии приёмки:

- Orchestration работает **поверх** существующих retrieval и generation **без** дублирования их алгоритмической сути.
- На **тестовых запросах** возвращается **единый** backend response, согласованный с контрактом orchestration.
- **Retrieval trace** и **sources** **доступны** в ответе или однозначно восстанавливаются из него.
- Orchestration **можно проверить отдельно** от classifier, scenario routing и UI.
- Для признания шага выполненным **не требуются** Web UI и продуктовая логика диалога.

## 8. Out of Scope

- Classifier и выбор сценария.
- Dialogue handling.
- User interface.
- Ветвление по сценариям (FAQ / selection / overview) — отдельный этап.
- Улучшения retrieval/generation сверх baseline.
- Production-оптимизация и политики безопасности.
