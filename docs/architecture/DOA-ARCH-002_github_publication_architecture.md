---
Project: RAG MVP
Doc type: architecture
ID: DOA-ARCH-002
Status: draft
Date: 2026-04-19
Parent: DOA-IDEA-002
---

# Title

GitHub publication architecture

## 1. Overview

- Цель архитектуры — определить структуру публичного представления проекта.
- Архитектура не влияет на runtime системы.
- Архитектура описывает documentation & repository layer для публикации.

## 2. Publication Layers

1. **Entry Layer**
   - README.md.
   - First impression.
   - Краткое описание проекта и его назначения.

2. **Setup Layer**
   - Environment requirements.
   - Dependencies.
   - Installation steps.

3. **Execution Layer**
   - Как запускать backend.
   - Как открыть UI.
   - Demo flow.

4. **Structure Layer**
   - Описание структуры проекта.
   - Объяснение основных директорий.

5. **Legal Layer**
   - LICENSE.
   - Условия использования.

## 3. Repository Structure (public view)

- `README.md` (root).
- `LICENSE` (root).
- `requirements.txt` (если есть).
- `backend/`.
- `docs/`.

Текущая структура проекта не меняется; архитектура публикации только описывает публичный view.

## 4. README Architecture

Обязательные секции:

- Title + short description.
- Features (что умеет система).
- Architecture overview (очень кратко).
- Quick start (самый важный блок).
- Demo flow.
- Project structure.
- Limitations (важно для честности MVP).
- License.

## 5. Execution Contract (for user)

Минимальные шаги запуска:

1. Install dependencies.
2. Run backend.
3. Open UI.

Контракт запуска должен оставаться коротким и воспроизводимым (не более 3-5 шагов).

## 6. Constraints

- Не менять backend код.
- Не добавлять новые функции.
- Не усложнять setup.
- Demo-first baseline остаётся неизменным.
- Документация минимально достаточная для публичного старта.

## 7. Non-goals

- Docker.
- CI/CD.
- Deployment.
- Advanced documentation.
- API docs full-scale.
- Swagger polishing.

## 8. Output Artifacts

- `README.md`.
- `LICENSE`.
- (Опционально) уточнение `requirements.txt`.

## 9. Success Criteria

- Пользователь понимает проект менее чем за 2 минуты.
- Пользователь запускает проект менее чем за 10 минут.
- Для старта и демо не требуется читать исходный код.
