# Minimal RAG template

Small local RAG over project documentation.

Structure:
- `ragchat/config.py` — model and indexing settings.
- `ragchat/chunking.py` — split Markdown docs.
- `ragchat/indexing.py` — embed and store in Chroma + BM25 index.
- `ragchat/retrieval.py` — hybrid dense + BM25 search.
- `ragchat/generation.py` — call local LLM with citations.
- `ragchat/cli.py` — Typer CLI.

Usage:
```bash
pip install -e .
python -m ragchat.cli index
python -m ragchat.cli ask "How does auth work?"
```

Edit `ragchat/config.py` to set your docs path and model names.
