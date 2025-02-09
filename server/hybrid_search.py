from sentence_transformers import CrossEncoder
from vector_search import VectorSearch
from bm25_search import BM25Search
from config import RERANKER_MODEL

class HybridSearch:
    def __init__(self, data, bm25_corpus):
        self.vector_search = VectorSearch(data)
        self.bm25_search = BM25Search(bm25_corpus, data)
        self.re_ranker = CrossEncoder(RERANKER_MODEL)
    
    def create_corpus_text(self, item, fields):
        return " ".join(str(item[field]) for field in fields if field in item).lower()


    def search(self, query, k=5):
        faiss_results = self.vector_search.search(query, k=10)
        bm25_results = self.bm25_search.search(query, k=10)
        
        combined_results = self.reciprocal_rank_fusion(faiss_results, bm25_results, k=10)
        
        if not combined_results:
            print("No results found.")
            return []
        
        return self.re_rank(combined_results, query, k)

    def reciprocal_rank_fusion(self, faiss_results, bm25_results, k=5, k_const=60):
        rank_scores, item_mapping = {}, {}
        for result_list in [faiss_results, bm25_results]:
            for rank, item in enumerate(result_list, start=1):
                title = item.get('Title', str(item))
                rank_scores[title] = rank_scores.get(title, 0) + 1 / (rank + k_const)
                item_mapping[title] = item
        top_titles = sorted(rank_scores, key=rank_scores.get, reverse=True)[:k]
        return [item_mapping[title] for title in top_titles]

    def re_rank(self, results, query, k):
        candidate_pairs = [(query, self.create_corpus_text(item, item.keys())) for item in results]
        scores = self.re_ranker.predict(candidate_pairs)
        reranked_results = sorted(zip(scores, results), key=lambda x: x[0], reverse=True)
        return [item for _, item in reranked_results[:k]]
