---
Project: RAG MVP
Doc type: implementation_snapshot
ID: DOA-IMP-007
Status: draft
Date: 2026-04-19
Parent: DOA-OP-008
---

# Title

Web UI implementation

## 1. Scope

Реализация Web UI согласно DOA-OP-008: минимальный demo-oriented интерфейс, подключение к scenario-level backend, ввод запроса, показ ответа, базовая история взаимодействия. Retrieval / generation / orchestration / scenario logic не перерабатывались за пределами необходимой UI-интеграции.

## 2. What was implemented

- **UI-структура:** добавлен статический frontend в `backend/app/ui/` (`index.html`, `styles.css`, `app.js`) без сложного framework setup.
- **Подключение к backend:** UI отправляет запросы в существующий scenario endpoint `GET /scenarios/handle?q=...&top_k=...`; backend-слой retrieval/generation/orchestration/scenarios переиспользуется как есть.
- **Ввод/отправка/показ ответа:** реализованы поле ввода, кнопка отправки, кнопки demo-примеров, вывод текста ответа и признаков обработки.
- **Базовая история:** в рамках одной локальной сессии хранится in-memory массив запросов/ответов, показывается история карточками (query, answer, scenario, mode, fallback, trace summary).
- **Отображение scenario/mode/trace:** UI выводит `scenario.name`, `mode`, `fallback`, количество `sources`, число retrieval hits из `retrieval_trace.results`.
- **UI entrypoint:** в backend добавлен маршрут `GET /ui` и раздача статических файлов через `app.mount("/ui/static", ...)`.

## 3. Files

**Созданные:**

- `backend/app/ui/index.html`
- `backend/app/ui/styles.css`
- `backend/app/ui/app.js`
- `docs/implementation_snapshot/DOA-IMP-007_web_ui.md`

**Изменённые:**

- `backend/app/main.py` (маршрут `/ui`, static mount для `/ui/static`)

## 4. Verification

- **Запуск backend:** локально через ASGI (`uvicorn app.main:app`) из каталога `backend`.
- **Открытие UI:** проверены `GET /ui` (HTML) и `GET /ui/static/app.js` (JS), оба ответа 200.
- **Проверка интеграции UI→backend:** подтверждено, что `app.js` вызывает `/scenarios/handle`.
- **Тестовые запросы для path coverage:**
  - FAQ: `Какой срок гарантии?` → `scenario=faq`, `mode=answer`
  - Overview: `Сделай обзор направлений` → `scenario=overview`, `mode=answer`
  - Selection: `Подбери портативный УЗИ для кабинета` → `scenario=selection`, `mode=answer`
  - Selection clarify: `Подбери оборудование` → `scenario=selection`, `mode=clarify`, `fallback_reason=selection_needs_clarification`
- **Подтверждение scenario-level backend:** все ответы для UI-потока идут через `/scenarios/handle`; trace поля (`retrieval_trace`/`sources`) сохраняются в ответе и выводятся в UI summary.

## 5. Result

- UI открывается локально.
- Запрос из UI доходит до backend и обрабатывается scenario-layer.
- Ответ отображается в интерфейсе.
- История работает в объёме demo-сессии (in-memory, без сложного state).
- Полный MVP pipeline демонстрируется через Web UI end-to-end.
