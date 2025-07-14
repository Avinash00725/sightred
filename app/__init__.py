# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import praw

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# ✅ Reddit instance - don't keep secrets hardcoded in production!
reddit = praw.Reddit(
    client_id="-OY_VDNQWsBKeQEYyRlAsw",
    client_secret="HbKEJ9seAovAAH76qaDtC8Daffc35w",
    user_agent="health_sentinel_v1"
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)

    # Import blueprints here to avoid circular imports
    from app.routes import main as main_blueprint
    from app.auth import auth as auth_blueprint

    # Register blueprints
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
