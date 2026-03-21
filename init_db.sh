#!/bin/bash
# init_db.sh - Initialize database for development/production

set -e

echo "🔧 Initializing database..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "📝 Please create .env file from .env.example:"
    echo "   cp .env.example .env"
    echo "   # Then edit .env with your actual values"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '#' | xargs)

# Create database tables
echo "📦 Creating database tables..."
python -c "
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print('✅ Database tables created successfully!')
"

echo ""
echo "✅ Database initialization complete!"
echo ""
echo "Next steps:"
echo "  1. Run: python main.py"
echo "  2. Visit: http://localhost:5000"
echo "  3. Register a new account"
echo "  4. Start searching!"
