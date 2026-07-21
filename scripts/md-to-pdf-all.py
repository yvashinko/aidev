#!/usr/bin/env python3
"""Рекурсивная конвертация всех Markdown-файлов в PDF через md2pdf.

Примеры:
    python3 scripts/md-to-pdf-all.py
    python3 scripts/md-to-pdf-all.py --dist
    python3 scripts/md-to-pdf-all.py --dist dist/pdf
"""

import argparse
import subprocess
import sys
from pathlib import Path

EXCLUDED_DIRNAMES = {
    ".git",
    "dist",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".specstory",
    ".cursor",
}


def should_skip(path: Path) -> bool:
    return any(part in EXCLUDED_DIRNAMES for part in path.parts)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Recursively convert Markdown files to PDF using md2pdf."
    )
    parser.add_argument(
        "--dist",
        nargs="?",
        const="dist",
        help="Save PDFs into a single directory preserving relative structure. "
        "Default directory: dist.",
    )
    args = parser.parse_args()

    root = Path(".")
    md_files = [p for p in root.rglob("*.md") if not should_skip(p)]

    total = len(md_files)
    ok = 0
    fail = 0

    for md in md_files:
        if args.dist:
            out = Path(args.dist) / md.relative_to(root).with_suffix(".pdf")
        else:
            out = md.with_suffix(".pdf")
        out.parent.mkdir(parents=True, exist_ok=True)

        result = subprocess.run(
            [sys.executable, "scripts/md-to-pdf.py", str(md), str(out)],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"  OK: {out}")
            ok += 1
        else:
            print(f"FAIL: {md}")
            fail += 1

    print(f"\nDone: {ok}/{total} PDFs created, {fail} failures.")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
