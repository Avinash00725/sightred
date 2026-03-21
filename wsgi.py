"""
WSGI application entry point for production deployment.
Used by Gunicorn, uWSGI, and other production servers.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app import create_app, db

# Create Flask application
app = create_app()

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()
