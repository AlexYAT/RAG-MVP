---
Project: RAG MVP
Doc type: architecture
ID: DOA-ARCH-004
Status: draft
Date: 2026-04-20
Parent: DOA-IDEA-004
---

# Title

RAG evaluation pipeline architecture

## 1. Overview

- Цель evaluation слоя — измерять качество RAG-системы на воспроизводимом наборе вопросов.
- Evaluation слой встраивается как отдельный контур поверх текущего baseline и не изменяет основной runtime pipeline.
- Архитектура фокусируется на сравнении retrieval/answer качества между режимами и формировании отчёта.

## 2. High-Level Flow

Dataset  
→ Retrieval  
→ Answer  
→ Evaluation  
→ Report

## 3. Components

- **Dataset Provider**  
  Поставляет набор evaluation-вопросов и сопутствующие ожидаемые данные (если доступны).

- **Evaluation Runner**  
  Координирует прогон сценариев оценки и управляет последовательностью этапов.

- **Retrieval Modes (keyword vs semantic)**  
  Обеспечивает переключение между keyword и semantic retrieval режимами для сопоставимого сравнения.

- **Answer Generator (reuse existing pipeline)**  
  Использует существующий answer flow без изменений бизнес-логики.

- **Evaluator (LLM or rule-based abstraction)**  
  Выполняет оценку ответа и retrieval-результатов через абстракцию оценщика.

- **Metrics Aggregator**  
  Собирает, нормализует и агрегирует метрики по режимам и наборам вопросов.

- **Report Output**  
  Формирует итоговый отчёт сравнения качества и наблюдаемых различий между режимами.

## 4. Evaluation Modes

- **Keyword mode**  
  Оценка качества при keyword retrieval.

- **Semantic mode**  
  Оценка качества при semantic retrieval.

## 5. Data Flow

- Вход: `question` + `ground truth` (если есть).
- Промежуточно: retrieval outputs, generated answer, evaluator signals.
- Выход: метрики качества + сравнительный результат по режимам.

## 6. Constraints

- Основной pipeline не изменяется.
- Evaluation работает отдельно от production-like request flow.
- Архитектура сохраняет минимальную сложность и учебный фокус.

## 7. Extensibility

- Возможность добавить новые метрики без перестройки базового evaluation потока.
- Возможность заменить evaluator (LLM-based или rule-based) через абстракцию.
