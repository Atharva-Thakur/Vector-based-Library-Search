from fastapi import FastAPI
from pydantic import BaseModel
from data_ingestion import DataIngestion
from hybrid_search import HybridSearch
from fastapi.middleware.cors import CORSMiddleware
import time

# Define the FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://studious-invention-x776g55wpvjh9vpx-5173.app.github.dev"],  # Or use ["*"] to allow all origins (not recommended in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Pydantic model to receive the query input
class QueryRequest(BaseModel):
    query: str

# Initialize DataIngestion and HybridSearch outside of the endpoint to avoid reinitializing on each request
ingestion = DataIngestion()
bm25_corpus, books, _ = ingestion.run()
hybrid_search = HybridSearch(books, bm25_corpus)

@app.get("/water")
async def getWater():
    return "water"

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