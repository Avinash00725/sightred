#!/usr/bin/env python
"""
init_db.py - Initialize database for development/production
Works on Windows, macOS, and Linux
"""
import os
import sys
from pathlib import Path

def init_database():
    """Initialize database tables."""
    
    # Check if .env exists
    env_path = Path('.env')
    if not env_path.exists():
        print("❌ Error: .env file not found!")
        print("\n📝 Create .env file from example:")
        print("   cp .env.example .env")
        print("   # Then edit .env with your actual values")
        sys.exit(1)
    
    # Load environment variables from .env
    from dotenv import load_dotenv
    load_dotenv()
    
    # Create database tables
    print("🔧 Initializing database...")
    print("📦 Creating database tables...")
    
    try:
        from app import create_app, db
        app = create_app()
        
        with app.app_context():
            db.create_all()
            
            # Check if tables were created
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            print("\n✅ Database initialized successfully!")
            print(f"   Tables created: {', '.join(tables)}")
            
    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        sys.exit(1)
    
    print("\n📋 Next steps:")
    print("   1. Run: python main.py")
    print("   2. Visit: http://localhost:5000")
    print("   3. Register a new account")
    print("   4. Start searching!")

if __name__ == "__main__":
    init_database()
