# RAG MVP (Demo-first)

Минимальный demo-first проект RAG-ассистента в домене медицинского оборудования.  
Система показывает полный локальный pipeline: ingest synthetic данных, retrieval, generation, scenario handling и Web UI.

## Features

- Scenario handling для `FAQ`, `selection`, `overview`
- Retrieval baseline с top-k выдачей и metadata
- Grounded generation с fallback
- Unified orchestration flow query -> retrieval -> answer
- Минимальный Web UI для demo-сессии

## Quick Start

1. Откройте терминал в каталоге `backend`.
2. Установите зависимости:
   - `python -m pip install -r requirements.txt`
3. Запустите backend:
   - `python run.py`
4. Откройте UI:
   - [http://127.0.0.1:8000/ui](http://127.0.0.1:8000/ui)

## Run Backend

Из каталога `backend`:

- `python run.py`

Альтернатива:

- `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000`

## Open UI

После запуска backend откройте:

- [http://127.0.0.1:8000/ui](http://127.0.0.1:8000/ui)

UI отправляет запросы в scenario-level endpoint:

- `/scenarios/handle`

## Demo Flow

Примеры запросов для проверки paths:

- FAQ: `Какой срок гарантии?`
- Overview: `Сделай обзор направлений`
- Selection: `Подбери портативный УЗИ для кабинета`
- Selection clarify: `Подбери оборудование`

## Project Structure

- `backend/` — backend приложение и API
- `data/knowledge/` — synthetic knowledge base
- `docs/` — DocOps lifecycle документы
- `README.md` — entry point для внешнего пользователя

## Limitations

- Demo-first baseline (не production-ready)
- Без Docker / CI/CD / deployment
- Без advanced security hardening
- Ограниченный UX и минимальный state

## License

Проект распространяется под лицензией MIT. См. файл `LICENSE`.
