# Intelligent Bus Inquiry Assistance Chat Bot 🚌

### <i> Overview: </i>
The Intelligent Bus Inquiry Assistance Chat Bot is an AI-powered application developed using FastAPI and Streamlit. It provides users with information about bus schedules, routes, fares, and more. The chatbot integrates tools like Wikipedia and DuckDuckGo, along with a custom knowledge base, to answer queries. The chat history is stored in a PostgreSQL database, and a user-friendly interface is available via Streamlit.

### <i> Demo Video: </i>

You can watch the demo of the Intelligent Bus Inquiry Assistance Chat Bot [here](https://www.loom.com/share/c26e083d8d9a4073980a4c1e7c79d16f?sid=96c9e19f-a82d-4726-bff3-a4c1341c2635).

### <i> Features: </i>

<b> 1. Natural Language Processing: </b> Uses AI to understand and respond to user queries.

<b> 2. Multi-Tool Integration: </b> Combines Wikipedia, DuckDuckGo, and a custom knowledge base to provide comprehensive answers.

<b> 3. Chat History Management: </b> Stores and retrieves chat history from a PostgreSQL database.

<b> 4. Streamlit Interface: </b> User-friendly interface for querying and reviewing chat history.

<b> 5. API Documentation: </b> Accessible via Swagger UI for easy interaction and testing.

### <i> Knowledge Base: </i>

The chatbot leverages a custom Knowledge Base containing detailed information about bus schedules, routes, fares, and more. You can access the Knowledge Base [here](https://drive.google.com/file/d/1vBgB4RlbA1yYkrg7sOWcxcLJReb9ta6u/view?usp=drive_link).

### <i> Prerequisites: </i>

- Python 3.8+
- FastAPI
- PostgreSQL
- SQLAlchemy
- LangChain and Community Tools
- Uvicorn
- Streamlit


### <i> Project Structure: </i>

``` bash
Final_Project/
│
├── src/
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # SQLAlchemy models and database setup
│   ├── database.py          # Database connection and session management
│   ├── agents.py            # LangChain and other service integrations
│   ├── utils.py             # Utility functions for loading environment variables
│   └── app.py               # Streamlit application for user interface
│ 
├── docs/
│   ├── usage_guidelines.md       # Guidelines on using the chat bot system
│   └── architectural_overview.md # Architectural overview and flowchart
│
├── .gitignore               # Git ignore file to exclude certain files from version control
├── requirements.txt         # List of Python dependencies
├── .env                     # Environment variables configuration
└── README.md                # Project overview and Setup instructions for the project
```

### <i> Setup: </i>

<b> 1. Clone the Repository: </b>
   
```bash

git clone https://github.com/drashtiadn/Final_Project.git

```
<b> 2. Create a virtual environment and install dependencies: </b>

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt

```

<b> 3. Set Up Environment Variables by creating a .env file in the root directory of the project with the following content: </b>

```bash
GOOGLE_API_KEY="your_google_api_key"
USER=postgres
DATABASE=chatdb
PASSWORD=password
HOST=localhost
PORT=5432
```

*** Replace the placeholder values with your actual PostgreSQL credentials and Google API key. ***

<b> 4. Initialize the Database by ensuring PostgreSQL is running and create the database: </b>

```bash
psql -U postgres -c "CREATE DATABASE chatdb;"
```

<b> 5. Run the FastAPI Application: </b>

```bash

uvicorn main:app --reload
```
The application will be available at http://127.0.0.1:8000.


<b> 6. Run the Streamlit Interface in a new terminal: </b>

```bash
streamlit run app.py
```

The Streamlit app will be available at http://localhost:8501.

### <i> Contributing: </i>
Feel free to fork the repository, make improvements, and submit a pull request. All contributions are welcome!

This README.md file provides a complete guide for setting up and using your Intelligent Bus Inquiry Assistance Chat Bot, including instructions for running both the FastAPI backend and the Streamlit interface.