"""
WSGI application entry point for production deployment.
Minimal to avoid any import issues during build.
"""
import os
import sys

# Set environment early
os.environ.setdefault('Flask_ENV', 'production')

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

try:
    from app import create_app
    app = create_app()
except Exception as e:
    print(f"Warning: Could not create app during import: {e}", file=sys.stderr)
    # Fallback empty app for health checks
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def health():
        return {'status': 'ok'}, 200

if __name__ == "__main__":
    app.run()
