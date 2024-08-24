# Architectural Overview

### <i> 1.1 System Components: </i>

<b> 1. FastAPI Application: </b>

- Handles API requests and responses.

- Interfaces with the database to store and retrieve chat history.

- Uses LangChain for processing and generating responses.

<b> 2. Database (PostgreSQL): </b>

- Stores chat history and user interactions.

- Configured through SQLAlchemy ORM for seamless data management..

<b> 3. LangChain Integration: </b>

- Manages conversational memory and agents.

- Utilizes various tools for information retrieval and response generation.

<b> 4. Streamlit Application: </b>

- Provides a user-friendly interface for interacting with the chat bot and viewing chat history.

### <i> 1.2 System Workflow: </i>

<b> 1. User Interaction: </b>

- User submits a query via the Streamlit interface.
- Query is sent to the FastAPI backend through a POST request.

<b> 2. Processing the Query: </b>

- FastAPI routes the request to the LangChain agent for processing.
- The agent generates a response using the available tools and memory.

<b> 3. Storing Chat History: </b>

- The response, along with the user input, is saved to the PostgreSQL database.

<b> 4. Retrieving Chat History: </b>

- Users can view past interactions through the Streamlit interface by querying the FastAPI backend.

### <i> 1.3 Flowchart </i>
Below is a flowchart that visually represents the workflow of the system:
``` bash

   Start
     |
     v
 User Input (Streamlit)
     |
     v
API Request Handling (FastAPI)
     |
     v
Processing the Request (LangChain Agent)
     |
     v
     Fetching Data
  /            |         \
 /             |          \
KnowledgeBase Wikipedia DuckDuckGo 
     |
     v
Generating Response (LangChain Agent)
     |
     v
 Saving Chat History (PostgreSQL)
     |
     v
 Returning Response (FastAPI)
     |
     v
Displaying Response (Streamlit)
     |
     v
    End
```