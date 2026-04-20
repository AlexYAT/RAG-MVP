---
Project: RAG MVP
Doc type: architecture
ID: DOA-ARCH-003
Status: draft
Date: 2026-04-20
Parent: DOA-IDEA-003
---

# Title

Semantic RAG pipeline architecture with deferred vector storage decision

## 1. Overview

- Архитектура фиксирует переход от keyword retrieval к semantic retrieval.
- Для повышения качества используются LLM-компоненты на этапах embeddings и generation.
- Цель архитектуры — улучшить качество retrieval и итоговых ответов без фиксации конкретного storage-инструмента на данном этапе.

## 2. High-Level Flow

User Query  
→ Query Processing  
→ Embedding Generation  
→ Vector Storage Lookup  
→ Semantic Retrieval  
→ Context Assembly  
→ Prompt Construction  
→ LLM Generation  
→ Response

## 3. Components

- **Query Processor**  
  Принимает и нормализует запрос, подготавливает его для embedding и retrieval.

- **Embedding Layer**  
  Преобразует запрос в embedding-представление для semantic поиска.

- **Vector Storage**  
  Хранит embedding-представления и связанные данные для retrieval.

- **Retriever**  
  Выполняет semantic поиск релевантных фрагментов по embedding-запросу.

- **Context Builder**  
  Формирует контекст из retrieved фрагментов и источников.

- **Prompt Builder**  
  Строит structured input для generation на основе query и assembled context.

- **LLM Generator**  
  Формирует ответ на основе подготовленного prompt и предоставленного контекста.

- **Response Formatter**  
  Приводит результат к стабильному output-виду: ответ + источники + служебные признаки.

## 4. Vector Storage Notes

- Storage должен быть **persistent**.
- Storage должен поддерживать хранение **embeddings + metadata + source linkage**.
- Для MVP допустим **minimal local vector storage**.
- Конкретный инструмент хранения **не выбран** на этом этапе.
- Выбор concrete storage выносится в отдельный **ANALYZE/DEC**.
- В будущем допускается использование **ChromaDB-class local storage** как одного из кандидатов, без фиксации решения в этом документе.

## 5. Data Flow

- Query → embedding.
- Embedding → retrieval from vector storage.
- Retrieved chunks → context.
- Context + query → LLM.
- Output → answer + sources.

## 6. Interaction Rules

- Generation выполняется только на основе retrieved context.
- Ответ не формируется без retrieved evidence.
- При недостаточном контексте допускается fallback.

## 7. Constraints

- Без выбора технологий.
- Без реализации.
- Без ingestion деталей.
- Без оптимизации и масштабирования.

## 8. Extensibility

- Future storage decision.
- Future reranking.
- Future hybrid search.
- Future caching.
