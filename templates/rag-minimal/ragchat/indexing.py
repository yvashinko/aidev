import httpx
import pickle
import chromadb
from rank_bm25 import BM25Okapi
from pathlib import Path
from .config import Config


def embed_texts(texts: list[str], cfg: Config) -> list[list[float]]:
    embeddings = []
    with httpx.Client(timeout=60) as client:
        for text in texts:
            resp = client.post(
                f"{cfg.ollama_url}/api/embeddings",
                json={"model": cfg.embed_model, "prompt": text},
            )
            resp.raise_for_status()
            embeddings.append(resp.json()["embedding"])
    return embeddings


def _tokenize(text: str) -> list[str]:
    import re
    return re.findall(r"\b\w+\b", text.lower())


def build_index(chunks: list[dict], cfg: Config) -> None:
    cfg.chroma_path.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(cfg.chroma_path))

    try:
        client.delete_collection(cfg.collection_name)
    except Exception:
        pass

    collection = client.create_collection(
        name=cfg.collection_name,
        metadata={"hnsw:space": "cosine"},
    )

    texts = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(
        documents=texts,
        metadatas=metadatas,
        embeddings=embed_texts(texts, cfg),
        ids=ids,
    )

    bm25 = BM25Okapi([_tokenize(t) for t in texts])
    with (cfg.chroma_path / "bm25.pkl").open("wb") as f:
        pickle.dump({"bm25": bm25, "ids": ids, "texts": texts, "metadatas": metadatas}, f)
