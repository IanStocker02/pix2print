from flask import Flask, request, jsonify, send_file
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename
from image_processor import process_image

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
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    save_dir = app.config["SAVE_FOLDER"]
    process_image(file_path, save_dir, num_colors=5)

    # Return the path to processed files (we'll assume the processed file is the first one for simplicity)
    processed_files = os.listdir(save_dir)
    if processed_files:
        processed_file_path = processed_files[0]  # Adjust as needed to pick the correct file
        return jsonify({"message": "File processed successfully", "file_path": processed_file_path})
    else:
        return jsonify({"error": "No processed files found"}), 500



@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    save_dir = app.config["SAVE_FOLDER"]
    file_path = os.path.join(save_dir, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
