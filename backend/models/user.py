from pymongo import MongoClient
from werkzeug.security import generate_password_hash

client = MongoClient("mongodb://localhost:27017")
db = client.pix2print  # Replace with your database name
users_collection = db.users  # Replace with your collection name

# Example of inserting a user
def create_user(username: str, password: str):
    if users_collection.find_one({"username": username}):
        raise ValueError("Username already exists")

    hashed_password = generate_password_hash(password)
    user = {
        "username": username,
        "password": hashed_password,  # Store hashed password
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    users_collection.insert_one(user)
    return user
