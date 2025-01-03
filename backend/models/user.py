from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from utils.database import db  # Import the database connection

users_collection = db.users  # Replace with your collection name

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

def find_user(username: str):
    return users_collection.find_one({"username": username})

def verify_password(stored_password: str, provided_password: str):
    return check_password_hash(stored_password, provided_password)