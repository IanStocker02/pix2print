from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB Connection URI
DATABASE_URL = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = "pix2print"

# MongoDB Client and Database
client = MongoClient(DATABASE_URL)
db = client[DB_NAME]