from sqlalchemy import create_engine, Column, Integer, Text, TIMESTAMP  # Import necessary SQLAlchemy components for database creation and manipulation
from sqlalchemy.ext.declarative import declarative_base  # Import declarative base class for model definition
from sqlalchemy.orm import sessionmaker, Session  # Import sessionmaker for session creation and Session class for typing
from datetime import datetime  # Import datetime for timestamp management
import os  # Import os for interacting with the operating system
from dotenv import load_dotenv  # Import load_dotenv to load environment variables from a .env file
from models import ChatHistory  # Import ChatHistory model (though it is redefined later, which may be redundant)

# Load environment variables from a .env file into the environment
load_dotenv()

# Retrieve environment variables required for database connection
USER = os.getenv('DATABASE_USER')  # Database username
DATABASE = os.getenv('DATABASE_NAME')  # Database name
PASSWORD = os.getenv('DATABASE_PASSWORD')  # Database password
HOST = os.getenv('DATABASE_HOST')  # Database host (localhost)
PORT = os.getenv('DATABASE_PORT')  # Database port number

# Construct the PostgreSQL connection string using the retrieved environment variables
SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

# Create a SQLAlchemy engine that will be used to interact with the PostgreSQL database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a sessionmaker, which will be used to create database sessions
# autocommit=False ensures that changes are not automatically committed to the database
# autoflush=False prevents automatic flushing of data to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a base class for declarative class definitions
Base = declarative_base()

# Define a ChatHistory class which maps to the "chat_history" table in the database
class ChatHistory(Base):
    __tablename__ = "chat_history"  # Name of the table in the database

    id = Column(Integer, primary_key=True, index=True)  # Primary key column with an index for quick lookup
    user_input = Column(Text, nullable=False)  # Column to store the user's input (cannot be null)
    agent_response = Column(Text, nullable=False)  # Column to store the agent's response (cannot be null)
    timestamp = Column(TIMESTAMP, default=datetime.now())  # Column to store the timestamp of the interaction (defaults to the current time)

# Create all tables defined by the Base's subclasses (in this case, ChatHistory) in the database
Base.metadata.create_all(bind=engine)

# Dependency function that provides a database session for use in FastAPI routes
# The session is automatically closed after the request is processed
async def get_db():
    db = SessionLocal()  # Create a new database session
    try:
        yield db  # Yield the session for use in the request
    finally:
        db.close()  # Close the session after the request is complete

# Function to save a chat history record to the database
# This function takes the user input and agent response, creates a ChatHistory object, and saves it to the database
def save_chat_history(user_input: str, agent_response: str, db: Session):
    chat_record = ChatHistory(user_input=user_input, agent_response=agent_response)  # Create a new ChatHistory object
    db.add(chat_record)  # Add the new chat history record to the session
    db.commit()  # Commit the session to save the changes to the database
    db.refresh(chat_record)  # Refresh the session to update the state of the chat_record object with the database's state
