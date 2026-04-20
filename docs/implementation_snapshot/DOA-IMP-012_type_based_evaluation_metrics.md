---
Project: RAG MVP
Doc type: implementation_snapshot
ID: DOA-IMP-012
Status: accepted
Date: 2026-04-20
Parent: DOA-OP-011
---

# Title

Type-based evaluation metrics and stratified report

## 1. What was implemented

- **Dataset** (`data/evaluation/eval_dataset.json`): у каждой записи обязательное поле **`type`** со значениями из DEC (**lexical**, **paraphrase**, **noisy**, **scenario**); вопросы слегка скорректированы там, где это улучшает соответствие типу, без расширения схемы полей.
- **Loader** (`backend/app/evaluation/dataset.py`): чтение и нормализация `type` (trim, lower), валидация по enum; при отсутствии, пустом или неизвестном `type` — **`ValueError`** с понятным сообщением; для CSV обязательна колонка **`type`**.
- **Runner** (`backend/app/evaluation/runner.py`): один проход по dataset на режим (**keyword** / **semantic**); в каждой строке `per_item` добавлено поле **`type`**; агрегация **`per_type`** по фиксированному порядку типов; глобальный **`summary`** сохранён; для сравнения режимов добавлен **`hallucination_rate_delta`** в блоке comparison (глобально и по типам).
- **Отчёт**: `data/evaluation/reports/eval_report.json` — блок **`per_type.<type>.keyword|semantic|comparison_keyword_vs_semantic`**.

CSV-примера в репозитории не было — отдельный CSV не добавлялся (условие OP «если есть»).

## 2. Files touched

- `data/evaluation/eval_dataset.json`
- `data/evaluation/reports/eval_report.json`
- `backend/app/evaluation/dataset.py`
- `backend/app/evaluation/runner.py`
- `docs/implementation_snapshot/DOA-IMP-012_type_based_evaluation_metrics.md`

Retrieval, embeddings и vector store **не изменялись**.

## 3. Dataset strategy (как зафиксировано)

- Единый JSON-dataset с обязательным **`type`** на запись (**DOA-DEC-005**).
- Типы запросов покрывают **lexical / paraphrase / noisy / scenario** для стратифицированного сравнения **keyword vs semantic**.

## 4. Report additions

- **`per_type`**: для каждого типа — метрики **`keyword`**, **`semantic`**, и **`comparison_keyword_vs_semantic`** (дельты semantic − keyword по correctness, hit_rate, overlap, hallucination_rate).
- **`summary`**: прежний глобальный свод по всему dataset (вспомогательный aggregate).

## 5. Verification

- Успешный прогон: из каталога `backend` выполнено `python -m app.evaluation --top-k 5` — завершилось без ошибки, отчёт перезаписан.
- В `eval_report.json` присутствует ключ **`per_type`** с подключами `lexical`, `paraphrase`, `noisy`, `scenario`.
- Отсутствие `type`: загрузка временного JSON только с `question` → **`ValueError: items[0]: field 'type' is required`**.
- CLI **`python -m app.evaluation`** без изменений контракта (опции `--dataset`, `--out`, `--top-k` по-прежнему работают).

## 6. Known limitations

- Dataset по-прежнему **небольшой** и синтетический.
- Без RAGAS, UI, CI; без изменений retrieval-пайплайна.
- Judge по-прежнему может работать в **heuristic** режиме без API-ключа — стратифицированные метрики зависят от этого качества.
