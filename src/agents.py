# Importing the necessary modules and classes from the LangChain library
from langchain.memory import ConversationBufferMemory  # For managing conversation memory
from langchain.agents import create_openai_tools_agent, AgentExecutor  # For creating agents and executing their tasks
from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchResults  # Tools for querying Wikipedia and DuckDuckGo
from langchain_community.utilities import WikipediaAPIWrapper, DuckDuckGoSearchAPIWrapper  # Utility wrappers for API interactions
from langchain_community.document_loaders import PyPDFLoader  # For loading PDF documents into the system
from langchain_community.vectorstores import Chroma  # Vector store for managing embeddings and document retrieval
from langchain_text_splitters import RecursiveCharacterTextSplitter  # Tool for splitting text into manageable chunks
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI  # Google AI tools for embeddings and chat capabilities
from langchain.tools.retriever import create_retriever_tool  # To create a retriever tool for document searches
from langchain import hub  # For pulling pre-built agents from the LangChain hub
import google.generativeai as genai  # Google Generative AI Software Development Kit

from utils import GOOGLE_API_KEY  # Import the Google API key from a utilities file

# Initialize memory for the agent to keep track of conversation context
memory = ConversationBufferMemory()

# Initialize tools for the agent to use
# Wikipedia API Wrapper: Limits results to top 1 and truncates content to 200 characters
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)
# WikipediaQueryRun: Wraps around the Wikipedia API to enable querying Wikipedia
wiki = WikipediaQueryRun(api_wrapper=api_wrapper)

# DuckDuckGo API Wrapper: Configures the wrapper to fetch news from Germany within the last day, limiting to 2 results
duckduckgo_wrapper = DuckDuckGoSearchAPIWrapper(region="de-de", time="d", max_results=2)
# DuckDuckGoSearchResults: Tool to retrieve search results from DuckDuckGo based on the API wrapper
duckduckgo = DuckDuckGoSearchResults(api_wrapper=duckduckgo_wrapper, source="news")

# PDF Loader: Loads a PDF file named "Knowledgebase.pdf" into the system
loader = PyPDFLoader("Knowledgebase.pdf")
docs = loader.load()  # Loads the documents from the PDF

# Text Splitter: Splits the documents into chunks of 1000 characters, with a 200-character overlap
documents = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(docs)

# Chroma Vector Store: Creates a vector store from the document chunks using Google Generative AI embeddings
vectordb = Chroma.from_documents(documents, GoogleGenerativeAIEmbeddings(model="models/embedding-001"))

# Retriever: Converts the vector store into a retriever to search for relevant document chunks
retriever = vectordb.as_retriever()

# Retriever Tool: Creates a retriever tool specifically for searching bus-related information
retriever_tool = create_retriever_tool(
    retriever,  # The retriever object
    "bus_information_search",  # Name of the tool
    "Search for information regarding bus schedules, routes, fares, and other relevant information. For any questions about Bus related information, you must use this tool!"  # Description
)

# Combine all tools into a list
tools = [retriever_tool, wiki, duckduckgo]

# Initialize the Large Language Model (LLM) for generating responses
# Uses Google Generative AI's "gemini-1.5-flash" model with a temperature setting of 0 for deterministic outputs
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

# Pull a pre-built agent prompt from the LangChain hub
prompt = hub.pull("hwchase17/openai-functions-agent")

# Create an OpenAI tools agent using the LLM and the list of tools, with the pulled prompt
agent = create_openai_tools_agent(llm, tools, prompt)

# Initialize the Agent Executor
# This wraps the agent with memory, allowing the agent to remember past interactions
agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)

# Configure the Google Generative AI API with the provided API key
genai.configure(api_key=GOOGLE_API_KEY)
