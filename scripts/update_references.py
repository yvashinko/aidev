#!/usr/bin/env python3
"""Update cross-references after splitting module 7."""

from pathlib import Path

REPLACEMENTS = {
    "Gen1/01-llm-fundamentals/01-chapter.md": [
        ("Модуль 7 (RAG как способ обхода ограничений контекста)", "Модуль 8 (RAG как способ обхода ограничений контекста)"),
        ("Модуль 7 (DPO/SFT поверх локальных моделей, RAG для свежей документации)", "Модули 7–8 (DPO/SFT поверх локальных моделей, RAG для свежей документации)"),
        ("Модуль 7 (RAG как основной antidote)", "Модуль 8 (RAG как основной antidote)"),
        ("Модуль 7 (Локальные модели и RAG)", "Модули 7–8 (Локальные модели и RAG)"),
    ],
    "Gen1/02-prompt-engineering/02-chapter.md": [
        ("Модуль 7 (RAG как способ выгрузить документацию из system)", "Модуль 8 (RAG как способ выгрузить документацию из system)"),
        ("Модуль 7 (RAG как продолжение этой главы)", "Модуль 8 (RAG как продолжение этой главы)"),
        ("Модуль 7 (RAG как замена «вечной сессии»)", "Модуль 8 (RAG как замена «вечной сессии»)"),
        ("Модуль 7 (Локальные модели и RAG)", "Модули 7–8 (Локальные модели и RAG)"),
    ],
    "Gen1/03-codegen-mvp/03-chapter.md": [
        ("Модуль 7 (Локальные модели и RAG)", "Модули 7–8 (Локальные модели и RAG)"),
    ],
    "Gen1/04-debugging-logs/04-chapter.md": [
        ("Модуль 7 (Локальные модели и RAG)", "Модули 7–8 (Локальные модели и RAG)"),
    ],
    "Gen1/05-testing-quality/05-chapter.md": [
        ("Модуль 7 (Локальные модели и RAG)", "Модули 7–8 (Локальные модели и RAG)"),
    ],
    "Gen1/06-docs-architecture/06-chapter.md": [
        ("Глава 7 (локальные модели — частичное решение cutoff-проблемы за счёт RAG над репо)", "Главы 7–8 (локальные модели — частичное решение cutoff-проблемы за счёт RAG над репо)"),
        ("Модуль 7 (Локальные модели для разработки и RAG)", "Модули 7–8 (Локальные модели и RAG)"),
    ],
    "Gen1/teaching-guide.md": [
        ("- `module-01-llm-fundamentals.md`\n- `module-02-prompt-engineering.md`\n- `module-03-codegen-mvp.md`\n- `module-04-debugging-logs.md`\n- `module-05-testing-quality.md`\n- `module-06-docs-architecture.md`\n- `module-07-local-models-rag.md`", "- `Gen1/01-llm-fundamentals/01-chapter.md` + `01-notes.md`\n- `Gen1/02-prompt-engineering/02-chapter.md` + `02-notes.md`\n- `Gen1/03-codegen-mvp/03-chapter.md` + `03-notes.md`\n- `Gen1/04-debugging-logs/04-chapter.md` + `04-notes.md`\n- `Gen1/05-testing-quality/05-chapter.md` + `05-notes.md`\n- `Gen1/06-docs-architecture/06-chapter.md` + `06-notes.md`\n- `Gen1/07-local-models/07-chapter.md` + `07-notes.md`\n- `Gen1/08-rag/08-chapter.md` + `08-notes.md`"),
    ],
}


def main() -> None:
    for rel_path, replacements in REPLACEMENTS.items():
        path = Path(rel_path)
        text = path.read_text(encoding="utf-8")
        for old, new in replacements:
            if old in text:
                text = text.replace(old, new)
                print(f"Updated {rel_path}: {old[:40]}... -> {new[:40]}...")
            else:
                print(f"Not found in {rel_path}: {old[:40]}...")
        path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
