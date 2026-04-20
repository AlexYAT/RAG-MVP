---
Project: RAG MVP
Doc type: operational_plan
ID: DOA-OP-014
Status: draft
Date: 2026-04-20
Parent: DOA-DEC-008
---

# Title

Quality and efficiency improvements execution plan for RAG MVP

## 1. Overview

- Цель: реализовать улучшения, зафиксированные в `DOA-IDEA-006`.
- Стратегия индексации берётся из `DOA-DEC-008` (fingerprint-based rebuild).
- Изменения должны улучшить эксплуатацию и эффективность без поломки текущего pipeline baseline из `DOA-IMP-014`.

## 2. Execution Scope

Включено:

- обновление документации (`README`);
- очистка репозитория от runtime-артефактов;
- внедрение fingerprint-based rebuild для semantic index;
- безопасная обработка ошибок LLM в user-facing ответах.

## 3. Tasks

### T1 — README alignment

Сделать:

- обновить `README` под текущее состояние системы:
  - LLM usage (embeddings + generation);
  - env переменные и обязательность корректного `.env` для development;
  - зависимости (OpenAI API usage, vector storage baseline);
  - различие semantic / keyword retrieval;
  - текущий базовый pipeline.

Проверка:

- `README` отражает фактическое поведение системы.

### T2 — Repository hygiene

Сделать:

- исключить `.chroma/` из репозитория:
  - добавить правило в `.gitignore`;
  - при необходимости убрать runtime-артефакты из индекса.

Проверка:

- `.chroma/` не появляется в `git status` после runtime-прогонов.

### T3 — Semantic index efficiency (по DEC-008)

Сделать:

- реализовать fingerprint корпуса данных;
- сравнивать fingerprint при старте;
- выполнять rebuild semantic index только при изменении корпуса;
- сохранить текущее поведение retrieval-контракта.

Проверка:

- при неизменном корпусе индекс не пересоздаётся полностью;
- при изменении корпуса rebuild выполняется корректно.

### T4 — Error handling safety

Сделать:

- убрать возврат внутренних деталей ошибок пользователю;
- в user response вернуть безопасное сообщение;
- детальную информацию об ошибках оставить во внутреннем логировании.

Проверка:

- пользователь не видит stack trace / internal error details;
- fallback поведение сохраняется.

## 4. Execution Order

1. **T2** — быстрый infra fix (runtime-гигиена репозитория).
2. **T1** — синхронизация документации с фактическим состоянием.
3. **T3** — оптимизация стратегии обновления semantic index по `DOA-DEC-008`.
4. **T4** — безопасная обработка ошибок без изменения продуктового контракта.

## 5. Acceptance Criteria

- `README` актуален и соответствует текущей системе.
- `.chroma/` не попадает в репозиторий.
- semantic index не пересоздаётся без изменений корпуса.
- внутренние ошибки не утекут в пользовательские ответы.
- pipeline продолжает работать совместимо с baseline из `DOA-IMP-014`.

## 6. Non-Goals

- не вводится reranking;
- не вводится caching (кроме index-level стратегии по `DOA-DEC-008`);
- не вводится multi-provider;
- не изменяется pipeline-архитектура;
- не добавляется новая функциональность RAG.
