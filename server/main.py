from data_ingestion import DataIngestion
from hybrid_search import HybridSearch

def main():
    print("Loading data and indexing...")
    ingestion = DataIngestion()
    bm25_corpus, data, _ = ingestion.run()

    hybrid_search = HybridSearch(data, bm25_corpus)

    query = "AI takes over humanity"
    print(f"\nPerforming hybrid search for: \"{query}\"...\n")

    results = hybrid_search.search(query, k=5, filter={'role': 'User'})

    print("Top Results:")
    print(results)

if __name__ == "__main__":
    main()
