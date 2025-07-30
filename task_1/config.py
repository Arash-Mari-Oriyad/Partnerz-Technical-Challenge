import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
EMBEDDING_MODEL = "text-embedding-3-large"
GENERATION_MODEL = "gpt-4o"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
CHROMA_DB_PATH = "./chroma_db"
