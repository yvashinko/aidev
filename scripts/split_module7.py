#!/usr/bin/env python3
"""Split Gen1/07-local-models-rag into 07-local-models and 08-rag."""

import re
from pathlib import Path

ROOT = Path("Gen1")
SRC = ROOT / "07-local-models-rag" / "07-chapter.md"

# 1-based line numbers of section headings from grep.
sections = {
    "intro": (1, 31),
    "7.1": (31, 119),
    "7.2": (119, 211),
    "7.3": (211, 557),
    "7.4": (557, 703),
    "7.5": (703, 839),
    "7.6": (839, 1060),
    "7.7": (1060, 1202),
    "7.8": (1202, 1692),
    "7.9": (1692, 1884),
    "7.10": (1884, 2044),
    "7.11": (2044, 2200),
    "7.12": (2200, 2447),
    "tail": (2447, 3015),
}


def get_lines(path: Path, start_1based: int, end_1based: int) -> list[str]:
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return lines[start_1based - 1 : end_1based - 1]


# Mapping from old section number to (target_module, new_number).
# Tail sections are mapped to the same module as the file they appear in.
mapping_7 = {
    1: (7, 1),
    2: (7, 2),
    3: (7, 3),
    4: (7, 4),
    5: (7, 5),
    6: (8, 1),
    7: (8, 2),
    8: (8, 3),
    9: (8, 4),
    10: (8, 5),
    11: (7, 6),
    12: (8, 6),
    13: (7, 7),
    14: (7, 8),
    15: (7, 9),
    16: (7, 10),
    17: (7, 11),
}

mapping_8 = {
    1: (7, 1),
    2: (7, 2),
    3: (7, 3),
    4: (7, 4),
    5: (7, 5),
    6: (8, 1),
    7: (8, 2),
    8: (8, 3),
    9: (8, 4),
    10: (8, 5),
    11: (7, 6),
    12: (8, 6),
    13: (8, 7),
    14: (8, 8),
    15: (8, 9),
    16: (8, 10),
    17: (8, 11),
}


def renumber(text: str, file_module: int, full_mapping: dict[int, tuple[int, int]], present_sections: list[int]) -> str:
    heading_mapping = {
        old: new for old, (mod, new) in full_mapping.items()
        if mod == file_module and old in present_sections
    }

    def heading_repl(m: re.Match) -> str:
        level = m.group(1)
        old = int(m.group(2))
        new = heading_mapping.get(old, old)
        return f"{level} {file_module}.{new}"

    text = re.sub(r"^(#{2,})\s+7\.(\d+)", heading_repl, text, flags=re.MULTILINE)

    def ref_repl(m: re.Match) -> str:
        old = int(m.group(1))
        suffix = m.group(2)
        mod, new = full_mapping.get(old, (7, old))
        return f"§{mod}.{new}{suffix}"

    text = re.sub(r"§7\.(\d+)([a-z]?)", ref_repl, text)
    return text


def build(
    file_module: int,
    body_sections: list[str],
    mapping: dict[int, tuple[int, int]],
    intro: str,
    final_thought: str,
) -> str:
    parts = [intro]
    for sec in body_sections:
        parts.extend(get_lines(SRC, sections[sec][0], sections[sec][1]))
    parts.extend(get_lines(SRC, sections["tail"][0], sections["tail"][1]))
    text = "".join(parts)

    present = [int(sec.split(".")[1]) for sec in body_sections]
    # Tail sections are 13-17 and always present.
    present += [13, 14, 15, 16, 17]

    text = renumber(text, file_module, mapping, present)
    text = text.replace("Глава 7", f"Глава {file_module}")
    text = re.sub(
        r"> \*\*Главная мысль главы\.\*\*.*$",
        final_thought.strip(),
        text,
        flags=re.DOTALL,
    )
    return text


intro_7 = """# Глава 7. Локальные модели для разработки

> «Локальная модель — не "бесплатный облачный AI", а инженерный компромисс между governance, latency, стоимостью владения и качеством».

## Зачем эта глава

Главы 1–6 построили дисциплину работы с frontier-моделями. Эта глава отвечает на вопрос: что делать, когда код, секреты или PII не могут покидать периметр, или когда облачная латентность и стоимость неприемлемы. Мы рассмотрим open-weights LLM, инструменты запуска (Ollama, LM Studio, vLLM), квантование, выбор железа, локальный code review и инженерную экономику self-hosted стека.

Целевой уровень — middle/senior, готовый к командным trade-off'ам между облаком и локальным размещением.

---
"""

intro_8 = """# Глава 8. RAG: Retrieval-Augmented Generation

> «RAG — не способ обучить модель вашим данным; это способ дать ей контекст, который уже есть в репозитории».

## Зачем эта глава

Локальные и облачные модели сталкиваются с общей проблемой: knowledge cutoff и отсутствие специфики вашего проекта. Эта глава посвящена RAG — инженерному паттерну поиска по документации и коду с последующей генерацией ответа. Мы разберём embedding-модели, chunking, vector stores, hybrid search, reranking, code-RAG, evaluation suite, MCP и безопасность retrieval-систем.

Целевой уровень — middle/senior, знакомый с базовым LLM-стеком и желающий построить grounded AI-ассистента над внутренними знаниями.

---
"""

final_7 = """> **Главная мысль главы.** Локальные модели — инженерный компромисс, а не «бесплатный облачный AI». Они закрывают governance и latency, ценой качества и операционной сложности. Выбор между облаком и self-hosted строится на измеримых критериях: data classification, TCO, latency, качество на ваших задачах и лицензионная политика. Инструменты вроде Ollama и LM Studio снижают порог входа, но не отменяют дисциплину: verifier-loop, versioned rules, eval и security gates остаются такими же, как с frontier-моделями."""

final_8 = """> **Главная мысль главы.** RAG — не обучение модели и не устранение галлюцинаций; это способ давать модели grounded контекст из ваших документов и кода. Production-grade RAG — pipeline из chunking, embedding, hybrid search, reranking, citation grounding и evaluation suite. Без регулярного измерения качества RAG быстро превращается в уверенно звучащий чёрный ящик. Команда, которая владеет этим pipeline'ом, получает AI-ассистента, который действительно опирается на внутренние знания, а не на усреднённый индустриальный guess."""


def main() -> None:
    (ROOT / "07-local-models").mkdir(exist_ok=True)
    (ROOT / "08-rag").mkdir(exist_ok=True)

    text_7 = build(7, ["7.1", "7.2", "7.3", "7.4", "7.5", "7.11"], mapping_7, intro_7, final_7)
    text_8 = build(8, ["7.6", "7.7", "7.8", "7.9", "7.10", "7.12"], mapping_8, intro_8, final_8)

    (ROOT / "07-local-models" / "07-chapter.md").write_text(text_7, encoding="utf-8")
    (ROOT / "08-rag" / "08-chapter.md").write_text(text_8, encoding="utf-8")

    print("Created Gen1/07-local-models/07-chapter.md")
    print("Created Gen1/08-rag/08-chapter.md")


if __name__ == "__main__":
    main()
