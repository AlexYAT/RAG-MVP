---
Project: RAG MVP
Doc type: idea_to_mvp
ID: DOA-IDEA-004
Status: draft
Date: 2026-04-20
Parent: DOA-IMP-003
---

# Title

RAG evaluation cycle for quality measurement

## 1. Goal

- Ввести систему оценки качества RAG.

## 2. Scope

**Включить:**

- Тестовый набор вопросов.
- Оценку релевантности retrieval.
- Оценку качества ответа.
- Анализ hallucinations.
- Сравнение keyword vs semantic retrieval.

## 3. Non-Goals

- Не улучшать retrieval.
- Не добавлять reranking.
- Не менять pipeline.
- Не оптимизировать производительность.

## 4. Success Criteria

- Можно измерить качество retrieval.
- Можно измерить качество answer.
- Можно сравнивать разные подходы.

## 5. Constraints

- Учебный проект.
- Допускается использование LLM для оценки.
- Простота важнее production-ready решения.
