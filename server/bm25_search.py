from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize
import time

class BM25Search:
    def __init__(self, corpus, data):
        self.bm25 = BM25Okapi(corpus)
        self.data = data
    
    def search(self, query, k=5):
        """Performs BM25 keyword search"""
        start_time = time.time()
        query_tokens = word_tokenize(query.lower())
        scores = self.bm25.get_scores(query_tokens)
        top_k_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        results = [self.data[i] for i in top_k_indices]
        
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for BM25 search: {execution_time:.4f} seconds")

        return results
