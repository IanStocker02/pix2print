from flask import Flask, request, jsonify, send_from_directory
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename
from image_processor import process_image  # Ensure this is correctly defined and imported
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask app
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "your-jwt-secret-key")
app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER", "./uploads")
app.config["SAVE_FOLDER"] = os.getenv("SAVE_FOLDER", "./processed")

# Log the loaded environment variables
logging.info(f"JWT_SECRET_KEY: {app.config['JWT_SECRET_KEY']}")
logging.info(f"UPLOAD_FOLDER: {app.config['UPLOAD_FOLDER']}")
logging.info(f"SAVE_FOLDER: {app.config['SAVE_FOLDER']}")

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["SAVE_FOLDER"], exist_ok=True)

CORS(app)
jwt = JWTManager(app)

# Authentication routes
from routes.auth import auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

# Image upload and process route
@app.route('/images/upload', methods=['POST'])
def upload_image():
    logging.info("Received request to upload image")
    if 'file' not in request.files:
        logging.error("No file part in the request")
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        logging.error("No selected file")
        return jsonify({"error": "No selected file"}), 400
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    logging.info(f"Saving file to {filepath}")
    file.save(filepath)
    
    # Process the image using image_processor.py
    logging.info(f"Processing image {filepath}")
    processed_files = process_image(filepath, app.config["SAVE_FOLDER"])
    logging.info(f"Image processed successfully, files: {processed_files}")
    
    return jsonify({'message': 'Image processed successfully', 'files': processed_files}), 200

@app.route('/images/download/<filename>', methods=['GET'])
def download_file(filename):
    logging.info(f"Received request to download file {filename}")
    try:
        return send_from_directory(app.config["SAVE_FOLDER"], filename)
    except FileNotFoundError:
        logging.error(f"File not found: {filename}")
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
