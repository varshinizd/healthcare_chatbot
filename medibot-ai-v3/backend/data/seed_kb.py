"""
Run this script once to build the ChromaDB vector index from medical KB text files.
Usage: python -m backend.data.seed_kb
"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend.config import settings
from backend.core.gemini_client import gemini_client
import chromadb
from chromadb.config import Settings as ChromaSettings

KB_DIR = Path(__file__).parent / "medical_kb"
CHROMA_DIR = Path(__file__).parent / "embeddings"


def chunk_text(text: str, source: str, chunk_size: int = 400) -> list[dict]:
    """Split text into overlapping chunks."""
    chunks = []
    lines = [line.strip() for line in text.strip().split("\n\n") if line.strip()]
    for i, paragraph in enumerate(lines):
        if len(paragraph) > chunk_size:
            words = paragraph.split()
            for j in range(0, len(words), chunk_size // 6):
                chunk = " ".join(words[j : j + chunk_size // 6])
                if len(chunk) > 50:
                    chunks.append(
                        {
                            "text": chunk,
                            "source": source,
                            "paragraph_idx": i,
                            "chunk_idx": j,
                        }
                    )
        else:
            chunks.append(
                {"text": paragraph, "source": source, "paragraph_idx": i, "chunk_idx": 0}
            )
    return chunks


def seed():
    print("[Seed] Initializing ChromaDB...")
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR),
        settings=ChromaSettings(anonymized_telemetry=False),
    )

    try:
        client.delete_collection(settings.CHROMA_COLLECTION_NAME)
        print("[Seed] Deleted existing collection.")
    except Exception:
        pass

    collection = client.create_collection(
        name=settings.CHROMA_COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    all_docs = []
    all_metas = []
    all_ids = []

    kb_files = list(KB_DIR.glob("*.txt"))
    if not kb_files:
        print(f"[Seed] ERROR: No .txt files found in {KB_DIR}")
        return

    for kb_file in kb_files:
        source = kb_file.stem.replace("_", " ").title()
        text = kb_file.read_text(encoding="utf-8")
        chunks = chunk_text(text, source)
        print(f"[Seed] {kb_file.name}: {len(chunks)} chunks")

        for chunk in chunks:
            doc_id = f"{kb_file.stem}_{chunk['paragraph_idx']}_{chunk['chunk_idx']}"
            all_docs.append(chunk["text"])
            all_metas.append({"source": source, "file": kb_file.name})
            all_ids.append(doc_id)

    print(f"[Seed] Embedding {len(all_docs)} chunks via Gemini API...")
    batch_size = 20
    for i in range(0, len(all_docs), batch_size):
        batch_docs = all_docs[i : i + batch_size]
        batch_metas = all_metas[i : i + batch_size]
        batch_ids = all_ids[i : i + batch_size]

        embeddings = []
        for doc in batch_docs:
            emb = gemini_client.embed_text(doc)
            embeddings.append(emb)

        collection.add(
            documents=batch_docs,
            embeddings=embeddings,
            metadatas=batch_metas,
            ids=batch_ids,
        )
        print(f"[Seed] Embedded {min(i + batch_size, len(all_docs))}/{len(all_docs)}")

    print(f"[Seed] ✅ Done! {collection.count()} chunks in ChromaDB at {CHROMA_DIR}")


if __name__ == "__main__":
    seed()
