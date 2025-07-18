import os
from dotenv import load_dotenv

load_dotenv()

DOCUMENTS_DIR = "documents/"
INDEX_DIR = "faiss_index"
PROMPT_PATH = "prompts/decision_prompt.txt"

# OAuth2 and JWT settings
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

SENTENCE_TRANSFORMER_MODEL = 'all-MiniLM-L6-v2'
MAX_CHUNK_SIZE = 1024
OVERLAP = 100
