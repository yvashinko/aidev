from pathlib import Path
from pydantic import BaseModel


class Config(BaseModel):
    docs_root: Path = Path("docs")
    chroma_path: Path = Path("data/chroma")
    collection_name: str = "[PROJECT_NAME]_docs"

    embed_model: str = "nomic-embed-text"
    llm_model: str = "llama3.1:8b-instruct-q4_K_M"
    ollama_url: str = "http://localhost:11434"

    chunk_size: int = 600
    chunk_overlap: int = 80
    top_k_dense: int = 20
    top_k_sparse: int = 20
    top_k_final: int = 5
    rrf_k: int = 60
