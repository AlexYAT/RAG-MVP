# RAG MVP (Demo-first)

Минимальный demo-first RAG-ассистент в домене медицинского оборудования.

Текущий baseline соответствует `DOA-IMP-014`: retrieval + grounded LLM generation соединены в рабочий end-to-end pipeline.

## Current Baseline

- **LLM usage в двух точках:**
  - embeddings для semantic retrieval;
  - grounded generation ответа из retrieval-контекста.
- **Retrieval modes:**
  - `semantic` (основной путь);
  - `keyword` (сохраняется как baseline/fallback path).
- **End-to-end flow:** `query -> retrieval -> generation -> response`.
- **MVP behavior:** fallback и clarify сценарии для текущего набора use-cases.
- **Evaluation baseline:** реализован и доступен отдельно (без обещания расширенной аналитики в runtime API).

## Quick Start

1. Откройте терминал в каталоге `backend`.
2. Установите зависимости:
   - `python -m pip install -r requirements.txt`
3. Создайте `.env` (например, на основе `.env.example`) и заполните `OPENAI_API_KEY`.
4. Запустите backend:
   - `python run.py`
5. Откройте UI:
   - [http://127.0.0.1:8000/ui](http://127.0.0.1:8000/ui)

## Environment Variables

Минимально необходимые переменные для LLM baseline:

- `OPENAI_API_KEY` — обязателен для embeddings и generation.
- `OPENAI_API_BASE` — базовый URL API.
- `OPENAI_EMBEDDING_MODEL` — модель embeddings.
- `OPENAI_GENERATION_MODEL` — модель generation.
- `OPENAI_TIMEOUT_SEC` — таймаут API-запросов.

Переменные retrieval storage:

- `CHROMA_PATH`
- `COLLECTION_NAME`

`dotenv` загружается на старте backend (`load_dotenv()`), system env сохраняет приоритет.

## Runtime/API Notes

Основные backend endpoints:

- `/retrieval/search` — retrieval trace (top-k + metadata).
- `/generation/answer` — retrieval + grounded generation.
- `/orchestration/query` — unified query flow.
- `/scenarios/handle` — scenario-level routing (`FAQ`, `selection`, `overview` + clarify path).

## Repository Hygiene

Runtime-артефакты Chroma (`.chroma/`, `backend/.chroma/`) используются локально, но не должны попадать в git.

## Demo Flow

Примеры запросов:

- FAQ: `Какой срок гарантии?`
- Overview: `Сделай обзор направлений`
- Selection: `Подбери портативный УЗИ для кабинета`
- Selection clarify: `Подбери оборудование`

## Project Structure

- `backend/` — backend приложение и API
- `data/knowledge/` — synthetic knowledge base
- `data/evaluation/` — evaluation dataset и reports
- `docs/` — DocOps lifecycle документы
- `README.md` — репозиторный entry point

## Limitations / Non-goals (Current MVP)

- Нет reranking.
- Нет multi-provider.
- Нет agent orchestration.
- Нет production hardening (CI/CD, scaling, security program).
- UI и UX остаются минимальными demo-level.

## License

Проект распространяется под лицензией MIT. См. `LICENSE`.
