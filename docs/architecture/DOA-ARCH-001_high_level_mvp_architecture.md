---
Project: RAG MVP
Doc type: architecture
ID: DOA-ARCH-001
Status: draft
Date: 2026-04-19
Parent: DOA-IDEA-001
---

# High-level MVP architecture for demo-first RAG assistant

## 1. Purpose

Документ описывает high-level архитектуру demo-first MVP: роли компонентов, поток обработки запроса и сопоставление сценариев. Уровень описания — архитектурный; детали реализации, выбор технологий и контракты API намеренно не раскрываются.

## 2. Architectural Scope

**Покрывает архитектура:**

- Ingest синтетических документов.
- Обработка пользовательского запроса.
- Определение сценария.
- Retrieval.
- Генерация ответа.
- Уточняющий диалог.
- Web UI.

**Не покрывает:**

- Production scalability.
- Security hardening.
- Hybrid search.
- Reranking.
- Caching.
- Taxonomy filtering.
- Расширенные роли и доступы.

## 3. High-level Components

Описание на уровне ролей и ответственности.

### Web UI

- Точка входа пользователя.
- Отправка запроса.
- Показ ответа и истории.

### Orchestrator

- Центральная координация запроса.
- Маршрутизация по сценарию.
- Сбор результата.

### Query Classifier

- Определение сценария: FAQ, equipment selection, equipment overview.

### Dialogue Manager

- Ведение краткого контекста.
- Генерация уточняющих вопросов при нехватке входных данных.

### Retrieval Module

- Поиск релевантных фрагментов по knowledge base.
- Возврат top-k контекста с metadata.

### Generator

- Формирование ответа на основе запроса и retrieved context.

### Knowledge Base / Document Store

- Хранение синтетического датасета.
- Источник для ingest и retrieval.

### Ingest Pipeline

- Загрузка документов.
- Подготовка данных.
- Разбиение и индексация для retrieval.

## 4. High-level Flow

Последовательность:

1. Пользователь отправляет запрос через Web UI.
2. Orchestrator принимает запрос.
3. Classifier определяет сценарий.
4. Dialogue Manager решает, нужен ли уточняющий вопрос.
5. Retrieval получает релевантный контекст.
6. Generator формирует ответ.
7. Orchestrator возвращает результат в UI.

**Дополнения по сценариям:**

- Для **selection** допускаются дополнительные уточняющие шаги до финального ответа.
- Для **overview** допустим более структурированный путь summarization при формировании ответа.

## 5. Scenario Mapping

- **FAQ** → classifier → retrieval → generator
- **Selection** → classifier → dialogue manager → retrieval → generator
- **Overview** → classifier → retrieval → generator

## 6. Architectural Constraints

- Demo-first.
- Synthetic dataset.
- Minimum viable complexity.
- Web UI обязателен.
- Ограниченный UX допустим.
- Архитектура должна оставлять расширяемость для будущих улучшений.

## 7. Extension Points

Без детальной проработки — возможные направления развития:

- Hybrid search.
- Reranking.
- Caching.
- Taxonomy filtering.
- Policy / security layer.
- Richer role model.

## 8. Out of Scope

Повторная фиксация границ:

- No production guarantees.
- No scalability design.
- No security model in detail.
- No technology lock-in.
- No vendor-specific implementation choices.
