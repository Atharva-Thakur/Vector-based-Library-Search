import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from config import FAISS_INDEX_PATH, EMBEDDING_MODEL

class VectorSearch:
    def __init__(self, books):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.books = books
        self.index = faiss.read_index(FAISS_INDEX_PATH)
    
    def search(self, query, k=5):
        """Performs FAISS vector search"""
        query_embedding = self.model.encode(query, normalize_embeddings=True).reshape(1, -1)
        _, indices = self.index.search(query_embedding, k)
        results = [self.books[i] for i in indices[0]]
        for result in results:
            print('Vector search result-',result)
            print('------------------------------------------------------------------------------------')

        return results

