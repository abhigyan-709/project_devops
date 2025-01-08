from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Database:
    client: MongoClient = None
    db_name: str = "testdb"

    def connect(self):
        mongo_uri = os.environ.get("MONGO_URI")
        if not mongo_uri:
            raise ValueError("MONGO_URI is not set in the environment variables.")
        self.client = MongoClient(mongo_uri)

    def get_client(self) -> MongoClient:
        if not self.client:
            self.connect()
        return self.client

db = Database()
