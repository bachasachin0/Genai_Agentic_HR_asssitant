import os
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI"),
MONGO_DB = "company_employees",
MONGO_COLLECTION = "employees_records",
LANGCHAIN_API_KEY = os.getenv("LANCHAIN_API_KEY"),
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY"),
GROQ_API_KEY = os.getenv("GROQ_API_KEY"),
OPEN_AI_EMBEDDING_MODEL_DIMENSION = 768
ATLAS_VECTOR_SEARCH_INDEX = "vector_index"
