DATA_PATH = "data/datasets/small_books_data.csv"
FAISS_INDEX_PATH = "data/index/faiss_books.index"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # or "sentence-transformers/all-mpnet-base-v2"
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-4-v2"  # Re-ranker model
EMBEDDING_PATH = "data/embeddings/small_books_data_embeddings.npy"
BM25_CORPUS_PATH = "data/corpus/bm25_corpus.pkl"