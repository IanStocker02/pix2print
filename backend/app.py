from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)

# Load MongoDB URI and JWT secret from environment variables
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "your-jwt-secret-key")  # Default secret key

# Enable CORS
CORS(app)

# Initialize JWT
jwt = JWTManager(app)

# MongoDB Connection (optional to show usage here, or delegate it to database.py)
from utils.database import db  # Ensure your MongoDB connection file is correct

# Register blueprints
from routes.auth import auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)