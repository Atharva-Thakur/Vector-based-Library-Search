from data_ingestion import DataIngestion
from hybrid_search import HybridSearch

def main():
    print("Loading data and indexing...")
    ingestion = DataIngestion()
    bm25_corpus, books, _ = ingestion.run()

    hybrid_search = HybridSearch(books, bm25_corpus)

    query = "AI takes over humanity"
    print(f"\nPerforming hybrid search for: \"{query}\"...\n")

    results = hybrid_search.search(query, k=5)

    print("Top Results:")
    for result in results:
        print(f"{result['title']} - {result['author']} - {result['about']}")

if __name__ == "__main__":
    main()
