#!/usr/bin/env bash
# scripts/md-to-pdf.sh — конвертация одного Markdown-файла в PDF.
# Использует pandoc + xelatex (как и основная сборка курса).
#
# Примеры:
#   scripts/md-to-pdf.sh research/2026-07-ai-landscape.md
#   scripts/md-to-pdf.sh Gen1/01-llm-fundamentals/01-chapter.md dist/01-chapter.pdf

set -euo pipefail

usage() {
    echo "Usage: $0 <input.md> [output.pdf]"
    exit 1
}

if [ "$#" -lt 1 ]; then
    usage
fi

INPUT="$1"

if [ "$#" -ge 2 ]; then
    OUTPUT="$2"
else
    OUTPUT="${INPUT%.md}.pdf"
fi

if [ ! -f "$INPUT" ]; then
    echo "Ошибка: файл не найден: $INPUT" >&2
    exit 1
fi

for cmd in pandoc xelatex; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        echo "Ошибка: '$cmd' не установлен." >&2
        echo "Установите pandoc и LaTeX (xelatex): https://pandoc.org/installing.html" >&2
        exit 1
    fi
done

mkdir -p "$(dirname "$OUTPUT")"

pandoc "$INPUT" -o "$OUTPUT" \
    --pdf-engine=xelatex \
    -V geometry:margin=2.5cm \
    -V colorlinks=true \
    --standalone

echo "PDF создан: $OUTPUT"
