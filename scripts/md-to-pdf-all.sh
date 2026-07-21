#!/usr/bin/env bash
# scripts/md-to-pdf-all.sh — рекурсивная конвертация всех Markdown-файлов в PDF.
# Для каждого файла вызывает scripts/md-to-pdf.sh.
#
# По умолчанию PDF сохраняется рядом с исходным .md (например, README.md → README.pdf).
# Опция --dist сохраняет PDF в единую директорию с сохранением структуры.
#
# Примеры:
#   scripts/md-to-pdf-all.sh
#   scripts/md-to-pdf-all.sh --dist
#   scripts/md-to-pdf-all.sh --dist dist/pdf

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MD_TO_PDF="$SCRIPT_DIR/md-to-pdf.sh"

DIST_MODE=false
OUTPUT_DIR=""

usage() {
    echo "Usage: $0 [--dist [dir]]"
    echo ""
    echo "  По умолчанию PDF сохраняется рядом с каждым .md файлом."
    echo "  --dist [dir] сохранять PDF в указанную директорию (по умолчанию: dist)"
    echo "               с сохранением относительной структуры каталогов."
    exit 1
}

while [ $# -gt 0 ]; do
    case "$1" in
        --dist)
            DIST_MODE=true
            if [ $# -ge 2 ] && [[ "$2" != --* ]]; then
                OUTPUT_DIR="$2"
                shift
            else
                OUTPUT_DIR="dist"
            fi
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            usage
            ;;
    esac
done

EXCLUDES=(
    -not -path './.git/*'
    -not -path './dist/*'
    -not -path './.venv/*'
    -not -path './venv/*'
    -not -path './node_modules/*'
    -not -path './__pycache__/*'
    -not -path './.pytest_cache/*'
    -not -path './.specstory/*'
    -not -path './.cursor/*'
    -not -path './.aider*'
)

TOTAL=0
OK=0
FAIL=0

process_file() {
    local file="$1"
    local out="$2"
    TOTAL=$((TOTAL + 1))
    if "$MD_TO_PDF" "$file" "$out" >/dev/null 2>&1; then
        echo "  OK: $out"
        OK=$((OK + 1))
    else
        echo "FAIL: $file"
        FAIL=$((FAIL + 1))
    fi
}

if [ "$DIST_MODE" = true ]; then
    mkdir -p "$OUTPUT_DIR"
    while IFS= read -r -d '' file; do
        rel="${file#./}"
        out="$OUTPUT_DIR/${rel%.md}.pdf"
        mkdir -p "$(dirname "$out")"
        process_file "$file" "$out"
    done < <(find . -type f -name '*.md' "${EXCLUDES[@]}" -print0)
else
    while IFS= read -r -d '' file; do
        out="${file%.md}.pdf"
        process_file "$file" "$out"
    done < <(find . -type f -name '*.md' "${EXCLUDES[@]}" -print0)
fi

echo ""
echo "Готово: $OK из $TOTAL PDF создано, $FAIL ошибок."

[ "$FAIL" -eq 0 ] || exit 1
