---
Project: RAG MVP
Doc type: decision
ID: DOA-DEC-002
Status: accepted
Date: 2026-04-19
Parent: DOA-ARCH-002
---

# Title

Publication strategy (LICENSE and README)

## 1. Context

- Документ фиксирует решения для GitHub publication readiness.
- Основан на DOA-IDEA-002 и DOA-ARCH-002.
- Определяет ключевые choices перед реализацией.

## 2. Decision: LICENSE

### Options considered

- MIT
- Apache 2.0
- No license

### Decision

Выбран MIT License.

### Rationale

- Простота и понятность.
- Широкое распространение.
- Подходит для demo / portfolio проекта.
- Не создаёт барьеров для использования.

## 3. Decision: README strategy

### Options considered

- Minimal demo-first
- Technical deep dive
- Marketing-heavy

### Decision

Выбран minimal demo-first подход с архитектурной структурой из DOA-ARCH-002.

### Rationale

- Быстрое понимание проекта (<2 минуты).
- Быстрый запуск (<10 минут).
- Соответствие цели demo MVP.
- Баланс между простотой и информативностью.

## 4. Implications

- README должен быть кратким и ориентированным на запуск.
- Quick start — центральный элемент.
- Детали архитектуры — только high-level.
- LICENSE должен быть добавлен в root проекта.

## 5. Non-goals

- Юридическая сложная лицензия.
- Полноценная техническая документация.
- Marketing packaging.
