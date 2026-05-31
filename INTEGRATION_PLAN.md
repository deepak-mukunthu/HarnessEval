# Integration Plan: MathTutor + Harness Evaluation

## Current State

### Your Existing MathTutor (React App)
- **Location**: `/Users/dmukunthu/Documents/PersonalProjects/MathTutor-Original`
- **Tech**: React + Vite
- **Coaching**: Hardcoded messages in `Quiz.jsx` (lines 24-74)
- **Question Generation**: Client-side in `questionGenerator.js`
- **Feedback**: Static messages based on attempt count

### New HarnessEval Project (Python Evaluation Framework)
- **Location**: `/Users/dmukunthu/Documents/PersonalProjects/HarnessEval`
- **Tech**: Python + Claude API + Dash
- **Purpose**: Evaluate 5 different AI coaching strategies
- **Output**: Metrics & dashboard

## Hybrid Architecture

```
┌─────────────────────────────────────────────────────────┐
│           Your React MathTutor (Frontend)               │
│  - Student interface                                     │
│  - Quiz interaction                                      │
│  - Display coaching messages                             │
└──────────────┬──────────────────────────────────────────┘
               │
               │ REST API
               │
┌──────────────▼──────────────────────────────────────────┐
│         Coaching API Server (Flask/FastAPI)             │
│  - Receives: question, student answer, attempt #        │
│  - Returns: coaching message, hint, feedback            │
│  - Modes: Static (original) OR AI (harness)             │
└──────────────┬──────────────────────────────────────────┘
               │
               ├─► Static Mode: Original hardcoded messages
               │
               └─► AI Mode: Claude API with harness strategies
                   ├─► Socratic Method
                   ├─► Direct Instruction
                   ├─► Step-by-Step
                   ├─► Discovery Learning
                   └─► Adaptive
```

## Implementation Phases

### Phase 1: Backend API Server ✅
Create FastAPI server that:
- Exposes `/api/coach` endpoint
- Supports both static and AI modes
- Integrates 5 harness strategies
- Logs interactions for evaluation

### Phase 2: React Integration
Modify your Quiz.jsx to:
- Call coaching API instead of local functions
- Support mode switching (Static vs AI)
- Display AI-generated coaching messages
- Track harness performance

### Phase 3: Evaluation Mode
Add evaluation interface:
- Admin panel to compare harnesses side-by-side
- Automatic testing across all harnesses
- Real-time metrics dashboard
- Export results for analysis

### Phase 4: Hybrid Dashboard
Combine:
- Your student-facing React app
- Harness evaluation dashboard
- Performance comparison tools
- A/B testing framework

## File Structure

```
HarnessEval/
├── backend/                    # NEW: API Server
│   ├── server.py               # FastAPI server
│   ├── coaching_service.py     # Coaching logic
│   └── harnesses/              # Reuse existing harnesses
│
├── src/                        # Existing Python evaluation
│   ├── harnesses/
│   ├── evaluator.py
│   └── dashboard.py
│
├── frontend/                   # NEW: Modified MathTutor
│   ├── src/
│   │   ├── components/
│   │   │   ├── Quiz.jsx        # Modified to use API
│   │   │   ├── HarnessSelector.jsx  # NEW
│   │   │   └── EvaluationMode.jsx   # NEW
│   │   └── utils/
│   │       └── coachingAPI.js  # NEW: API client
│   └── package.json
│
└── evaluation/                 # Automated testing
    ├── run_ab_test.py
    └── analyze_results.py
```

## API Design

### Endpoint: POST /api/coach

**Request:**
```json
{
  "mode": "ai",               // "static" or "ai"
  "harness": "socratic",      // "socratic", "direct", etc.
  "context": {
    "question": "What is 2 + 3?",
    "correct_answer": 5,
    "student_answer": 4,
    "attempt": 1,
    "hint_used": false,
    "is_correct": false
  }
}
```

**Response:**
```json
{
  "message": "Not quite. What happens when you add 2 items to 3 items?",
  "hint": "Try counting: 1, 2, then 3, 4, 5",
  "show_hint": true,
  "show_answer": false,
  "encouragement": "You're close! Think it through."
}
```

## Benefits of Hybrid Approach

1. **Backward Compatible**: Your app works as-is with static mode
2. **Progressive Enhancement**: Enable AI gradually
3. **Real User Data**: Test harnesses with actual students
4. **Side-by-Side Comparison**: Static vs AI coaching
5. **Extensible**: Easy to add new harnesses
6. **Cost Control**: Choose when to use AI vs static

## Next Steps

Choose your path:

### Option A: Quick Integration (1-2 hours)
- Create minimal FastAPI backend
- Modify Quiz.jsx to support API calls
- Test with one harness

### Option B: Full Evaluation System (4-6 hours)
- Complete backend with all harnesses
- Evaluation mode in React
- Automated testing framework
- Combined dashboard

### Option C: Research-Focused (6-8 hours)
- Option B + Real user A/B testing
- Statistical analysis tools
- Academic paper-ready metrics
- Publication-quality visualizations

## Recommended: Start with Option A

Let's build a minimal working integration:

1. Create FastAPI server with your existing harnesses
2. Add API client to React app
3. Modify Quiz.jsx to support both modes
4. Test with one problem to validate approach
5. Expand from there

Would you like me to proceed with Option A?
