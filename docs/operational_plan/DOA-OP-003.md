---
Project: RAG MVP
Doc type: operational_plan
ID: DOA-OP-003
Status: draft
Date: 2026-04-20
Parent: DOA-DEC-003
---

# Title

Implement VectorStore abstraction and ChromaDB first integration

## 1. Objective

- Реализовать storage abstraction.
- Внедрить ChromaDB как первую реализацию.
- Подключить abstraction в semantic retrieval path.

## 2. Scope

**Включить:**

- Определить минимальный контракт `VectorStore`.
- Создать ChromaDB-backed implementation.
- Подключить abstraction в retriever/pipeline.
- Обеспечить хранение embeddings + metadata + source linkage.
- Обеспечить local persistence.
- Сохранить совместимость с текущим MVP поведением там, где это возможно.
- Выполнить базовую функциональную проверку.

## 3. Out of Scope

- Alternative storage implementations.
- Reranking.
- Hybrid retrieval.
- Caching.
- Performance optimization.
- Quality evaluation framework.
- Production hardening.

## 4. Execution Steps

- **T01:** Inventory current retrieval/storage touchpoints.
- **T02:** Define minimal VectorStore contract.
- **T03:** Implement ChromaDB adapter.
- **T04:** Refactor retriever/pipeline to depend on abstraction.
- **T05:** Wire configuration and persistence path.
- **T06:** Run basic manual verification.
- **T07:** Create implementation snapshot after execution.

## 5. Acceptance Criteria

- Pipeline не зависит от ChromaDB напрямую.
- ChromaDB implementation работает через abstraction.
- Embeddings/chunks/metadata/source linkage сохраняются и читаются корректно.
- Semantic retrieval path проходит базовую проверку.
- Код запускается без нарушения основного MVP flow.

## 6. Risks

- Hidden direct dependencies in retrieval flow.
- Metadata/source mismatch.
- Persistence misconfiguration.
- Regression in existing answer flow.

## 7. Deliverables

- Code changes.
- OP execution evidence.
- Later IMP snapshot.
