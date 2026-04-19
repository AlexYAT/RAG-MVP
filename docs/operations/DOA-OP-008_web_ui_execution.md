---
Project: RAG MVP
Doc type: operational
ID: DOA-OP-008
Status: draft
Date: 2026-04-19
Parent: DOA-OP-001
---

# Title

Web UI execution

## 1. Context

- Документ — execution-шаг в рамках **DOA-OP-001**.
- Покрывает только **Phase 7 — Web UI**.
- Опирается на **DOA-DEC-001**, **DOA-ARCH-001** и **DOA-IMP-006**: backend scenario handling уже существует и готов как точка интеграции для UI.

## 2. Objective

- Добавить минимальный **Web UI** для демонстрации MVP.
- Подключить UI к существующему **scenario-level backend entrypoint**.
- Обеспечить сквозную demo-проверку от пользовательского ввода до ответа системы.

## 3. Scope

**Включить:**

- Минимальный web interface.
- Поле ввода запроса.
- Отправку запроса в backend.
- Отображение ответа.
- Отображение базовой истории взаимодействия в объёме, достаточном для демо.
- Отображение сценария / режима ответа, если это уже доступно из backend.
- Служебную проверку UI в локальном запуске.

**Не включать:**

- Сложный frontend framework setup сверх минимальной необходимости.
- Product-grade UX polishing.
- Сложное состояние клиента.
- Полноценный чат-менеджмент.
- Новые backend сценарии.
- Policy / security hardening.
- Production deployment.

## 4. Web UI Baseline

- UI минимальный и demo-oriented.
- UI использует существующий scenario-handling backend как основной источник ответа.
- UI не меняет backend-логику retrieval / generation / orchestration / scenarios.
- UI достаточен для демонстрации трёх сценариев MVP.
- UI должен позволять показать полный pipeline end-to-end.

## 5. Tasks

На уровне намерений, без кода:

1. Определить минимальную структуру Web UI.
2. Подключить UI к существующему backend endpoint сценарного уровня.
3. Реализовать ввод запроса и показ ответа.
4. Показать базовую историю запросов/ответов в рамках одной demo-сессии.
5. Обеспечить воспроизводимую локальную проверку UI.
6. Подтвердить, что через UI доступны FAQ / selection / overview paths.

## 6. Expected Result

- Пользователь может открыть Web UI локально.
- Пользователь может ввести запрос и получить ответ.
- UI демонстрирует связку с backend scenario handling.
- Полный MVP pipeline демонстрируется через web interface.

## 7. Validation

Критерии приёмки:

- UI открывается локально.
- Запрос из UI доходит до backend.
- Ответ отображается в UI.
- Можно воспроизвести как минимум по одному примеру для FAQ / selection / overview.
- Шаг не требует production deployment и не выходит за demo-first scope.

## 8. Out of Scope

- Расширенный frontend UX.
- Дополнительные сценарии.
- Multi-user state.
- Authentication / roles.
- Production frontend/backend deployment.
- Дальнейшие улучшения retrieval / generation.
