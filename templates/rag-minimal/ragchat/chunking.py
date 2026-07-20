from pathlib import Path
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

HEADERS = [("#", "h1"), ("##", "h2"), ("###", "h3")]


def chunk_markdown_file(path: Path, chunk_size: int, chunk_overlap: int) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    md_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=HEADERS, strip_headers=False)
    sections = md_splitter.split_text(text)

    char_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )

    chunks = []
    for section in sections:
        for idx, piece in enumerate(char_splitter.split_text(section.page_content)):
            chunks.append({
                "text": piece,
                "metadata": {
                    "source": str(path),
                    "h1": section.metadata.get("h1", ""),
                    "h2": section.metadata.get("h2", ""),
                    "h3": section.metadata.get("h3", ""),
                    "chunk_index": idx,
                },
            })
    return chunks


def chunk_repo(docs_root: Path, chunk_size: int, chunk_overlap: int) -> list[dict]:
    chunks: list[dict] = []
    for md_path in docs_root.rglob("*.md"):
        chunks.extend(chunk_markdown_file(md_path, chunk_size, chunk_overlap))
    return chunks
