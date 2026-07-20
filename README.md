# ИИ в разработке

Исходники практического курса (и одноимённой книги) по системному использованию генеративного ИИ в инженерной работе: от prompt engineering и генерации кода до отладки, тестирования, документации, локальных моделей и RAG.

## Аудитория

- Middle/Senior разработчики
- Тимлиды, техлиды, engineering-менеджеры
- Инженеры, переходящие от «спросил — вставил» к repeatable AI-assisted процессам

## Структура

- `Gen1/program.md` — программа курса
- `Gen1/teaching-guide.md` — методичка для преподавателя
- `Gen1/<модуль>/` — модули: глава-книга (`<NN>-chapter.md`) и конспект занятия (`<NN>-notes.md`)
- `templates/` — заготовки под спецификации, ADR, README, PR-описания
- `prompts/` — шаблоны промптов из глав
- `examples/task-service/` — сквозной учебный backend-проект для практики
- `Gen1/workbook.md` — learner-facing workbook с заданиями
- `Gen1/glossary.md` — общий глоссарий терминов
- `Gen1/bibliography.md` — общая библиография

## Как использовать

- Читать главы как книгу.
- Преподавателю — `teaching-guide.md` + `<NN>-notes.md`.
- Слушателям — `workbook.md` + практика в `examples/`.

## Сборка

Требуется `pandoc` (для PDF/HTML) и опционально `markdownlint-cli2` / `lychee`.

```bash
make pdf          # собрать PDF всех глав в dist/
make html         # собрать HTML всех глав в dist/
make lint         # проверить Markdown
make check-links  # проверить ссылки
```

PDF-файлы являются артефактами сборки и не хранятся в исходниках — только в `dist/`.

## Лицензия

CC BY-SA 4.0 — см. [`LICENSE`](LICENSE).
