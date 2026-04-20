---
Project: RAG MVP
Doc type: decision_log
ID: DOA-DEC-008
Status: draft
Date: 2026-04-20
Parent: DOA-IDEA-006
---

# Title

Semantic index update strategy fixed for MVP

## 1. Context

- В `DOA-IDEA-006` зафиксирован улучшительный цикл качества и эффективности для уже работающего RAG MVP.
- Внешний аудит выявил практическую проблему: полный rebuild semantic index / embeddings на каждом старте слишком дорогой по времени и ресурсам.
- Требуется более эффективная стратегия обновления индекса без premature complexity и без выхода за рамки MVP.

## 2. Decision

Зафиксировано принятое решение для текущего этапа:

- **Full rebuild on startup** не используется как целевая стратегия.
- Для MVP принимается **fingerprint-based rebuild strategy**.
- Semantic index / embeddings пересобираются только при изменении корпуса (по fingerprint состояния корпуса).
- **Incremental upsert / fine-grained partial sync** на текущем этапе не вводятся.

## 3. Rationale

- Снижение стоимости и времени старта по сравнению с unconditional full rebuild.
- Сохранение простоты реализации и воспроизводимости поведения.
- Меньшая сложность и операционный риск относительно incremental sync.
- Соответствие принципу **growth-ready, minimal-by-scope**.

## 4. Alternatives Considered

- **Full rebuild on startup** — отклонено как неэффективное для практической эксплуатации.
- **Incremental upsert** — отложено как более сложное решение, не обязательное для текущего MVP.
- **Fingerprint-based rebuild** — принято как баланс эффективности и простоты.

## 5. Consequences

**Плюсы:**

- Быстрее и дешевле старт.
- Поведение остаётся понятным и предсказуемым.
- Ниже риск ошибок синхронизации, чем у incremental подхода.

**Минусы:**

- Полный rebuild всё ещё возможен при любом изменении корпуса.
- Эффективность не максимальная относительно fine-grained incremental update.

## 6. Non-Goals

- Не вводится incremental document sync.
- Не вводится distributed indexing.
- Не вводится отдельная index management subsystem.
- Не меняется retrieval architecture beyond update strategy.
