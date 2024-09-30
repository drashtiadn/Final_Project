import streamlit as st  # Importing Streamlit for creating web interfaces
import requests  # Importing requests to make HTTP requests
from typing import List  # Importing List for type hinting
from dotenv import load_dotenv  # Importing dotenv to load environment variables
import os

# Load environment variables from the .env file
load_dotenv()

# Get the FastAPI base URL from the environment variables
FASTAPI_BASE_URL = os.getenv("FASTAPI_BASE_URL")

# Define a function to fetch chat history from the FastAPI endpoint
# This function retrieves chat history records from the backend server
def get_chat_history(skip: int = 0, limit: int = 100):
    try:
        # Make a GET request to the FastAPI endpoint to fetch chat history
        response = requests.get(f"{FASTAPI_BASE_URL}/chat_history?skip={skip}&limit={limit}")
        
        # Raise an error if the request was unsuccessful
        response.raise_for_status()
        
        # Return the JSON response, which contains the chat history
        return response.json()
    except requests.RequestException as e:
        # If an error occurs during the request, display an error message using Streamlit
        st.error(f"Error fetching chat history: {e}")
        
        # Return an empty list in case of an error
        return []

# Streamlit interface
# Set the title of the Streamlit app
st.title("Intelligent Bus Inquiry Assistance Chat Bot 🚌")

# Sidebar for chat history
# Set the title of the sidebar where chat history will be displayed
st.sidebar.title("Chat History")

# Retrieve chat histories using the previously defined function
chat_histories = get_chat_history()

# If chat histories are available
if chat_histories:
    # Create a dictionary to map chat index to the chat record
    # This helps in displaying and selecting a specific chat history
    chat_options = {f"Chat {i+1} - {chat['timestamp']}": chat for i, chat in enumerate(chat_histories)}
    
    # Create a dropdown menu in the sidebar to select a specific chat history
    selected_chat = st.sidebar.selectbox("Select a chat history", list(chat_options.keys()))

    # Display the selected chat history details
    if selected_chat:
        # Retrieve the chat data corresponding to the selected option
        chat = chat_options[selected_chat]
        
        # Display the user's input from the selected chat history
        st.sidebar.write(f"**User Input:** {chat['user_input']}")
        
        # Display the agent's response from the selected chat history
        st.sidebar.write(f"**Agent's Response:** {chat['agent_response']}")
        
        # Display the timestamp of the selected chat history
        st.sidebar.write(f"**Timestamp:** {chat['timestamp']}")
else:
    # If no chat history is available, display a message in the sidebar
    st.sidebar.write("No chat history available.")

# User input
# Create a text input field where the user can enter their query
user_input = st.text_input("Enter your query:")

# If the submit button is pressed
if st.button("Submit"):
    if user_input:
        # Send a POST request to the FastAPI endpoint with the user's input
        response = requests.post(f"{FASTAPI_BASE_URL}/ask", json={"input": user_input})
        
        # If the request is successful (status code 200)
        if response.status_code == 200:
            # Retrieve the response from the server and display it using Streamlit
            result = response.json()
            st.write(result["response"])
        else:
            # If there's an error, display an error message
            st.error("Error: Unable to get the response from the server.")
    else:
        # If the user input is empty, display a warning message
        st.warning("Please enter a query.")
