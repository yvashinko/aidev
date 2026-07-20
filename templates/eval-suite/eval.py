import argparse
import json
from pathlib import Path

from datasets import Dataset
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from ragas import evaluate
from ragas.metrics import Faithfulness, AnswerRelevancy, ContextPrecision, ContextRecall

DATASET_PATH = Path("eval_dataset.json")
THRESHOLDS_PATH = Path("thresholds.json")

LLM_MODEL = "llama3.1:70b-instruct-q4_K_M"
EMBED_MODEL = "nomic-embed-text"
OLLAMA_URL = "http://localhost:11434"

METRICS = [
    Faithfulness(),
    AnswerRelevancy(),
    ContextPrecision(),
    ContextRecall(),
]


def load_dataset(path: Path = DATASET_PATH) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def generate_answers(records: list[dict]) -> list[dict]:
    # Stub: replace with your retrieval + generation pipeline.
    # For eval, answers should come from the actual RAG system under test.
    return [
        {**r, "answer": "[GENERATED_ANSWER_PLACEHOLDER]"} for r in records
    ]


def run_eval(records: list[dict]) -> dict:
    ds = Dataset.from_list(records)
    llm = ChatOllama(model=LLM_MODEL, base_url=OLLAMA_URL)
    emb = OllamaEmbeddings(model=EMBED_MODEL, base_url=OLLAMA_URL)
    result = evaluate(ds, metrics=METRICS, llm=llm, embeddings=emb)
    return result.to_pandas().to_dict(orient="records")


def check_thresholds(scores: list[dict], thresholds: dict) -> bool:
    ok = True
    for row in scores:
        q = row.get("question", "?")
        for metric, min_val in thresholds.items():
            value = row.get(metric)
            if value is None:
                continue
            status = "OK" if value >= min_val else "FAIL"
            if status == "FAIL":
                ok = False
            print(f"{q} | {metric}: {value:.2f} ({status}, min {min_val})")
    return ok


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true", help="Generate answers")
    parser.add_argument("--check", action="store_true", help="Run metrics and check thresholds")
    args = parser.parse_args()

    records = load_dataset()

    if args.generate:
        answered = generate_answers(records)
        with DATASET_PATH.open("w", encoding="utf-8") as f:
            json.dump(answered, f, ensure_ascii=False, indent=2)
        print(f"Wrote answers to {DATASET_PATH}")
        return

    if args.check:
        scores = run_eval(records)
        with open("eval_results.json", "w", encoding="utf-8") as f:
            json.dump(scores, f, ensure_ascii=False, indent=2)

        thresholds = json.loads(THRESHOLDS_PATH.read_text(encoding="utf-8"))
        ok = check_thresholds(scores, thresholds)
        raise SystemExit(0 if ok else 1)

    parser.print_help()


if __name__ == "__main__":
    main()
