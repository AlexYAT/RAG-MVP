---
Project: RAG MVP
Doc type: implementation_snapshot
ID: DOA-IMP-002
Status: draft
Date: 2026-04-19
Parent: DOA-OP-003
---

# Title

Data ingest setup implementation

## 1. Scope

Реализация шага Data ingest setup согласно **DOA-OP-003**: synthetic dataset, структура knowledge base, ingest/loading path, проверка загрузки. Retrieval, embeddings, LLM, scenario routing и UI не добавлялись.

## 2. What was implemented

- **Структура synthetic dataset:** каталог `data/knowledge/` с подпапками `faq/`, `equipment/`, `overview/`; документы в формате Markdown (`.md`).
- **Типы документов:** один FAQ-файл с 4 парами вопрос–ответ; семь карточек оборудования для сценария selection; один файл обзора направлений для overview.
- **Загрузка документов:** модуль `backend/app/knowledge/loader.py` — разрешение корня репозитория, чтение всех `*.md` под `data/knowledge`, категория по первому сегменту пути, подсчёт символов, превью текста.
- **Проверка ingest baseline:** служебный HTTP endpoint **`GET /ingest/status`** возвращает JSON: путь к knowledge root, `document_count`, агрегаты `by_category`, список документов с `relative_path`, `category`, `char_count`, `preview`.

## 3. Files

**Созданные:**

- `data/knowledge/faq/faq.md`
- `data/knowledge/overview/directions.md`
- `data/knowledge/equipment/device_01.md` … `device_07.md`
- `backend/app/knowledge/__init__.py`
- `backend/app/knowledge/loader.py`
- `docs/implementation_snapshot/DOA-IMP-002_data_ingest_setup.md`

**Изменённые:**

- `backend/app/main.py` (маршрут `/ingest/status`)

## 4. Verification

- **Запуск:** из каталога `backend` — ASGI-сервер разработки для приложения `app.main:app` (проверка выполнялась на порту 8010, чтобы исключить конфликт с уже занятым 8000).
- **Проверка ingest baseline:** HTTP `GET http://127.0.0.1:8010/ingest/status` — ответ **200**, JSON с полями `document_count`, `by_category`, `documents`.
- **Результаты:** `document_count`: **9**; `by_category`: **equipment** — 7, **faq** — 1, **overview** — 1; в `documents` — относительные пути файлов, категории, длина текста, превью содержимого (для ручной проверки чтения файлов системой).

## 5. Result

- Synthetic dataset **присутствует** в репозитории и покрывает три сценария MVP (FAQ, selection, overview).
- Документы **читаются backend** и отражаются в ответе `/ingest/status` без retrieval и генерации.
- Следующий шаг **retrieval baseline** не блокируется отсутствием исходных данных.
