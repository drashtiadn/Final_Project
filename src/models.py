from pydantic import BaseModel  # Import BaseModel from Pydantic for data validation and serialization
from sqlalchemy import Column, Integer, Text, TIMESTAMP  # Import necessary SQLAlchemy components for defining database columns and types
from sqlalchemy.ext.declarative import declarative_base  # Import declarative base class for model definition
from datetime import datetime  # Import datetime for timestamp management

# Initialize the base class for declarative class definitions using SQLAlchemy
Base = declarative_base()

# Define the ChatHistory class, which maps to the "chat_history" table in the database
class ChatHistory(Base):
    __tablename__ = "chat_history"  # Name of the table in the database

    id = Column(Integer, primary_key=True, index=True)  # Primary key column with an index for quick lookup
    user_input = Column(Text, nullable=False)  # Column to store the user's input (cannot be null)
    agent_response = Column(Text, nullable=False)  # Column to store the agent's response (cannot be null)
    timestamp = Column(TIMESTAMP, default=datetime.now())  # Column to store the timestamp of the interaction (defaults to the current time)

# Define a Pydantic model for input validation when receiving a query from the user
class QueryInput(BaseModel):
    input: str  # Define a single field "input" to accept the user's query as a string

# Define a Pydantic model for serializing chat history records to send back to the client
class ChatHistoryResponse(BaseModel):
    id: int  # Define an integer field for the chat history record's ID
    user_input: str  # Define a string field for the user's input
    agent_response: str  # Define a string field for the agent's response
    timestamp: str  # Define a string field for the timestamp, which will be formatted as a string

    # Configure the Pydantic model to allow loading data directly from SQLAlchemy models
    class Config:
        from_attributes = True  # This allows Pydantic to parse data from SQLAlchemy ORM objects

    # Define a class method to create a Pydantic model instance from an ORM object
    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,  # Get the ID from the ORM object
            user_input=orm_obj.user_input,  # Get the user input from the ORM object
            agent_response=orm_obj.agent_response,  # Get the agent's response from the ORM object
            timestamp=orm_obj.timestamp.strftime("%d-%m-%Y at %H:%M:%S")  # Format the timestamp into a readable string
        )
