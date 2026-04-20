---
Project: RAG MVP
Doc type: implementation_snapshot
ID: DOA-IMP-013
Status: accepted
Date: 2026-04-20
Parent: DOA-OP-013
---

# Title

Dotenv startup loading for MVP environment variables

## Summary

Выполнен `DOA-OP-013` в минимальном объёме: добавлена зависимость `python-dotenv` и ранняя загрузка `.env` в startup path backend-приложения. Изменения ограничены только необходимыми точками для MVP.

## Changes Made

- Обновлён `backend/requirements.txt`:
  - добавлена зависимость `python-dotenv>=1.0.1`.
- Обновлён `backend/app/main.py`:
  - добавлен импорт `load_dotenv` из `dotenv`;
  - добавлен вызов `load_dotenv()` на модульном уровне **до** импортов модулей приложения, где может читаться env.

Точка подключения `load_dotenv()`:
- файл: `backend/app/main.py`
- позиция: сразу после базовых импортов `Path` / `dotenv`, перед импортами `app.*` модулей.

## Verification

Проверка выполнена локально в `backend`:

1. Базовая проверка доступности ключа без ручного export:
   - до импорта `app.main`: `OPENAI_API_KEY` = `missing`;
   - после импорта `app.main`: `OPENAI_API_KEY` = `present`.

2. Проверка совместимости с system env:
   - при явной установке `OPENAI_API_KEY=SYSTEM_ENV_SENTINEL` в процессе,
   - после импорта `app.main` эффективное значение осталось `SYSTEM_ENV_SENTINEL`.

3. Проверка запуска:
   - импорт `app.main` и выполнение проверочных скриптов проходят без падения приложения.

## Result vs DoD

- `OPENAI_API_KEY` доступен без ручного export в development-сценарии: **достигнуто**.
- Приложение запускается/импортируется без ошибок после интеграции `dotenv`: **достигнуто**.
- `.env` корректно читается при старте: **достигнуто**.

Итог по DoD: **полностью достигнут**.

## Risks / Notes

- Риск конфликта значений между `.env` и system env остаётся управляемым: используется поведение `load_dotenv()` по умолчанию (без `override=True`), поэтому системные переменные не перезаписываются.
- Изменения не включают рефакторинг конфигурационной подсистемы и не затрагивают production orchestration (в рамках non-goals OP-013).
