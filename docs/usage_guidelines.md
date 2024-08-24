# Usage Guidelines

### <i> 1.1 Interacting with the Chat Bot: </i>
<b> 1. Access the Streamlit Interface: </b>

- Open your web browser and navigate to http://localhost:8501.

<b> 2. Using the Chat Bot: </b>

- Enter your query in the text input field.

- Click the "Submit" button to send the query to the FastAPI backend.

- The bot will process the query and return the response.

<b> 3. Viewing Chat History: </b>

- Use the sidebar to select from the available chat history.

- View details such as user input, agent's response, and timestamp.

### <i> 1.2 API Endpoints: </i>
<b> 1. Ask the Agent: </b>

- Endpoint: POST /ask

- Request Body:

```json
{
  "input": "Your query here"
}
```

- Response:
```json
{
  "response": "Agent's response here"
}
```

<b> 2. Get Chat History: </b>

- <b> Endpoint: </b> GET /chat_history

- <b> Query Parameters: </b>
    - <i>skip:</i>  Number of records to skip (default: 0).
    - <i>limit:</i> Number of records to retrieve (default: 10).

- <b> Response: </b>

```json

[
  {
    "id": 1,
    "user_input": "User's input",
    "agent_response": "Agent's response",
    "timestamp": "Formatted timestamp"
  }
]
```

### <i> 1.3 API Documentation: </i>

Access the interactive API documentation at:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
