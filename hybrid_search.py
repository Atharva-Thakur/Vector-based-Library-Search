from sentence_transformers import CrossEncoder
from vector_search import VectorSearch
from bm25_search import BM25Search
from config import RERANKER_MODEL

class HybridSearch:
    def __init__(self, books, bm25_corpus):
        self.books = books
        self.vector_search = VectorSearch(books)
        self.bm25_search = BM25Search(bm25_corpus, books)
        self.re_ranker = CrossEncoder(RERANKER_MODEL)
    
    def reciprocal_rank_fusion(self, faiss_results, bm25_results, k=5, k_const=50):
        """
        Merge FAISS and BM25 results using RRF and return full book objects.
        Each list's ranking is computed independently.
        """
        rank_scores = {}
        book_mapping = {}
        
        for result_list in [faiss_results, bm25_results]:
            for rank, book in enumerate(result_list, start=1):
                title = book['title']
                score = 1 / (rank + k_const)
                rank_scores[title] = rank_scores.get(title, 0) + score
                if title not in book_mapping:
                    book_mapping[title] = book
        
        top_titles = sorted(rank_scores, key=lambda t: rank_scores[t], reverse=True)[:k]
        
        return [book_mapping[title] for title in top_titles]

    
    def search(self, query, k=5):
        """
        Performs hybrid search by first retrieving results from vector search (FAISS)
        and BM25, merging them using RRF, and finally re-ranking using a CrossEncoder.
        """
        faiss_results = self.vector_search.search(query, k=10)
        bm25_results = self.bm25_search.search(query, k=10)
        
        combined_results = self.reciprocal_rank_fusion(faiss_results, bm25_results, k=10)
        print('Combined results (before re-ranking):', combined_results)
        print('--------------------------------------------------------------')
        
        candidate_pairs = [(query, book['title']) for book in combined_results]
        
        scores = self.re_ranker.predict(candidate_pairs)
        
        reranked_results = [
            book for _, book in sorted(zip(scores, combined_results), key=lambda pair: pair[0], reverse=True)
        ][:k]
        
        return reranked_results
