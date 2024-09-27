import os  # Importing the 'os' module for interacting with the operating system
from dotenv import load_dotenv  # Importing 'load_dotenv' to load environment variables from a .env file

# Load environment variables from a .env file into the system's environment
# This makes the variables defined in the .env file available for use in the script
load_dotenv()

# Fetch the value of the environment variable 'GOOGLE_API_KEY'
# If the variable is not found, it will return 'None'
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# At this point, the 'GOOGLE_API_KEY' variable holds the API key value
# (if it's set in the .env file), which can be used for configuring API access in the application
HUGGING_FACE_TOKEN= os.getenv("HUGGING_FACE_TOKEN")