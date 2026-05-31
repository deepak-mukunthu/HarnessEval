#!/bin/bash
# Start the MathTutor backend server

cd "$(dirname "$0")"

echo "=========================================="
echo "🎓 Starting MathTutor Server"
echo "=========================================="
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️  Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📦 Installing dependencies..."
    pip install -q -r backend/requirements.txt
    echo "✅ Setup complete"
fi

echo ""
echo "🚀 Starting server..."
echo ""

cd backend
python server.py
