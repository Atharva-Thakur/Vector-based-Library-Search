import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from config import FAISS_INDEX_PATH, EMBEDDING_MODEL
import time

class VectorSearch:
    def __init__(self, data):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.data = data
        self.index = faiss.read_index(FAISS_INDEX_PATH)
    
    def search(self, query, k=5):
        """Performs FAISS vector search"""
        start_time = time.time()
        query_embedding = self.model.encode(query, normalize_embeddings=True).reshape(1, -1)
        _, indices = self.index.search(query_embedding, k)
        results = [self.data[i] for i in indices[0]]

        end_time = time.time()
        execution_time = end_time - start_time
    
        print(f"Execution time for vector search: {execution_time:.4f} seconds")
        return results

