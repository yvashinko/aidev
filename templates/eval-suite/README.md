# RAG eval suite template

Uses Ragas to measure faithfulness, answer relevance, context precision and recall.

Files:
- `eval.py` — run evaluation against `eval_dataset.json`.
- `eval_dataset.json` — curated question/context/ground_truth records.
- `thresholds.json` — minimum acceptable scores.
- `pyproject.toml` — dependencies.

Run:
```bash
python eval.py --check
```

Add new questions to `eval_dataset.json`.
