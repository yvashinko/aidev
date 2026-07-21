# Срез AI-инструментов разработки: июль 2026

**Статус:** отдельная заметка для преподавателей и авторов курса. Не входит в основную книгу.  
**Дата среза:** 2026-07-20.  
**Цель:** понять, какие модели и инструменты вышли недавно, как с ними работать и что из этого релевантно для студентов в Беларуси.

## TL;DR

- Главный тренд 2025–2026 — переход от «автодополнения строки» к полноценным **агентам кодирования** (Codex, Claude Code, Cursor agents, GitHub Copilot agents), которые выполняют задачи в фоне, запускают тесты и создают PR.
- Лидеры frontier: **OpenAI GPT-5.6 Sol/Terra/Luna**, **Anthropic Claude Fable 5 / Sonnet 5**, **Google Gemini 2.5 Pro/Flash**. Они дорогие, быстро меняются и **официально недоступны в Беларуси**.
- Параллельно растёт мощный пласт **open-weight моделей**: **Kimi K3**, **Qwen 3.5/3.6/3.8**, **Gemma 4**, **Llama 4**, **Nemotron 3 Super**, **DeepSeek V3/R1**. Их можно запускать локально через Ollama / LM Studio / llama.cpp.
- **MCP (Model Context Protocol)** становится стандартом подключения агентов к внешним инструментам, базам и API.
- Для аудитории в Беларуси критично строить обучение вокруг **open-source и локального инференса**, потому что доступ к OpenAI, Anthropic и Google AI Studio/Gemini API ограничен санкциями и Terms of Service.

---

## 1. Агенты и IDE-инструменты

### OpenAI Codex

- Что это: облачный software-engineering агент, запущенный в research preview весной 2025.
- Модель: `codex-1` на базе семейства `o3`, оптимизирована для программирования.
- Как работает: задача создаётся в ChatGPT, агент выполняет её в изолированном cloud-sandbox с клоном репозитория, может читать/писать файлы, запускать тесты, линтеры, выдавать diff и PR.
- Важная деталь: поддерживает `AGENTS.md` — файл с инструкциями для агента внутри репозитория (аналог README для человека).
- Доступ: ChatGPT Pro/Enterprise/Business, позже Plus и Edu. **Беларусь отсутствует в списке поддерживаемых стран OpenAI API** [Supported countries and territories | OpenAI API](https://platform.openai.com/docs/supported-countries).

### Anthropic Claude Code

- Что это: агент кодирования от Anthropic, доступный в терминале, VS Code, JetBrains, десктоп-приложении и вебе.
- Модели: Claude Fable 5 / Sonnet 5 / др.
- Особенности: понимает весь codebase, работает с несколькими файлами, поддерживает `CLAUDE.md` для персистентных инструкций, MCP-серверы.
- Доступ: требуется подписка Anthropic или Anthropic Console. Terms of Service прямо запрещают использование в странах, попадающих под санкции США [Anthropic Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms). **Беларусь — под санкциями, официальный доступ отсутствует.**

### GitHub Copilot

- Что это: встроенный в IDE AI pair programmer (VS Code, JetBrains, Vim/Neovim, Visual Studio).
- Возможности: inline completions, chat, Copilot Edits, Copilot Workspace, code review, CLI.
- Тарификация: есть бесплатный tier (2000 completions + 50 chat requests/месяц), Pro/Pro+/Max/Enterprise. С июня 2026 code review тратит GitHub Actions минуты.
- Доступ: GitHub Copilot входит в GitHub Student Developer Pack, но оформление платной подписки из Беларуси может быть затруднено из-за ограничений на приём платежей. Базовый GitHub доступен, но **нет гарантии беспрепятственного доступа к платным AI-функциям.**

### Cursor

- Что это: IDE на базе VS Code, заточенная под AI-агентов (Composer, Bugbot, Agents).
- Есть бесплатный **Hobby**-план с ограниченным числом Agent-запросов; платные планы от $16/мес.
- Купила Continue.dev — значит, экосистема консолидируется.
- Для Беларуси: регистрация возможна, но оплата Pro из-за белорусских карт с большой вероятностью не пройдёт.

### Альтернативы для ручной работы

- **Aider** — open-source терминальный ассистент, работает с любой моделью (Claude, OpenAI, DeepSeek, local). Автоматически коммитит изменения, строит карту codebase.
- **Cline / Roo Code** — open-source VS Code-расширения, поддерживают собственные API-ключи и локальные модели.
- **Continue** — был куплен Cursor; дальнейшая судьба неопределенна.

---

## 2. Open-weight / локальные модели

Лето 2026 — пик open-weight моделей. Их можно скачивать через Ollama, Hugging Face, ModelScope и запускать локально без привязки к стране.

| Модель / семейство | Кто выпустил | Что важно для кода | Размеры (примерные) |
|---|---|---|---|
| **Kimi K3 / K2.7 Code** | Moonshot AI | Frontier-уровень кодирования, agentic workflows, open-weight (веса K3 планируются к публикации 27 июля 2026) | 2.8T params (K3), младшие версии меньше |
| **Qwen 3.5 / 3.6 / 3.8** | Alibaba | Сильные мультимодальные и coding-способности, открытые веса | от 0.8B до 122B |
| **Gemma 4** | Google | Frontier-уровень при малых размерах, coding, multimodal | 12B / 26B / 31B |
| **Llama 4 Scout / Maverick** | Meta | MoE, multimodal, но большие; Scout — 109B total / 17B active | 109B / 400B |
| **Nemotron 3 Super** | NVIDIA | 120B MoE, 12B active, для multi-agent приложений | 120B |
| **DeepSeek V3 / R1 / Coder** | DeepSeek | Очень сильные для кода и reasoning; требуют мощного железа | V3 ~671B MoE |
| **Qwen 2.5 Coder** | Alibaba | Проверенный выбор для локального кодирования на ноутбуке | 7B / 14B / 32B |
| **Gemma 3 / 4, CodeGemma** | Google | Лёгкие, быстрые, хорошо квантованные | 4B–27B |
| **Mistral / Codestral** | Mistral AI | Европейский вендор, хорош для кода | разные |

**Практика для студентов:**

- На обычном ноутбуке без GPU: Qwen 2.5 Coder 7B/14B, Gemma 4 12B (квантованные), DeepSeek R1 7B/14B distill.
- На машине с 16–32 GB RAM и GPU (RTX 3060/4060): Qwen 2.5 Coder 32B, DeepSeek Coder V2 16B/236B (квант), Gemma 4 26B.
- Инструменты: **Ollama** (самый простой), **LM Studio** (GUI), **llama.cpp** / **koboldcpp** (максимальный контроль), **text-generation-webui**.

---

## 3. Протоколы и инфраструктура

### Model Context Protocol (MCP)

- Разработан Anthropic, но поддерживается многими инструментами.
- Дает агентам стандартный способ подключаться к внешним источникам: базы данных, GitHub, Slack, календари, собственные API.
- Летом 2026 выходит обновление спецификации с **stateless session IDs**, что упрощает масштабирование MCP-серверов за load balancer.
- **Почему важно для курса:** умение писать простой MCP-сервер или правильно конфигурировать агента с MCP — уже базовый навык, аналогичный написанию CLI-утилиты.

### AGENTS.md / CLAUDE.md / .cursorrules

- Файлы инструкций в репозитории, которые читают агенты Codex, Claude Code, Cursor.
- Содержат: как запускать тесты, какая структура проекта, правила стиля, ограничения.
- Это продолжение идей prompt engineering и context engineering из курса.

---

## 4. Что это меняет для курса

Основная книга (`Gen1/`) фокусируется на фундаментальных навыках: prompt engineering, генерация кода, отладка, тестирование, документация, локальные модели, RAG. Эти навыки не устарели — наоборот, они стали **базой** для работы с агентами.

Что стоит донести студентам:

1. **Агент — не замена разработчика, а инструмент с высокой планкой review.** Код по-прежнему нужно читать, тестировать, запускать.
2. **Качество входных инструкций остаётся ключевым.** `AGENTS.md`, чёткое ТЗ, разбиение задачи — это prompt engineering в новой форме.
3. **Локальные open-weight модели — рабочий путь там, где недоступны frontier API.** Умение запускать Qwen/Gemma/DeepSeek через Ollama даёт независимость.
4. **MCP и tool use — новый слой интеграции.** Стоит добавить хотя бы демонстрацию или одну практику.
5. **Экономика токенов и latency имеет значение.** Выбор модели (Sol vs Terra vs Luna, Qwen 7B vs 32B) — это trade-off цена/скорость/качество.

---

## 5. Ограничения для студентов в Беларуси (факты)

| Сервис | Официальный статус для Беларуси | Источник |
|---|---|---|
| OpenAI API / ChatGPT / Codex | **Не поддерживается.** Беларусь отсутствует в списке стран. | [OpenAI Supported countries and territories](https://platform.openai.com/docs/supported-countries) |
| Anthropic Claude / Claude Code | **Запрещено ToS.** Terms запрещают доступ в санкционные страны. | [Anthropic Commercial Terms of Service, раздел M.8](https://www.anthropic.com/legal/commercial-terms) |
| Google AI Studio / Gemini API | **Недоступен.** Беларуси нет в списке регионов. | [Available regions for Google AI Studio and Gemini API](https://ai.google.dev/gemini-api/docs/available-regions) |
| GitHub Copilot (платный) | Базовый GitHub работает, но **покупка/подписка может блокироваться** платёжными системами. Student Pack есть, но доступность Copilot-части зависит от верификации и санкционной политики в конкретный момент. | [GitHub Terms of Service](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service) |
| Ollama, LM Studio, Aider, local models | **Доступны.** Скачивание весов и запуск локально не требуют аккаунта в санкционном сервисе. | — |

> **Юридическая оговорка:** доступ через VPN или регистрацию чужих аккаунтов часто нарушает Terms of Service соответствующих сервисов. В учебном контексте это создаёт риски для студентов и для университета.

---

## 6. Источники

- OpenAI. *Introducing Codex* (2025-04-16) — через [OpenAI Codex announcement](https://openai.com/index/introducing-codex/).
- OpenAI. *GPT-5.6: Frontier intelligence that scales with your ambition* (2026) — [OpenAI GPT-5.6](https://openai.com/index/gpt-5-6/).
- Anthropic. *Overview — Claude Code Docs* (2026) — [Claude Code Docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview).
- Anthropic Newsroom: Claude Sonnet 5, Fable 5, Claude Code (2026) — [Anthropic News](https://anthropic.com/news).
- GitHub. *GitHub Copilot FAQ / Pricing* (2026) — [GitHub Copilot](https://github.com/features/copilot).
- The Verge. *China delivers a one-two punch to America’s AI dominance* (2026-07-20) — [The Verge](https://www.theverge.com/ai-artificial-intelligence/967781/chinese-ai-models-open-source-moonshot-kimi-k3-alibaba-qwen).
- TechCrunch. *OpenAI is scared of open-weight models. Should the US be?* (2026-07-20) — [TechCrunch](https://techcrunch.com/2026/07/20/openai-is-scared-of-open-weight-models-should-the-us-be/).
- TechCrunch. *AI’s most important protocol is getting a little bit easier to use* (2026-07-20) — [TechCrunch](https://techcrunch.com/2026/07/20/ais-most-important-protocol-is-getting-a-little-bit-easier-to-use/).
- Ollama Library (2026-07-20) — [Ollama Models](https://ollama.com/search).

---

## 7. Рекомендация авторам курса

Не встраивать этот срез в основные главы «как есть» — модели меняются быстро. Лучше:

- Добавить в `Gen1/bibliography.md` ссылку на эту заметку.
- В `Gen1/program.md` отметить, что модули 07 (Local models) и 08 (RAG) являются **базой для работы в условиях ограниченного доступа к frontier API**.
- При обновлении курса добавить раздел «Агенты кодирования» как отдельный необязательный модуль или приложение, с фокусом на **принципы** (decomposition, verification, AGENTS.md, MCP), а не на конкретный проприетарный инструмент.
