from pymongo import MongoClient

# MongoDB Connection URI (Change this when using MongoDB Atlas)
DATABASE_URL = "mongodb://localhost:27017"
DB_NAME = "pix2print"

# MongoDB Client and Database
client = MongoClient(DATABASE_URL)
db = client[DB_NAME]
