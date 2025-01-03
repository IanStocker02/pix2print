from flask import Flask, request, jsonify, send_from_directory
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename
from main import process_image, upload_image  # Import your main.py processing function

# Load environment variables
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)

# Load MongoDB URI and JWT secret from environment variables
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "your-jwt-secret-key")  # Default secret key
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["PROCESSED_FOLDER"] = "processed"

# Enable CORS
CORS(app)

# Initialize JWT
jwt = JWTManager(app)

# MongoDB Connection (optional to show usage here, or delegate it to database.py)
from utils.database import db  # Ensure your MongoDB connection file is correct

# Import and register the auth blueprint
from routes.auth import auth_blueprint

app.register_blueprint(auth_blueprint, url_prefix='/auth')

# Ensure upload and processed folders exist
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["PROCESSED_FOLDER"], exist_ok=True)

# Register the upload_image route from main.py
app.add_url_rule('/images/upload', 'upload_image', upload_image, methods=['POST'])

@app.route('/images/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config["PROCESSED_FOLDER"], filename)

if __name__ == '__main__':
    app.run(debug=True)