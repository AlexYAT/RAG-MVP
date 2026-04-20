---
Project: RAG MVP
Doc type: implementation_snapshot
ID: DOA-IMP-003
Status: accepted
Date: 2026-04-20
Parent: DOA-OP-003
---

# Title

Semantic RAG baseline with VectorStore abstraction and ChromaDB

## 1. Summary

- Реализован semantic retrieval слой.
- Добавлен VectorStore abstraction.
- ChromaDB используется как первая реализация storage.
- Сохранен fallback на keyword retrieval.
- Generation pipeline продолжает работать без изменения базового flow.

## 2. Implemented Components

- VectorStore interface (базовый контракт доступа к storage).
- ChromaVectorStore adapter (первая concrete implementation).
- Обновленный retrieval слой с использованием abstraction.
- Конфигурация через env-параметры для storage path и collection.
- Persistent storage embeddings и связанных metadata/source linkage.

## 3. Integration Points

- VectorStore используется в retrieval-пути как основной способ доступа к semantic storage.
- Retriever/pipeline зависят от abstraction, а не от ChromaDB напрямую.
- Fallback подключен в retrieval слое: при недоступности semantic path сохраняется keyword-based путь.

## 4. Verification

- Сервер запускается корректно после изменений.
- Протестированы минимум 2 запроса через рабочий flow.
- Ответы возвращаются корректно, сценарный путь остается рабочим.

## 5. Known Limitations

- Нет reranking.
- Нет hybrid search.
- Нет evaluation framework.
- Нет optimization/performance tuning.

## 6. Notes

- Chroma используется как MVP storage baseline.
- Storage может быть заменен в будущем без изменения основного pipeline.

## Naming Note

Этот файл создан как canonical naming версия DOA-IMP-003.

Причина:
- исходный файл был создан без slug в имени
- это нарушает установленный паттерн DOA-IMP-XXX_<slug>.md

Исходный файл сохранён без изменений согласно create-only политике.
