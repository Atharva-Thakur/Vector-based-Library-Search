import os
import json
import numpy as np
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import nltk
import pickle
from config import BM25_CORPUS_PATH, DATA_PATH, FAISS_INDEX_PATH, EMBEDDING_MODEL, EMBEDDING_PATH

nltk.download("punkt")
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')

class DataIngestion:
    def __init__(self, data_path=DATA_PATH, embedding_path=EMBEDDING_PATH, faiss_path=FAISS_INDEX_PATH):
        self.data_path = data_path
        self.embedding_path = embedding_path
        self.faiss_path = faiss_path
        self.fields = []
        self.model = SentenceTransformer(EMBEDDING_MODEL)

    def load_data(self):
        if DATA_PATH.endswith(".json"):
            with open(DATA_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)
        elif DATA_PATH.endswith(".csv"):
            data = pd.read_csv(DATA_PATH).to_dict(orient="records")
        else:
            raise ValueError("Unsupported file format!")
        
        self.fields = list(data[0].keys()) if data else []
        print(f"Loaded {len(data)} records.")
        return data

    def create_corpus_text(self, item, fields):
        return " ".join(str(item[field]) for field in fields if field in item).lower()

    def create_bm25_corpus(self, data):
        """ Create and store BM25 corpus if not already saved. """
        if os.path.exists(BM25_CORPUS_PATH):
            with open(BM25_CORPUS_PATH, "rb") as f:
                return pickle.load(f)
        
        corpus = [nltk.word_tokenize(self.create_corpus_text(item, self.fields)) for item in data]
        
        # Save corpus
        with open(BM25_CORPUS_PATH, "wb") as f:
            pickle.dump(corpus, f)
        
        return corpus

    def create_faiss_index(self, data):
        if os.path.exists(EMBEDDING_PATH) and os.path.exists(FAISS_INDEX_PATH):
            embeddings = np.load(EMBEDDING_PATH)
            index = faiss.read_index(FAISS_INDEX_PATH)
        elif os.path.exists(EMBEDDING_PATH):
            embeddings = np.load(EMBEDDING_PATH)
            d = embeddings.shape[1]
            nlist = 10
            quantizer = faiss.IndexFlatL2(d)
            index = faiss.IndexIVFFlat(quantizer, d, nlist)
            index.train(embeddings)
            index.add(embeddings)
            faiss.write_index(index, FAISS_INDEX_PATH)
        else:
            texts = [self.create_corpus_text(item, self.fields) for item in data]
            embeddings = np.array(self.model.encode(texts, normalize_embeddings=True), dtype=np.float32)
            np.save(EMBEDDING_PATH, embeddings)
            index = faiss.IndexFlatIP(embeddings.shape[1])
            index.add(embeddings)
            faiss.write_index(index, FAISS_INDEX_PATH)
        return index, embeddings

    def run(self):
        data = self.load_data()
        bm25_corpus = self.create_bm25_corpus(data)
        faiss_index, embeddings = self.create_faiss_index(data)
        return bm25_corpus, data, faiss_index


if __name__ == "__main__":
    ingestion = DataIngestion()
    ingestion.run()
