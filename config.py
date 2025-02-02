import os

DATA_PATH = "data/books_dataset.csv"
FAISS_INDEX_PATH = "data/faiss_books.index"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # or "sentence-transformers/all-mpnet-base-v2"
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"  # Re-ranker model
EMBEDDING_PATH = "data/embeddings/book_embeddings.npy"