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
    allow_origins=["*"],  # Or use ["*"] to allow all origins (not recommended in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Pydantic model to receive the query input
class QueryRequest(BaseModel):
    query: str
    filter:dict

# Initialize DataIngestion and HybridSearch outside of the endpoint to avoid reinitializing on each request
ingestion = DataIngestion()
bm25_corpus, data, _ = ingestion.run()
hybrid_search = HybridSearch(data, bm25_corpus)

@app.get("/genres")
def get_unique_genres():
    genres = set()
    
    for book in data:
        genre_value = book.get("genre", [])
        
        if isinstance(genre_value, str):  # If "genre" is a single string
            genres.add(genre_value)
        elif isinstance(genre_value, list):  # If "genre" is a list
            genres.update(genre_value)
    print(len(genres))
    return list(genres)

@app.post("/search")
async def search_books(query_request: QueryRequest):
    start_time = time.time()  # Start the timer

    query = query_request.query
    filter = query_request.filter
    results = hybrid_search.search(query, k=5, filter=filter)

    end_time = time.time()  # End the timer
    execution_time = end_time - start_time  # Calculate the time taken
    
    # Print the execution time
    print(f"Execution time: {execution_time:.4f} seconds")

    # Return a JSON object with a key like 'results'
    return {"results": results}