from langchain.memory import ConversationBufferMemory
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchResults
from langchain_community.utilities import WikipediaAPIWrapper, DuckDuckGoSearchAPIWrapper
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.tools.retriever import create_retriever_tool
from langchain import hub
import google.generativeai as genai
from utils import HUGGING_FACE_TOKEN
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

# Configure Google Generative AI API with the API key
from utils import GOOGLE_API_KEY
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize memory for conversation context
memory = ConversationBufferMemory()

# Wikipedia tool setup
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)
wiki = WikipediaQueryRun(api_wrapper=api_wrapper)

# DuckDuckGo tool setup for news search in India within the last day
duckduckgo_wrapper = DuckDuckGoSearchAPIWrapper(region="in-en", time="d", max_results=2)
duckduckgo = DuckDuckGoSearchResults(api_wrapper=duckduckgo_wrapper, source="news")

# PDF document loading and text splitting
loader = PyPDFLoader("Knowledgebase.pdf")

docs = loader.load()

documents = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(docs)

huggingface_embeddings=HuggingFaceBgeEmbeddings(
    model_name="dunzhang/stella_en_1.5B_v5",   #"BAAI/bge-small-en-v1.5",      #sentence-transformers/all-MiniLM-l6-v2
    model_kwargs={'device':'cpu'},
    encode_kwargs={'normalize_embeddings':True}

)

import  numpy as np
print(np.array(huggingface_embeddings.embed_query(documents[0].page_content)))
print(np.array(huggingface_embeddings.embed_query(documents[0].page_content)).shape)

vectordb = Chroma.from_documents(documents[:120],huggingface_embeddings)

# Create the retriever
retriever = vectordb.as_retriever()

# Create a retriever tool
retriever_tool = create_retriever_tool(
    retriever, 
    "bus_information_search",
    "Search for information regarding bus schedules, routes, fares, and other relevant information."
)

# List of tools the agent can use
tools = [retriever_tool, wiki, duckduckgo]

# Initialize LLM and create an agent
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
prompt = hub.pull("hwchase17/openai-functions-agent")
agent = create_openai_tools_agent(llm, tools, prompt)

# Initialize the agent executor with memory and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)