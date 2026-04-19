---
Project: RAG MVP
Doc type: decision_log
ID: DOA-DEC-001
Status: draft
Date: 2026-04-19
Parent: DOA-ARCH-001
---

# Title

MVP architecture baseline decisions

## 1. Context

Проект стартует как demo-first RAG MVP. **DOA-IDEA-001** и **DOA-ARCH-001** уже задали границы и high-level архитектуру. На этом шаге фиксируются ключевые baseline decisions, чтобы дальше переходить к operational planning без расплывчатости по scope и приоритетам.

## 2. Decision 1 — Demo-first scope

**Решение:** MVP строится как демонстрационная система; реализуется только минимально достаточный scope; остальные возможности декларируются как future extension points, а не как обязательства первого цикла.

## 3. Decision 2 — Synthetic dataset

**Решение:** В MVP используется синтетический dataset. Причины: скорость итерации, управляемость содержимого, предсказуемость демо. Реальные данные не являются prerequisite для первого цикла.

## 4. Decision 3 — Scenario set for MVP

**Решение:** MVP ограничен тремя сценариями: FAQ, equipment selection, equipment overview. Расширение набора сценариев выносится за пределы текущего baseline.

## 5. Decision 4 — Interaction channel

**Решение:** Обязательный пользовательский канал MVP — Web UI; UI допускается минимальным и demo-oriented. Другие каналы доступа не входят в текущий baseline.

## 6. Decision 5 — Retrieval baseline

**Решение:** Retrieval в MVP — базовый vector-based retrieval. Hybrid search, reranking, caching, taxonomy filtering не входят в первый baseline. Metadata у фрагментов сохраняется как foundation для будущего усложнения retrieval.

## 7. Decision 6 — Orchestration model

**Решение:** Система использует scenario-based orchestration: classifier, dialogue handling, retrieval и generation образуют базовую логику координации в духе ARCH. Детализация внутренней реализации остаётся вне этого DEC.

## 8. Consequences

- Scope становится управляемым и проверяемым по сценариям.
- Возможен быстрый переход к implementation / operational planning без переобсуждения базовых границ.
- Снижается риск premature complexity.
- Архитектура остаётся расширяемой; MVP не перегружается нефункциональными требованиями первого цикла.

## 9. Alternatives Considered

- **Real dataset from start** — дольше путь к первому демо и выше зависимости от внешних данных; противоречит выбранному synthetic baseline.
- **Multi-channel access in MVP** — расширяет surface без необходимости для первого цикла; baseline ограничивает канал Web UI.
- **Advanced retrieval stack in first iteration** — ломает минимальный retrieval baseline; hybrid/rerank/cache отложены осознанно.
- **Broader scenario coverage from day one** — размывает фокус и усложняет критерии готовности; три сценария уже зафиксированы на уровне IDEA/ARCH.

## 10. Non-goals

В этом документе **не** фиксируются:

- Конкретные технологии.
- Operational tasks и планы работ.
- API контракты.
- Детали prompt / model tuning.
