# mongodb_utils.py

from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import MONGO_URI, MONGO_DB, MONGO_COLLECTION, ATLAS_VECTOR_SEARCH_INDEX
DATABASE_NAME = "company_employees"
COLLECTION_NAME = "history"
MONGO_COLLECTION= "employees_records"

def get_session_history(session_id: str) -> MongoDBChatMessageHistory:
    # from config import MONGO_URI, DATABASE_NAME
    global MONGO_URI, DATABASE_NAME, COLLECTION_NAME
    return MongoDBChatMessageHistory(MONGO_URI, session_id, database_name = DATABASE_NAME, collection_name=COLLECTION_NAME)

# Vector Store Creation
embedding_model = GoogleGenerativeAIEmbeddings(model='models/text-embedding-004')

vector_store = MongoDBAtlasVectorSearch.from_connection_string(
    connection_string=MONGO_URI,
    namespace=DATABASE_NAME + "." + MONGO_COLLECTION,
    embedding=embedding_model,
    index_name=ATLAS_VECTOR_SEARCH_INDEX,
    text_key="employee_string"
)
