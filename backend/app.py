from flask import Flask, request, jsonify, send_from_directory
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename
from image_processor import process_image  # Ensure this is correctly defined and imported

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "your-jwt-secret-key")
app.config["UPLOAD_FOLDER"] = "./uploads"
app.config["SAVE_FOLDER"] = "./processed"

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
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)
    
    # Process the image using image_processor.py
    processed_files = process_image(filepath, app.config["SAVE_FOLDER"])
    
    return jsonify({'message': 'Image processed successfully', 'files': processed_files}), 200

@app.route('/images/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_from_directory(app.config["SAVE_FOLDER"], filename)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)