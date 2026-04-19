---
Project: RAG MVP
Doc type: implementation_snapshot
ID: DOA-IMP-001
Status: draft
Date: 2026-04-19
Parent: DOA-OP-002
---

# Title

Project bootstrap implementation

## 1. Scope

Реализация Project bootstrap согласно **DOA-OP-002**: минимальный backend, entrypoint, один служебный endpoint, локальный запуск. Retrieval, ingest, LLM, сценарии и UI не добавлялись.

## 2. What was implemented

- **Структура проекта:** каталог `backend/` с пакетом `app/` под дальнейшее расширение.
- **Backend entrypoint:** модуль `app.main` экспортирует ASGI-приложение; для локального запуска используется `backend/run.py` (обёртка над ASGI-сервером разработки).
- **API endpoint:** `GET /health` возвращает JSON с полем статуса для проверки «живости» сервиса.
- **Запуск сервера:** из каталога `backend` — установка зависимостей из `requirements.txt`, затем запуск через модуль ASGI-сервера или через `run.py`.

## 3. Files

- `backend/requirements.txt`
- `backend/app/__init__.py`
- `backend/app/main.py`
- `backend/run.py`
- `.gitignore` (Python/venv артефакты)

## 4. Verification

- **Запуск сервера:** из `backend` выполнялся запуск ASGI-приложения `app.main:app` на `127.0.0.1:8000` (процесс uvicorn).
- **Проверка endpoint:** запрос `GET http://127.0.0.1:8000/health`.
- **Пример ответа:** тело ответа `{"status":"ok"}` (HTTP 200).

## 5. Result

- Система (backend) **запускается** локально.
- Endpoint **`/health` отвечает** и подтверждает доступность сервиса без dataset, retrieval и UI.
