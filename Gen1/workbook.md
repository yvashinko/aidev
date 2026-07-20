# Workbook: ИИ в разработке

Этот workbook — краткое изложение курса для слушателя. Каждый модуль содержит ключевые идеи, практические задания и вопросы для самопроверки.

---

## Модуль 1. Принципы работы генеративного ИИ

**Ключевые идеи**
- LLM — параметрическая функция, предсказывающая следующий токен.
- Модель не знает истину; она аппроксимирует распределение.
- Галлюцинация — свойство, не баг.
- Quality gates: C-C-S-I-M (Correctness, Completeness, Safety, Idiomaticity, Maintainability).

**Практика**
- Провести 5 запросов к 2–3 моделям и сравнить ответы по шкале C-C-S-I-M.
- Найти минимум 2 потенциальные ошибки модели.

---

## Модуль 2. Prompt Engineering

**Ключевые идеи**
- Промпт = спецификация задачи, не вопрос.
- R-C-T-F-Q: Role, Context, Task, Format, Quality criteria.
- Few-shot (2–5 примеров) повышает стабильность.
- Reasoning-модели не нуждаются в явном CoT.

**Практика**
- Улучшить 3 «плохих» промпта до production-уровня.
- Создать шаблоны промптов для feature, bugfix, review, test, doc.

---

## Модуль 3. Генерация кода и MVP

**Ключевые идеи**
- Генерация сервиса = спецификация → план → инкремент с верификацией.
- `AGENTS.md` ≤ 200 строк; skills активируются по триггеру; hooks = production-код.
- Prompt-driven architecture drift — главный риск.
- AI provenance в PR.

**Практика**
- Собрать backend MVP из 3 endpoint-ов + тестов + README (см. `examples/task-service/`).
- Завести `AGENTS.md` и один skill для команды.

---

## Модуль 4. Debugging и анализ логов

**Ключевые идеи**
- AI — генератор гипотез, не замена инженерной диагностике.
- HDD: Reproduce → Collect → Hypothesize → Test → Decide.
- MRE ≤ 30 строк; регрессионный тест обязателен.
- Постмортем: timeline, root cause, action items.

**Практика**
- Разобрать инцидент «API отвечает 500 на часть запросов».
- Подготовить постмортем с SMART action items.

---

## Модуль 5. Тестирование и качество

**Ключевые идеи**
- Coverage ≠ качество; mutation score — более точная метрика.
- AAA + observable behavior.
- Property-based для инвариантов.
- Quality gates: линтер, type checker, SAST, SCA, secret-scan.

**Практика**
- Покрыть модуль из MVP unit + integration тестами.
- Найти тавтологию или mock-mirror в сгенерированных тестах.

---

## Модуль 6. Документация и архитектура

**Ключевые идеи**
- Doc-as-code; единый source of truth.
- README: quick start ≤ 15 мин.
- ADR: MADR + measurable Confirmation + Review trigger.
- Drift detection против doc rot.

**Практика**
- Подготовить README для MVP.
- Оформить ADR по спорному техническому решению.

---

## Модуль 7. Локальные модели

**Ключевые идеи**
- Локальная модель — governance/latency vs качество/операции.
- GGUF q4_K_M — стандарт dev; ~0.5 GB VRAM на 1B параметров.
- Ollama / LM Studio / vLLM — разные уровни абстракции.
- TCO учитывает железо, инженеров, лицензии.

**Практика**
- Развернуть Qwen2.5-Coder-7B через Ollama.
- Сравнить latency/качество с облачной моделью на одном промпте.

---

## Модуль 8. RAG

**Ключевые идеи**
- RAG даёт grounded контекст, не обучает модель.
- BGE-M3 / nomic-embed-text — рабочие embedding'и.
- Hybrid dense + BM25; reranker + citation grounding.
- Eval-suite: faithfulness, answer relevance, context recall/precision.

**Практика**
- Собрать RAG над `docs/` проекта.
- Построить 30-вопросный eval-сет и замерить baseline.
