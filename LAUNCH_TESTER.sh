#!/bin/bash
# Quick launcher for the Interactive Harness Tester

echo "=========================================="
echo "Launching MathTutor Harness Tester"
echo "=========================================="
echo ""

# Check if backend is running
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "✅ Backend is already running"
else
    echo "⚠️  Backend is not running!"
    echo ""
    echo "Starting backend in background..."
    cd backend && python server.py &
    BACKEND_PID=$!
    echo "Backend PID: $BACKEND_PID"
    sleep 3
fi

echo ""
echo "Opening web interface..."
echo ""

# Try different methods to open the browser
if command -v open &> /dev/null; then
    open frontend/index.html
elif command -v xdg-open &> /dev/null; then
    xdg-open frontend/index.html
elif command -v start &> /dev/null; then
    start frontend/index.html
else
    echo "Please open this file in your browser:"
    echo "$(pwd)/frontend/index.html"
fi

echo ""
echo "=========================================="
echo "✅ Harness Tester is ready!"
echo ""
echo "The web interface should open automatically."
echo "If not, manually open: frontend/index.html"
echo ""
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the backend"
echo "=========================================="

# Keep script running if we started the backend
if [ ! -z "$BACKEND_PID" ]; then
    wait $BACKEND_PID
fi
