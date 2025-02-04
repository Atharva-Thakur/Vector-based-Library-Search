from fastapi import FastAPI
from pydantic import BaseModel
from data_ingestion import DataIngestion
from hybrid_search import HybridSearch

# Define the FastAPI app
app = FastAPI()

# Pydantic model to receive the query input
class QueryRequest(BaseModel):
    query: str

# Initialize DataIngestion and HybridSearch outside of the endpoint to avoid reinitializing on each request
ingestion = DataIngestion()
bm25_corpus, books, _ = ingestion.run()
hybrid_search = HybridSearch(books, bm25_corpus)

@app.post("/search")
async def search_books(query_request: QueryRequest):
    query = query_request.query
    results = hybrid_search.search(query, k=5)

    # Return a JSON object with a key like 'results'
    return {"results": results}