#!/usr/bin/env python3
"""Конвертация одного Markdown-файла в PDF через xhtml2pdf.

Не требует pandoc/xelatex — достаточно Python-зависимостей из environment.txt.

Примеры:
    python3 scripts/md-to-pdf.py research/2026-07-ai-landscape.md
    python3 scripts/md-to-pdf.py README.md dist/README.pdf
"""

import argparse
import sys
from pathlib import Path

import markdown
from xhtml2pdf import pisa


# Пути к распространённым системным шрифтам с поддержкой Unicode/кириллицы.
FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/Library/Fonts/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "C:/Windows/Fonts/arial.ttf",
]


def find_system_font() -> str | None:
    for candidate in FONT_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    return None


def build_html(md_text: str, font_path: str | None) -> str:
    body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "toc"],
    )

    if font_path:
        font_face = f"@font-face {{ font-family: 'MDFont'; src: url('{font_path}'); }}"
        font_family = "'MDFont', sans-serif"
    else:
        font_face = ""
        font_family = "sans-serif"

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{font_face}
body {{ font-family: {font_family}; font-size: 11pt; line-height: 1.5; margin: 2cm; }}
h1, h2, h3, h4 {{ color: #222; page-break-after: avoid; }}
code {{ background: #f4f4f4; padding: 2px 4px; font-family: monospace; font-size: 10pt; }}
pre {{ background: #f4f4f4; padding: 10px; overflow-x: auto; white-space: pre-wrap; }}
table {{ border-collapse: collapse; width: 100%; margin: 1em 0; }}
th, td {{ border: 1px solid #ccc; padding: 6px; text-align: left; vertical-align: top; }}
ul {{ margin: 0.5em 0; }}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert a Markdown file to PDF using xhtml2pdf."
    )
    parser.add_argument("input", help="Input Markdown file.")
    parser.add_argument(
        "output",
        nargs="?",
        help="Output PDF file. Defaults to <input>.pdf next to the source.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_file():
        print(f"Error: file not found: {input_path}", file=sys.stderr)
        return 1

    output_path = Path(args.output) if args.output else input_path.with_suffix(".pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    md_text = input_path.read_text(encoding="utf-8")
    font_path = find_system_font()
    html = build_html(md_text, font_path)

    with open(output_path, "wb") as out:
        result = pisa.CreatePDF(html, dest=out)

    if result.err:
        print(
            f"Error: {result.err} error(s) during PDF generation",
            file=sys.stderr,
        )
        return 1

    print(f"PDF created: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
