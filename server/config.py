DATA_PATH = "data/datasets/small_books_data_with_roles.csv"
FAISS_INDEX_PATH = "data/index/"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # or "sentence-transformers/all-mpnet-base-v2"
RERANKER_MODEL = "cross-encoder/ms-marco-TinyBERT-L-2-v2"  # Re-ranker model
EMBEDDING_PATH = "data/embeddings/small_books_data_embeddings.npy"
BM25_CORPUS_PATH = "data/corpus/bm25_corpus.pkl"