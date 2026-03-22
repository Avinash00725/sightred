"""
WSGI application entry point for production deployment.
Used by Gunicorn, uWSGI, and other production servers.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app import create_app

# Create Flask application
app = create_app()

# Database tables are created in app/__init__.py during create_app()
# No need to create them again here

if __name__ == "__main__":
    app.run()
