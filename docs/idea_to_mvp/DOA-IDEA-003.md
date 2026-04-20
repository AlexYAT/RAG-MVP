---
Project: RAG MVP
Doc type: idea_to_mvp
ID: DOA-IDEA-003
Status: draft
Date: 2026-04-20
Parent: DOA-IMP-009
---

# Title

LLM-enhanced semantic RAG for quality improvement

## 1. Context

- Текущий MVP baseline зафиксирован в DOA-IMP-009 и является исходной точкой нового цикла.
- В текущей версии используется keyword-based retrieval.
- Генерация ответов реализована в controlled формате и система находится в demo-ready состоянии.

## 2. Problem

- Низкая семантическая релевантность при поиске.
- Сильная зависимость от keyword match.
- Ограниченное качество итоговых ответов при вариативных пользовательских формулировках.

## 3. Goal

- Повысить качество retrieval и generation.
- Использовать LLM как ключевой компонент нового baseline качества.

## 4. Scope

**Включено:**

- LLM-based embeddings.
- Semantic retrieval.
- Улучшенный prompt building.
- Улучшение качества ответов.

**Исключено:**

- Архитектура.
- Выбор технологий.
- Реализация ingestion pipeline.
- Оптимизация и масштабирование.

## 5. Success Criteria

- Релевантность поиска выше keyword baseline.
- Ответы более точные и связные.
- Демонстрируется использование LLM:
  - embeddings
  - generation

## 6. Constraints

- Учебный проект.
- Synthetic dataset допустим.
- Без production требований.

## 7. Non-Goals

- Hybrid search.
- Reranking.
- Caching.
- Distributed architecture.
- Performance tuning.
