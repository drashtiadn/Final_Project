# Importing necessary modules from FastAPI and SQLAlchemy
from fastapi import FastAPI, Depends  # FastAPI framework and dependency injection
from sqlalchemy.orm import Session  # SQLAlchemy session handling
from typing import List  # Typing module for type hints

# Importing models and functions
from models import QueryInput, ChatHistoryResponse, ChatHistory  # Models for request and response
from database import get_db, save_chat_history  # Database utilities for session management and saving chat history
from agents import agent_executor, memory  # Agent executor for handling queries and memory for conversation context

# Initialize the FastAPI app
app = FastAPI()

# Define a POST endpoint for querying the agent
@app.post("/ask")
async def ask_agent(query: QueryInput, db: Session = Depends(get_db)):
    """
    Endpoint to handle user queries. This takes a query input, 
    processes it through the agent, and returns the agent's response.
    
    Parameters:
    - query: The user's input query (QueryInput model).
    - db: Database session, managed by FastAPI's dependency injection (using get_db).
    
    Steps:
    1. The user's input is extracted.
    2. The agent_executor processes the input and generates a response.
    3. The chat history (user input and agent response) is saved to the database.
    4. The agent's response is returned to the user.
    """
    inputs = {"input": query.input}  # Prepare input for the agent
    response = agent_executor.invoke(inputs)  # Invoke the agent to get a response
    save_chat_history(query.input, response["output"], db)  # Save the input and output to the database
    return {"response": response["output"]}  # Return the agent's response to the client

# Define a GET endpoint to retrieve chat history
@app.get("/chat_history", response_model=List[ChatHistoryResponse])
async def get_chat_history(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve chat history. This allows users to view past interactions.
    
    Parameters:
    - skip: Number of records to skip (used for pagination).
    - limit: Maximum number of records to return (also for pagination).
    - db: Database session, managed by FastAPI's dependency injection (using get_db).
    
    Steps:
    1. Query the database for chat history records, applying pagination.
    2. Convert each record to the response model (ChatHistoryResponse).
    3. Return the list of chat history records to the client.
    """
    chat_history = db.query(ChatHistory).offset(skip).limit(limit).all()  # Fetch chat history with pagination
    return [ChatHistoryResponse.from_orm(chat) for chat in chat_history]  # Convert database models to response models

# Main entry point for running the application
if __name__ == "__main__":
    import uvicorn  # Uvicorn is the ASGI server for running FastAPI apps
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Run the app on host 0.0.0.0 and port 8000

