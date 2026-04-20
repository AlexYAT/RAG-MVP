---
Project: RAG MVP
Doc type: operational_plan
ID: DOA-OP-010
Status: draft
Date: 2026-04-20
Parent: DOA-DEC-004
---

# Title

Implement RAG evaluation pipeline with hybrid evaluator

## 1. Objective

- Реализовать evaluation pipeline.
- Обеспечить сравнение keyword vs semantic.
- Внедрить hybrid evaluator.

## 2. Scope

**Включить:**

- Dataset loading (минимальный формат).
- Evaluation runner.
- Keyword retrieval mode.
- Semantic retrieval mode.
- Rule-based retrieval metrics.
- LLM-based answer evaluation.
- Metrics aggregation.
- Simple report output.

## 3. Out of Scope

- RAGAS.
- Сложные метрики.
- UI.
- CI/CD интеграция.
- Автоматизация.
- Оптимизация.

## 4. Execution Steps

- **T01:** define dataset format.
- **T02:** implement dataset loader.
- **T03:** implement evaluation runner.
- **T04:** implement retrieval modes switch.
- **T05:** implement rule-based metrics.
- **T06:** implement LLM judge evaluation.
- **T07:** implement aggregation.
- **T08:** implement report output.
- **T09:** run evaluation on sample dataset.
- **T10:** create implementation snapshot.

## 5. Acceptance Criteria

- Evaluation запускается на dataset.
- Есть сравнение keyword vs semantic.
- Retrieval метрики считаются.
- Answer оценивается через LLM.
- Формируется итоговый report.

## 6. Risks

- Inconsistent LLM judge.
- Dataset quality.
- Mismatch retrieval vs answer.
- Evaluation pipeline complexity.

## 7. Deliverables

- Code.
- Evaluation results.
- Implementation snapshot.
