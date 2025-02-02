import os
import json
import numpy as np
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import nltk
from config import DATA_PATH, FAISS_INDEX_PATH, EMBEDDING_MODEL, EMBEDDING_PATH

nltk.download("punkt")


class DataIngestion:
    def __init__(self, data_path=DATA_PATH, embedding_path=EMBEDDING_PATH, faiss_path=FAISS_INDEX_PATH):
        self.data_path = data_path
        self.embedding_path = embedding_path
        self.faiss_path = faiss_path
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def load_data(self):
        """Load books from JSON or CSV."""
        if self.data_path.endswith(".json"):
            with open(self.data_path, "r", encoding="utf-8") as file:
                books = json.load(file)
        elif self.data_path.endswith(".csv"):
            books = pd.read_csv(self.data_path).to_dict(orient="records")
        else:
            raise ValueError("Unsupported file format!")
        print(f"Loaded {len(books)} books.")
        return books

    def create_bm25_corpus(self, books):
        """Create tokenized corpus for BM25 using title, author, genre, and about."""
        print('Creating BM25 corpus...')
        corpus = []
        for book in books:
            text = f"{book['title']} {book['author']} {' '.join(book['genre'])} {book['about']}".lower()
            corpus.append(nltk.word_tokenize(text))  # Tokenize the combined text
        
        return corpus

    def create_faiss_index(self, books):
        """Create or load FAISS index."""
        if os.path.exists(self.embedding_path):
            print("Loading saved embeddings...")
            embeddings = np.load(self.embedding_path)
            index = faiss.IndexFlatL2(embeddings.shape[1])
            index.add(embeddings)
            faiss.write_index(index, self.faiss_path)
        else:
            print("Generating new embeddings and FAISS index...")
            texts = [[f"{book['title']} {book['author']} {' '.join(book['genre'])} {book['about']}".lower()] for book in books]
            embeddings = np.array(self.model.encode(texts), dtype=np.float32)
            
            # Save embeddings
            np.save(self.embedding_path, embeddings)

            # Create FAISS index
            index = faiss.IndexFlatL2(embeddings.shape[1])
            index.add(embeddings)
            faiss.write_index(index, self.faiss_path)

        return index, embeddings

    def run(self):
        """Load data, process BM25 & FAISS, and return results."""
        books = self.load_data()
        bm25_corpus = self.create_bm25_corpus(books)
        faiss_index, embeddings = self.create_faiss_index(books)
        return bm25_corpus, books, faiss_index


if __name__ == "__main__":
    ingestion = DataIngestion()
    ingestion.run()
