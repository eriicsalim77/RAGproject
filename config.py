import os
from dotenv import load_dotenv
load_dotenv()

DOCS_FOLDER = "docs"
CHROMA_PATH = "./chroma_db"
CHUNK_SIZE = 300
OVERLAP = 50
MIN_CHUNK_LENGTH = 50
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHROMA_COLLECTION = "nyc_tech_jobs"
N_RESULTS = 5
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
