# Interactive Harness Tester - Web UI

Beautiful web interface for testing AI teaching harnesses in real-time!

## Quick Start

```bash
# 1. Start the backend API
cd backend
python server.py

# 2. Open the web interface
open frontend/index.html
```

That's it! The web interface will connect to your backend at `http://localhost:8000`.

## Features

- ✨ Beautiful, modern UI
- 🎯 Test individual harnesses
- 📊 Compare all harnesses side-by-side
- 🔄 Real-time backend connection status
- 📱 Responsive design
- 🎨 No build step required - pure HTML/CSS/JS

## Usage

1. **Select Mode**: Choose Static (original) or AI (harnesses)
2. **Enter Test Data**: Question, answers, attempt number
3. **Select Harness**: Click on a teaching strategy
4. **Test**: Click "Test Harness" for single test
5. **Compare**: Click "Compare All Harnesses" to see all responses

## Screenshots

### Single Harness Test
Test one harness at a time, see detailed coaching response.

### Compare All Harnesses
See how all 5 harnesses respond to the same problem side-by-side.

## No Server Needed

This is a client-side only HTML file - no npm, no build, no webpack. Just open it in your browser!

The only requirement is that the backend API is running at `http://localhost:8000`.
