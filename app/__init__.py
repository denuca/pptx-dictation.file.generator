from app.email_service import send_email  # Optional
from flask import Flask
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SESSION_SECRET_KEY', 'default_secret_key')

    # Flask configuration for session security
    app.config.update(
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=False,
        SESSION_COOKIE_HTTPONLY=True
    )

    # Import and register blueprints/routes here
    from .routes import index
    app.register_blueprint(index)

    return app