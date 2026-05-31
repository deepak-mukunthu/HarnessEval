#!/bin/bash
# Quick test script for the backend API

echo "======================================"
echo "Testing MathTutor Coaching API"
echo "======================================"
echo ""

# Check if server is running
echo "1. Checking if server is running..."
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "   ✅ Server is running!"
else
    echo "   ❌ Server is not running."
    echo "   Start it with: cd backend && python server.py"
    exit 1
fi

echo ""
echo "2. Testing health endpoint..."
curl -s http://localhost:8000/api/health | python3 -m json.tool

echo ""
echo "3. Testing static coaching (no API key required)..."
curl -s -X POST http://localhost:8000/api/coach \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "static",
    "context": {
      "question": "What is 5 + 3?",
      "correct_answer": 8,
      "student_answer": 7,
      "attempt": 1,
      "is_correct": false,
      "hint": "Try counting from 5"
    }
  }' | python3 -m json.tool

echo ""
echo "4. Testing AI coaching (requires API key)..."
curl -s -X POST http://localhost:8000/api/coach \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "ai",
    "harness": "socratic",
    "context": {
      "question": "What is 5 + 3?",
      "correct_answer": 8,
      "student_answer": 7,
      "attempt": 1,
      "is_correct": false,
      "hint": "Try counting from 5"
    }
  }' | python3 -m json.tool

echo ""
echo "======================================"
echo "✅ Tests complete!"
echo ""
echo "Visit http://localhost:8000/docs for interactive API testing"
echo "======================================"
