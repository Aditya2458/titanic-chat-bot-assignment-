"""
FastAPI Backend for Titanic Chatbot
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn

from agent import TitanicAgent

# Initialize FastAPI app
app = FastAPI(
    title="Titanic Chatbot API",
    description="A friendly chatbot that analyzes the Titanic dataset",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Titanic agent
agent = TitanicAgent()


class QueryRequest(BaseModel):
    """Request model for chat queries"""
    query: str


class QueryResponse(BaseModel):
    """Response model for chat queries"""
    answer: str
    visualization: Optional[str] = None  # Base64 encoded image


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Titanic Chatbot API",
        "endpoints": {
            "/chat": "POST - Send a query about the Titanic dataset",
            "/info": "GET - Get dataset information",
            "/health": "GET - Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/info")
async def get_info():
    """Get dataset information"""
    from data_loader import get_dataset_info
    return get_dataset_info()


@app.post("/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):
    """
    Process a chat query about the Titanic dataset.
    
    Args:
        request: QueryRequest containing the user's question
        
    Returns:
        QueryResponse with answer and optional visualization
    """
    try:
        result = agent.process_query(request.query)
        return QueryResponse(
            answer=result["answer"],
            visualization=result.get("visualization")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
