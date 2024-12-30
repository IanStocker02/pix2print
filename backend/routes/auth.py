from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient

# Create a Blueprint for auth
auth_blueprint = Blueprint("auth", __name__)

# MongoDB setup (ensure this matches your main app configuration)
client = MongoClient("mongodb://localhost:27017")
db = client.pix2print
users_collection = db.users

# Signup route
@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    if len(username) < 3 or len(password) < 6:
        return jsonify({'message': 'Username must be at least 3 characters and password at least 6 characters long'}), 400

    # Check if the user already exists
    if users_collection.find_one({"username": username}):
        return jsonify({'message': 'Username already exists'}), 400

    # Hash the password and save to database
    hashed_password = generate_password_hash(password)
    users_collection.insert_one({"username": username, "password": hashed_password})

    return jsonify({'message': 'User created successfully'}), 201

# Login route
@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    # Find the user in the database
    user = users_collection.find_one({"username": username})
    if not user:
        return jsonify({'message': 'User does not exist'}), 404

    if not check_password_hash(user["password"], password):
        return jsonify({'message': 'Invalid password'}), 401

    # Generate JWT token
    access_token = create_access_token(identity=username)
    return jsonify({'message': f'Welcome, {username}', 'access_token': access_token}), 200

# Example protected route
@auth_blueprint.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify({'message': 'You have access to this route'}), 200
