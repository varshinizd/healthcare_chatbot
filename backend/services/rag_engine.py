import json
import faiss
import numpy as np
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer


class RAGEngine:
    def __init__(self, json_path="medical_clean.json"):

        self.documents = []
        self.index = None
        self.vectorizer = TfidfVectorizer(stop_words="english")

        self.index_file = "faiss_index.bin"
        self.doc_file = "docs.pkl"
        self.vec_file = "vectorizer.pkl"

        if os.path.exists(self.index_file):
            print("⚡ Loading cached RAG...")
            self.load_cache()
        else:
            print("🧠 Building RAG first time...")
            self.build_index(json_path)
            self.save_cache()

    # ---------------- BUILD ----------------
    def build_index(self, path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        texts = []

        for item in data:
            text = f"""
Disease: {item.get('disease')}
Also Called: {', '.join(item.get('also_called', []))}
Category: {', '.join(item.get('category', []))}
Summary: {item.get('summary')}
"""
            texts.append(text)
            self.documents.append(text)

        tfidf_matrix = self.vectorizer.fit_transform(texts).toarray().astype("float32")

        dim = tfidf_matrix.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(tfidf_matrix)

        print(f"✅ RAG built with {len(self.documents)} entries")

    # ---------------- CACHE ----------------
    def save_cache(self):
        faiss.write_index(self.index, self.index_file)

        with open(self.doc_file, "wb") as f:
            pickle.dump(self.documents, f)

        with open(self.vec_file, "wb") as f:
            pickle.dump(self.vectorizer, f)

        print("💾 RAG cache saved")

    def load_cache(self):
        self.index = faiss.read_index(self.index_file)

        with open(self.doc_file, "rb") as f:
            self.documents = pickle.load(f)

        with open(self.vec_file, "rb") as f:
            self.vectorizer = pickle.load(f)

        print("✅ RAG loaded instantly")

    # ---------------- SEARCH ----------------
    def search(self, query, top_k=3):
        query_vec = self.vectorizer.transform([query]).toarray().astype("float32")

        distances, indices = self.index.search(query_vec, top_k)

        results = []
        for idx in indices[0]:
            results.append(self.documents[idx])

        return "\n\n".join(results)
