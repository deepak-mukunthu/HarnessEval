# Hybrid MathTutor System - Complete Guide

## What You Now Have

A **hybrid system** that combines:
1. Your existing **React MathTutor** (student-facing quiz app)
2. **5 AI coaching harnesses** (different teaching strategies)
3. **Evaluation framework** (compare effectiveness)
4. **Backend API** (bridges React ↔ AI harnesses)

## Architecture Overview

```
┌──────────────────────────────────────────────────────────┐
│        Your Existing React MathTutor                     │
│  github.com/deepak-mukunthu/MathTutor                    │
│  Location: ../MathTutor-Original/                        │
│                                                           │
│  Can be modified to call ──────┐                         │
└────────────────────────────────┼─────────────────────────┘
                                 │
                                 │ HTTP API
                                 │
┌────────────────────────────────▼─────────────────────────┐
│              Backend API Server                          │
│  Location: HarnessEval/backend/                          │
│  Port: http://localhost:8000                             │
│                                                           │
│  Endpoints:                                              │
│    POST /api/coach  - Get coaching feedback              │
│    GET  /api/harnesses - List strategies                 │
│                                                           │
│  Modes:                                                  │
│    - static: Your original hardcoded messages            │
│    - ai: Claude API with harnesses                       │
└────────────────────────────────┬─────────────────────────┘
                                 │
                                 │
┌────────────────────────────────▼─────────────────────────┐
│           5 Coaching Harnesses                           │
│  Location: HarnessEval/src/harnesses/                    │
│                                                           │
│  • Socratic Method - Guided questioning                  │
│  • Direct Instruction - Clear explanations               │
│  • Step-by-Step - Sequential guidance                    │
│  • Discovery Learning - Pattern exploration              │
│  • Adaptive - Personalized approach                      │
│                                                           │
│  Each uses Claude API (Sonnet 4.6)                       │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│         Evaluation & Analytics                           │
│  Location: HarnessEval/src/                              │
│                                                           │
│  • evaluator.py - Track metrics                          │
│  • dashboard.py - Visualize results                      │
│  • run_experiment.py - Automated testing                 │
└──────────────────────────────────────────────────────────┘
```

## Quick Start

### Step 1: Start the Backend API

```bash
cd backend
pip install -r requirements.txt
python server.py
```

Server will be at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

### Step 2: Test the API

```bash
# Test health check
curl http://localhost:8000/api/health

# Test static coaching (works without API key)
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

# Test AI coaching (requires API key in .env)
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

### Step 3: Integrate with Your React App

#### Option A: Quick Test (No React Changes)
Use the interactive API docs to test harnesses:
1. Open `http://localhost:8000/docs`
2. Try POST `/api/coach` with different harnesses
3. Compare responses

#### Option B: Full Integration (Modify React)
See `REACT_INTEGRATION.md` for step-by-step guide to modify your Quiz.jsx

## Project Structure

```
HarnessEval/
├── backend/                      # ✨ NEW: API Server
│   ├── server.py                 # FastAPI app
│   ├── coaching_service.py       # Coaching logic
│   ├── requirements.txt
│   └── README.md
│
├── src/                          # Existing: Harnesses & Evaluation
│   ├── harnesses/
│   │   ├── socratic.py
│   │   ├── direct.py
│   │   ├── step_by_step.py
│   │   ├── discovery.py
│   │   └── adaptive.py
│   ├── evaluator.py
│   ├── dashboard.py
│   └── math_tutor.py
│
├── data/
│   ├── test_problems.json        # Test problems
│   └── results/                  # Experiment results
│
├── run_experiment.py             # Automated experiments
├── analysis_notebook.py          # Interactive analysis
│
└── ../MathTutor-Original/        # Your existing React app
    ├── src/
    │   ├── components/
    │   │   ├── Quiz.jsx          # To be modified
    │   │   └── ...
    │   └── utils/
    │       └── questionGenerator.js
    └── package.json
```

## Usage Modes

### Mode 1: Standalone Evaluation
Test harnesses without React app (what we built first):

```bash
# Run automated experiment
python run_experiment.py 3

# View results dashboard
python src/dashboard.py
```

### Mode 2: API Testing
Test different coaching strategies via API:

```bash
# Start server
cd backend && python server.py

# Use API docs for interactive testing
open http://localhost:8000/docs
```

### Mode 3: React Integration
Use AI coaching in your actual MathTutor app:

1. Modify Quiz.jsx to call `/api/coach`
2. Add harness selector component
3. Students get AI-powered coaching!

### Mode 4: A/B Testing
Compare harnesses with real students:

1. Deploy backend + modified React app
2. Route 20% of students to each harness
3. Collect metrics and analyze

## Comparison: Original vs Hybrid

### Your Original MathTutor

**Pros:**
- ✅ Simple, no backend needed
- ✅ Fast, no API latency
- ✅ Free, no API costs
- ✅ Works offline

**Cons:**
- ❌ Static messages only
- ❌ Can't adapt to student context
- ❌ No personalization
- ❌ Limited variety

**Code:** Hardcoded in Quiz.jsx lines 24-74

### Hybrid with AI Harnesses

**Pros:**
- ✅ Dynamic, context-aware coaching
- ✅ 5 different teaching strategies
- ✅ Personalized to student responses
- ✅ Can be evaluated and improved
- ✅ Backward compatible (static mode)

**Cons:**
- ❌ Requires backend server
- ❌ API latency (~1-2 seconds)
- ❌ Costs ~$0.001-0.005 per interaction
- ❌ Needs internet connection

**Code:** Backend API + Claude harnesses

## Use Cases

### For Research
- Compare teaching strategies
- Publish papers on AI tutoring
- Evaluate effectiveness metrics
- A/B test with real students

### For Production
- Deploy as premium feature
- Offer "AI Tutor" mode
- Personalize to student needs
- Collect learning analytics

### For Learning
- Understand prompt engineering
- Experiment with teaching styles
- Build portfolio project
- Demonstrate full-stack skills

## Key Features

### 1. Backward Compatible
Your React app still works with static mode (no changes needed).

### 2. Progressive Enhancement
Enable AI gradually:
- Start with static mode
- Test one harness
- Roll out to subset of users
- Full deployment when ready

### 3. Cost Control
- Static mode: Free
- AI mode: Pay per interaction
- Choose when to use AI
- Set budget limits

### 4. Evaluation Framework
- Track metrics automatically
- Compare harnesses
- Visualize results
- Make data-driven decisions

### 5. Extensible
- Add new harnesses easily
- Customize prompts
- Integrate new features
- Scale as needed

## Next Steps

### Option 1: Just Test the API (5 minutes)
```bash
cd backend
python server.py
# Visit http://localhost:8000/docs
```

### Option 2: Run Automated Evaluation (15 minutes)
```bash
# Test all harnesses on sample problems
python run_experiment.py 3

# View dashboard
python src/dashboard.py
```

### Option 3: Full React Integration (1-2 hours)
1. Read `REACT_INTEGRATION.md`
2. Modify your Quiz.jsx
3. Add harness selector
4. Test with students

### Option 4: Deploy to Production (4-6 hours)
1. Deploy backend (Heroku, Railway, etc.)
2. Update CORS settings
3. Modify React to use production API
4. Deploy updated React app

## Configuration

### Backend (.env in project root)
```bash
ANTHROPIC_API_KEY=sk-ant-...
```

### React (optional, in .env.local)
```bash
VITE_API_URL=http://localhost:8000
VITE_COACHING_MODE=static  # or 'ai'
VITE_DEFAULT_HARNESS=socratic
```

## Testing Strategy

### Phase 1: API Testing
- ✅ Test all endpoints
- ✅ Verify static mode works
- ✅ Verify AI mode works
- ✅ Test each harness

### Phase 2: Integration Testing
- ⏳ Modify Quiz.jsx
- ⏳ Test with sample problems
- ⏳ Verify coaching appears correctly
- ⏳ Check error handling

### Phase 3: User Testing
- ⏳ Small group of students
- ⏳ Collect feedback
- ⏳ Monitor metrics
- ⏳ Iterate on prompts

### Phase 4: A/B Testing
- ⏳ Route users to different harnesses
- ⏳ Track performance metrics
- ⏳ Statistical analysis
- ⏳ Choose best harness

## Cost Analysis

### Static Mode (Original)
- API calls: 0
- Cost: $0
- Latency: 0ms

### AI Mode (Hybrid)
Per student session (10 questions):
- API calls: ~30-40 (3-4 per question)
- Cost: $0.03-0.20
- Latency: ~1-2 seconds per interaction

Monthly (1000 students, 10 quizzes each):
- Total sessions: 10,000
- Total cost: $300-2000
- Per student: $0.30-2.00

**Optimization strategies:**
- Use static for easy questions
- Use AI for complex problems
- Cache common responses
- Batch API calls

## Deployment Options

### Backend
- **Heroku**: Easy, free tier available
- **Railway**: Modern, simple setup
- **Render**: Free tier, auto-deploy
- **AWS Lambda**: Serverless, pay per use
- **DigitalOcean**: Full control, $5/month

### React App (No changes needed)
- Your existing GitHub Pages deployment works as-is
- Just point to backend API URL

## Support & Documentation

### API Documentation
- Interactive: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Code Documentation
- Backend: `backend/README.md`
- Harnesses: See docstrings in `src/harnesses/*.py`
- Integration: `REACT_INTEGRATION.md` (to be created)

### Guides
- This file: System overview
- `QUICKSTART.md`: Original evaluation framework
- `ANALYSIS_GUIDE.md`: Interpreting results
- `PROJECT_OVERVIEW.md`: Technical details

## FAQ

**Q: Do I need to modify my React app?**
A: No! You can test harnesses via API first. Integration is optional.

**Q: Can I use this without an API key?**
A: Yes! Static mode works without API key (your original messages).

**Q: How do I add my own harness?**
A: Create new file in `src/harnesses/`, define system prompt, add to server.py.

**Q: Can I use a different AI model?**
A: Yes! Modify `src/math_tutor.py` to use different model/provider.

**Q: How do I choose the best harness?**
A: Run experiments, view dashboard, compare metrics. Or A/B test with real students.

**Q: Is this production-ready?**
A: Backend is solid. Add error handling, monitoring, and rate limiting for production.

---

## 🎉 What You've Built

You now have:
✅ Your original MathTutor (unchanged, still works)
✅ 5 AI teaching harnesses with different strategies
✅ REST API to bridge React ↔ AI
✅ Evaluation framework to compare effectiveness
✅ Dashboard to visualize results
✅ Complete documentation

**Ready to test?** Start with: `cd backend && python server.py`
