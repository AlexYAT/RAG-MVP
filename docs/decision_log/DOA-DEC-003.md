---
Project: RAG MVP
Doc type: decision_log
ID: DOA-DEC-003
Status: accepted
Date: 2026-04-20
Parent: DOA-ARCH-003
---

# Title

Vector storage abstraction with ChromaDB as first implementation

## 1. Context

- Новый lifecycle направлен на развитие semantic RAG.
- Архитектура уже определяет vector storage как абстрактный компонент.
- Требуется зафиксировать concrete MVP direction без разрушения масштабируемости и без жесткой привязки pipeline к конкретному storage.

## 2. Decision

- Доступ к storage должен идти через абстракцию/интерфейс `VectorStore`.
- Pipeline и retriever должны зависеть от абстракции, а не от ChromaDB напрямую.
- ChromaDB выбран как первая concrete implementation для MVP.
- Замена storage должна оставаться возможной с минимальными изменениями вне storage-модуля.

## 3. Rationale

- Приоритет масштабируемости и управляемой эволюции архитектуры.
- Снижение связности между retrieval pipeline и storage-деталями.
- Сохранение чистой архитектуры с четкими границами ответственности.
- Быстрый MVP старт за счет готового локального persistent storage в рамках ChromaDB.
- Готовность к будущей замене storage без переписывания core pipeline.

## 4. Consequences

**Позитивные:**

- Легче заменить storage в будущих циклах.
- Pipeline остается стабильным при смене backend хранения.
- Повышается maintainability.
- Упрощается дальнейшее расширение.

**Негативные / trade-offs:**

- Появляется небольшой дополнительный слой абстракции.
- Требуется чуть больше проектной дисциплины при интеграции.
- Первая реализация потребует явного контракта interface + adapter.

## 5. Alternatives Considered

- Direct ChromaDB usage in pipeline — rejected.
- FAISS + custom metadata storage — not selected for current MVP due to higher integration complexity.

## 6. Non-Goals

- Не фиксировать полный API interface на этом этапе.
- Не описывать реализацию ingestion.
- Не выбирать future storage replacements.
- Не переходить к operational steps.
