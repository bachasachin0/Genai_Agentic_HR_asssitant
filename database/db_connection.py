import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = "company_employees"
COLLECTION_NAME = "employees_records"

def get_mongo_client(mongo_uri: str):
    """Establish connection to MongoDB and ping the database."""
    try:
        client = MongoClient(mongo_uri)
        client.admin.command('ping')
        print("Connection to MongoDB successful")
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def push_data_to_mongo(client, data: list):
    """Push the generated data to MongoDB."""
    db = client.get_database(DATABASE_NAME)
    collection = db.get_collection(COLLECTION_NAME)
    collection.insert_many(data)
    print("Data ingestion into MongoDB completed")

