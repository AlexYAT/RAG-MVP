---
Project: RAG MVP
Doc type: implementation_snapshot
ID: DOA-IMP-006
Status: draft
Date: 2026-04-19
Parent: DOA-OP-007
---

# Title

Scenario handling implementation

## 1. Scope

Реализация Scenario handling согласно DOA-OP-007: различение FAQ / selection / overview, backend-ветвление поверх orchestration, минимальное уточнение для selection, служебная проверка без UI. Web UI, дополнительные сценарии и сложный dialogue management не добавлялись.

## 2. What was implemented

- **Scenario-handling модуль:** добавлен пакет `backend/app/scenarios/` с `service.py` и функцией `run_scenario_flow(query, top_k)`; этот слой не реализует retrieval/generation заново, а вызывает существующий orchestration.
- **Определение сценария:** `detect_scenario()` на rule-based эвристиках (`rules_v1`) классифицирует запрос в один из трёх сценариев: `faq`, `selection`, `overview`.
- **Использование orchestration:** для FAQ/overview и для достаточного selection-запроса сценарный слой вызывает `run_orchestration(...)` и возвращает ответ с полями `answer`, `fallback`, `sources`, `retrieval_trace`, `orchestration_trace`.
- **Уточнение для selection:** если запрос слишком общий/недостаточный, возвращается один предсказуемый clarify-response (`mode=clarify`, `fallback_reason=selection_needs_clarification`) без state machine и длинного диалога.
- **Проверка scenario handling:** добавлен отдельный endpoint `GET /scenarios/handle` (отдельно от `/orchestration/query`) для служебной проверки всех трёх сценариев и clarify-path.

## 3. Files

**Созданные:**

- `backend/app/scenarios/__init__.py`
- `backend/app/scenarios/service.py`
- `docs/implementation_snapshot/DOA-IMP-006_scenario_handling.md`

**Изменённые:**

- `backend/app/main.py` (маршрут `/scenarios/handle`)

## 4. Verification

- **Запуск:** локальный dev-сервер поднимался из каталога `backend` через ASGI (`uvicorn app.main:app`).
- **Проверка scenario handling:** endpoint `GET /scenarios/handle?q=...&top_k=3` проверялся на четырёх запросах:
  - FAQ: `Какой срок гарантии?` → `scenario=faq`, `mode=answer`
  - Overview: `Сделай обзор направлений` → `scenario=overview`, `mode=answer`
  - Selection (достаточный): `Подбери портативный УЗИ для кабинета` → `scenario=selection`, `mode=answer`
  - Selection clarify-path: `Подбери оборудование` → `scenario=selection`, `mode=clarify`, `fallback_reason=selection_needs_clarification`
- **Проверка traceability:** в answer-path подтверждено наличие `retrieval_trace` и `orchestration_trace` (включая список retrieval-результатов); trace не теряется при прохождении через scenario layer.
- **Проверка разделения слоёв:** `/scenarios/handle` работает как отдельный сервисный вход, не заменяя прямые `/retrieval/search`, `/generation/answer`, `/orchestration/query`.

## 5. Result

- Backend различает три сценария MVP: FAQ, selection, overview.
- FAQ / selection / overview обрабатываются раздельно поверх существующего orchestration.
- Selection поддерживает минимальное воспроизводимое уточнение при недостаточном запросе.
- Следующий шаг Web UI не блокируется: есть отдельный стабильный backend entrypoint сценарного уровня.
