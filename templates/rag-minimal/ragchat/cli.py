import json
import typer
from .config import Config
from .chunking import chunk_repo
from .indexing import build_index
from .retrieval import hybrid_search
from .generation import generate_answer

app = typer.Typer()


@app.command()
def index() -> None:
    cfg = Config()
    chunks = chunk_repo(cfg.docs_root, cfg.chunk_size, cfg.chunk_overlap)
    print(f"Chunked {len(chunks)} pieces from {cfg.docs_root}")
    build_index(chunks, cfg)
    print(f"Index ready: {cfg.chroma_path}")


@app.command()
def ask(question: str) -> None:
    cfg = Config()
    retrieved = hybrid_search(question, cfg)
    result = generate_answer(question, retrieved, cfg)

    print(f"\n=== ANSWER ===\n{result['answer']}\n")
    print("=== SOURCES ===")
    for c in result["citations"]:
        section = f" > {c['section']}" if c["section"] else ""
        print(f"  [{c['id']}] {c['source']}{section}")


@app.command()
def ask_json(question: str) -> None:
    cfg = Config()
    retrieved = hybrid_search(question, cfg)
    result = generate_answer(question, retrieved, cfg)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    app()
