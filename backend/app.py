from flask import Flask
from routes.auth import auth_blueprint
from routes.projects import projects_blueprint

app = Flask(__name__)

# Configurations (e.g., secret key, database URI)
app.config["JWT_SECRET_KEY"] = "your-secret-key"

# Register Blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(projects_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
