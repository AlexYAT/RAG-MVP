---
Project: RAG MVP
Doc type: implementation_snapshot
ID: DOA-IMP-003
Status: draft
Date: 2026-04-19
Parent: DOA-OP-004
---

# Title

Retrieval baseline implementation

## 1. Scope

Реализация Retrieval baseline согласно **DOA-OP-004**: retrieval-ready представление (чанки), поиск по текстовому запросу, top-k выдача с metadata, служебный HTTP endpoint. Generation, LLM, classifier, orchestration, dialogue handling, UI, hybrid search, reranking, caching и taxonomy filtering не добавлялись.

## 2. What was implemented

- **Retrieval-ready представление:** полные тексты markdown из `data/knowledge` (через расширенный ingest path) режутся на чанки по пустым строкам (параграфы); длинные параграфы дополнительно режутся по длине. У каждого чанка есть `relative_path`, `category`, `chunk_index` внутри файла.
- **Модуль retrieval:** `backend/app/retrieval/` — построение корпуса чанков, разреженное векторное пространство **TF–IDF по символьным n-граммам** (baseline для короткого русскоязычного корпуса без стемминга и без эмбеддингов), косинусная близость запроса к чанкам.
- **Top-k:** возвращается не более `min(top_k, 20, число_чанков)` результатов, отсортированных по убыванию score.
- **Проверка baseline:** `GET /retrieval/search` с параметрами `q` и `top_k` — JSON с `chunk_count`, `top_k_requested`, `top_k_returned`, списком `results` (текст фрагмента, `score`, вложенная `metadata`: путь, категория, индексы чанка).

## 3. Files

**Созданные:**

- `backend/app/retrieval/__init__.py`
- `backend/app/retrieval/chunks.py`
- `backend/app/retrieval/search.py`
- `docs/implementation_snapshot/DOA-IMP-003_retrieval_baseline.md`

**Изменённые:**

- `backend/app/knowledge/loader.py` (добавлен `load_markdown_full_documents`, ingest-метаданные переиспользуют полные тексты)
- `backend/app/main.py` (маршрут `/retrieval/search`)
- `backend/requirements.txt` (зависимости для TF–IDF и численных операций)

## 4. Verification

- **Запуск:** из каталога `backend` — ASGI-сервер для `app.main:app` (проверки выполнялись локально).
- **Проверка retrieval:** прямой вызов функции поиска из интерпретатора и HTTP `GET /retrieval/search?q=...&top_k=...` с URL-кодированием UTF-8 для запросов на кириллице.
- **Тестовые запросы (примеры):** `гарантия`, `монитор`, `монитор пациента` — ожидались ненулевые score и ожидаемые файлы (например FAQ для «гарантия», equipment/overview для «монитор»).
- **Результаты:** для корпуса из текущего synthetic dataset получено **32** чанка; для `top_k=3` возвращалось **3** элемента; для `top_k=2` — **2** элемента (соблюдение верхней границы top-k).
- **Top-k:** `top_k_returned` не превышал `top_k_requested` и не превышал число чанков.

## 5. Result

- Retrieval работает **на текущем synthetic dataset** в `data/knowledge`.
- Backend возвращает **релевантные по baseline** фрагменты с **прозрачной metadata** для последующей генерации.
- Следующий шаг **generation layer** не блокируется отсутствием retrieval: контекст можно собирать из `results[].text` и metadata.
