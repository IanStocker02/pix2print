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
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "your-jwt-secret-key")  # Default secret key

# Enable CORS
CORS(app)

# Initialize JWT
jwt = JWTManager(app)

# Import and register the auth blueprint
from routes.auth import auth_blueprint  # Use the subfolder name 'auth'

app.register_blueprint(auth_blueprint, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)
