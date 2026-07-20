import httpx
from .config import Config

SYSTEM_PROMPT = """You are a documentation assistant for the [PROJECT_NAME] project.
Answer the user's question using ONLY the provided CONTEXT.
If the answer is not in the context, say "I don't know based on the indexed docs."
Cite sources by their numeric markers like [1], [2].
Be concise: 3-6 sentences unless detail is asked."""


def _format_context(retrieved: list[dict]) -> tuple[str, list[dict]]:
    parts = []
    citations = []
    for i, item in enumerate(retrieved, start=1):
        meta = item["metadata"]
        section = " > ".join(filter(None, [meta.get("h1"), meta.get("h2"), meta.get("h3")]))
        header = f"[{i}] ({meta['source']}{' > ' + section if section else ''}):"
        parts.append(f"{header}\n{item['text']}")
        citations.append({"id": i, "source": meta["source"], "section": section})
    return "\n\n".join(parts), citations


def generate_answer(query: str, retrieved: list[dict], cfg: Config) -> dict:
    context, citations = _format_context(retrieved)
    user_prompt = f"CONTEXT:\n{context}\n\nQUESTION: {query}\n\nANSWER:"

    with httpx.Client(timeout=120) as client:
        resp = client.post(
            f"{cfg.ollama_url}/api/chat",
            json={
                "model": cfg.llm_model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                "stream": False,
                "options": {"temperature": 0.2, "num_ctx": 8192},
            },
        )
        resp.raise_for_status()
        answer = resp.json()["message"]["content"]

    return {"question": query, "answer": answer, "citations": citations}
