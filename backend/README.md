# MathTutor Coaching API

FastAPI backend that provides coaching feedback for your MathTutor React app.

## Features

- **Static Mode**: Original hardcoded coaching messages
- **AI Mode**: 5 different AI teaching harnesses
- **CORS Enabled**: Works with React frontend
- **OpenAPI Docs**: Interactive API documentation

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Set API Key (for AI mode)

```bash
# In project root .env file
ANTHROPIC_API_KEY=your_key_here
```

### 3. Run Server

```bash
python server.py
```

Server runs at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

## API Endpoints

### GET /api/harnesses
List available coaching strategies.

### POST /api/coach
Get coaching feedback.

**Request:**
```json
{
  "mode": "ai",
  "harness": "socratic",
  "context": {
    "question": "What is 2 + 3?",
    "correct_answer": 5,
    "student_answer": 4,
    "attempt": 1,
    "hint_used": false,
    "is_correct": false,
    "hint": "Try counting on your fingers"
  }
}
```

**Response:**
```json
{
  "message": "Not quite. What happens when you combine 2 items with 3 more items?",
  "hint": "Try counting on your fingers",
  "show_hint": true,
  "show_answer": false,
  "encouragement": "Keep going!"
}
```

### POST /api/reset/{harness}
Reset conversation history for a harness.

### GET /api/health
Health check with AI availability status.

## Available Harnesses

| Harness | Strategy | Best For |
|---------|----------|----------|
| `socratic` | Guided questioning | Deep understanding |
| `direct` | Clear explanations | Quick learning |
| `step-by-step` | Sequential steps | Complex problems |
| `discovery` | Pattern exploration | Building intuition |
| `adaptive` | Personalized approach | Mixed abilities |

## Usage with React App

See `frontend/src/utils/coachingAPI.js` for client integration example.

## Testing the API

### Using curl
```bash
# Test static mode
curl -X POST http://localhost:8000/api/coach \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "static",
    "context": {
      "question": "What is 5 + 3?",
      "correct_answer": 8,
      "student_answer": 7,
      "attempt": 1,
      "is_correct": false
    }
  }'

# Test AI mode
curl -X POST http://localhost:8000/api/coach \
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
  }'
```

### Using httpie
```bash
# Install: pip install httpie

http POST localhost:8000/api/coach \
  mode=static \
  context:='{"question":"What is 5+3?","correct_answer":8,"student_answer":7,"attempt":1,"is_correct":false}'
```

### Using the Interactive Docs
Visit `http://localhost:8000/docs` for Swagger UI with live API testing.

## Development

### Run with auto-reload
```bash
uvicorn server:app --reload --port 8000
```

### Run tests
```bash
pytest test_server.py
```

## Deployment

### Production server
```bash
gunicorn server:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker
```bash
docker build -t mathtutor-api .
docker run -p 8000:8000 --env-file .env mathtutor-api
```

## Configuration

Environment variables (in `.env`):
- `ANTHROPIC_API_KEY` - Required for AI mode
- `CORS_ORIGINS` - Allowed CORS origins (optional)
- `LOG_LEVEL` - Logging level (default: info)

## Cost Estimation

AI mode costs (per coaching interaction):
- Socratic/Discovery: ~$0.002-0.005 (more exploratory)
- Direct/Step-by-Step: ~$0.001-0.003 (more focused)
- Adaptive: ~$0.002-0.004 (variable)

Static mode: Free (no API calls)

## Troubleshooting

### "AI mode requires ANTHROPIC_API_KEY"
Add your API key to `.env` file in project root.

### CORS errors
Add your frontend URL to `allow_origins` in `server.py`.

### Import errors
Make sure you're running from the `backend/` directory or the project root with proper Python path.
