from fastapi import FastAPI
from pydantic import BaseModel
from data_ingestion import DataIngestion
from hybrid_search import HybridSearch
import time

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
    start_time = time.time()  # Start the timer

    query = query_request.query
    results = hybrid_search.search(query, k=5)

    end_time = time.time()  # End the timer
    execution_time = end_time - start_time  # Calculate the time taken
    
    # Print the execution time
    print(f"Execution time: {execution_time:.4f} seconds")

    # Return a JSON object with a key like 'results'
    return {"results": results}