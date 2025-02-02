from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize

class BM25Search:
    def __init__(self, corpus, books):
        self.bm25 = BM25Okapi(corpus)
        self.books = books
    
    def search(self, query, k=5):
        """Performs BM25 keyword search"""
        query_tokens = word_tokenize(query.lower())
        scores = self.bm25.get_scores(query_tokens)
        top_k_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        results = [self.books[i] for i in top_k_indices]
        for result in results:
            print('BM25 result-',result)
            print('------------------------------------------------------------------------------------')

        return results
