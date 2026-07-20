import pickle
import chromadb
from .config import Config
from .indexing import embed_texts, _tokenize


def _reciprocal_rank_fusion(rankings: list[list[str]], k: int = 60) -> dict[str, float]:
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank + 1)
    return scores


def hybrid_search(query: str, cfg: Config) -> list[dict]:
    client = chromadb.PersistentClient(path=str(cfg.chroma_path))
    collection = client.get_collection(cfg.collection_name)

    query_emb = embed_texts([query], cfg)[0]
    dense_result = collection.query(
        query_embeddings=[query_emb],
        n_results=cfg.top_k_dense,
        include=["documents", "metadatas", "distances"],
    )
    dense_ids = dense_result["ids"][0]

    with (cfg.chroma_path / "bm25.pkl").open("rb") as f:
        bm25_data = pickle.load(f)

    query_tokens = _tokenize(query)
    bm25_scores = bm25_data["bm25"].get_scores(query_tokens)
    sparse_top = sorted(range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True)
    sparse_ids = [bm25_data["ids"][i] for i in sparse_top[: cfg.top_k_sparse]]

    fused = _reciprocal_rank_fusion([dense_ids, sparse_ids], k=cfg.rrf_k)
    top_ids = sorted(fused.keys(), key=lambda i: fused[i], reverse=True)[: cfg.top_k_final]

    id_to_idx = {i: idx for idx, i in enumerate(bm25_data["ids"])}
    return [
        {
            "rank": rank + 1,
            "id": doc_id,
            "text": bm25_data["texts"][id_to_idx[doc_id]],
            "metadata": bm25_data["metadatas"][id_to_idx[doc_id]],
            "score": fused[doc_id],
        }
        for rank, doc_id in enumerate(top_ids)
    ]
