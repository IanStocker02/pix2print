from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import User
from utils.database import db_session
import bcrypt

auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data["username"]
    password = data["password"]

    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Save to database
    user = User(username=username, password=hashed_password)
    db_session.add(user)
    db_session.commit()

    return jsonify(message="User created successfully"), 201

@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    # Find user in database
    user = db_session.query(User).filter_by(username=username).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password):
        return jsonify(message="Invalid username or password"), 401

    # Create JWT
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200
