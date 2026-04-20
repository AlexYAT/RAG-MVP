---
Project: RAG MVP
Doc type: decision_log
ID: DOA-DEC-004
Status: accepted
Date: 2026-04-20
Parent: DOA-ARCH-004
---

# Title

Hybrid evaluator strategy for RAG evaluation

## 1. Context

- Evaluation cycle требует измерения retrieval quality, answer quality и hallucinations.
- Архитектура уже задаёт evaluator как replaceable abstraction.
- Требуется решение, которое остаётся масштабируемым и при этом даёт содержательную оценку качества.

## 2. Decision

- Выбрана **Hybrid evaluator strategy**.
- Retrieval evaluation выполняется **rule-based** способом.
- Answer quality evaluation выполняется через **LLM-as-judge**.
- Hallucination-oriented judgement относится к **LLM-based evaluator path**.
- Результаты агрегируются в **единый unified report**.

## 3. Rationale

- Rule-based retrieval metrics детерминированы и лучше масштабируются.
- LLM judge лучше подходит для семантической оценки answer quality и проверки hallucinations.
- Hybrid подход балансирует воспроизводимость, стоимость и глубину оценки.
- Решение сохраняет архитектурную гибкость evaluator слоя.

## 4. Consequences

**Позитивные:**

- Retrieval evaluation лучше масштабируется.
- Answer evaluation остаётся семантически содержательной.
- Evaluation architecture сохраняет extensibility.
- Сравнение keyword vs semantic остаётся практичным.

**Негативные / trade-offs:**

- Растёт orchestration complexity.
- Нужно поддерживать два evaluation path.
- LLM-based часть менее детерминирована, чем rule-based метрики.

## 5. Alternatives Considered

- Full LLM-as-judge — rejected due to cost/latency/scalability concerns.
- Full rule-based evaluation — rejected due to weak answer-quality and hallucination assessment.

## 6. Non-Goals

- Не фиксировать конкретные judge prompts.
- Не фиксировать конкретные metrics formulas.
- Не выбирать конкретные библиотеки/frameworks.
- Не переходить к implementation steps.
