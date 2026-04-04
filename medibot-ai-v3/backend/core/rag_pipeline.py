import os
from typing import Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from backend.config import settings
from backend.core.gemini_client import gemini_client
from backend.prompts import RAG_INJECTION_TEMPLATE


class RAGPipeline:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self.collection = None
        self._init_collection()

    def _init_collection(self):
        try:
            self.collection = self.client.get_or_create_collection(
                name=settings.CHROMA_COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"},
            )
        except Exception as e:
            print(f"[RAG] ChromaDB init warning: {e}")
            self.collection = None

    def is_ready(self) -> bool:
        if self.collection is None:
            return False
        try:
            return self.collection.count() > 0
        except Exception:
            return False

    async def retrieve_context(self, query: str) -> Optional[str]:
        if not self.is_ready():
            return None
        try:
            query_embedding = gemini_client.embed_text(query)
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=settings.RAG_TOP_K,
                include=["documents", "metadatas", "distances"],
            )
            docs = results.get("documents", [[]])[0]
            metas = results.get("metadatas", [[]])[0]
            distances = results.get("distances", [[]])[0]

            relevant_chunks = []
            for doc, meta, dist in zip(docs, metas, distances):
                similarity = 1 - dist
                if similarity >= 0.5:
                    source = meta.get("source", "Medical Knowledge Base")
                    relevant_chunks.append(f"[{source}] {doc}")

            if not relevant_chunks:
                return None

            context = "\n\n".join(relevant_chunks)
            return RAG_INJECTION_TEMPLATE.format(context=context)
        except Exception as e:
            print(f"[RAG] Retrieval error: {e}")
            return None

    def add_documents(self, documents: list[str], metadatas: list[dict], ids: list[str]):
        if self.collection is None:
            return
        embeddings = [gemini_client.embed_text(doc) for doc in documents]
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids,
        )


rag_pipeline = RAGPipeline()
