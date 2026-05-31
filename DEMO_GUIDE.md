# 🎬 Complete Demo Guide

Step-by-step walkthrough to demonstrate all features of the MathTutor Harness Evaluation System.

## 🎯 Demo Overview

This demo showcases:
1. Interactive web UI testing (5 min)
2. API exploration (3 min)
3. Automated evaluation (10 min)
4. Results analysis (5 min)
5. Custom scenarios (5 min)

**Total Time:** ~30 minutes
**Prerequisites:** None! Works out of the box.

---

## 🚀 Demo 1: Interactive Web UI (5 minutes)

### Setup (1 minute)

```bash
cd HarnessEval
source venv/bin/activate  # If already set up
# OR first time: python3 -m venv venv && source venv/bin/activate && pip install -r backend/requirements.txt

cd backend
python server.py
```

Wait for:
```
🎓 MathTutor Coaching API Server
========================================
AI Mode: ❌ Disabled (add ANTHROPIC_API_KEY)

🌐 Web UI:    http://localhost:8000
📚 API Docs:  http://localhost:8000/docs
```

### Part A: Single Harness Test (2 minutes)

1. **Open** http://localhost:8000 in your browser

2. **Notice the UI:**
   - Left panel: Input form
   - Right panel: 5 harness cards (Socratic is selected)
   - Top: Connection status (green dot = connected)

3. **Test Scenario 1 - Wrong Answer:**
   ```
   Question: What is 12 × 8?
   Correct Answer: 96
   Student's Answer: 94
   Attempt: 1
   Hint: Think about 12 groups of 8
   Mode: Static (Original)
   Harness: Socratic (click the card)
   ```

4. **Click "🚀 Test Harness"**

5. **Observe the Response:**
   ```
   "Not quite. Take another look at the problem. 
    What are you solving for?"
   💡 Hint: Think about 12 groups of 8
   💪 Encouragement: You can do this!
   ```

6. **Try Different Harnesses:**
   - Click "Direct" → Notice more explanatory style
   - Click "Step-by-Step" → Notice sequential guidance
   - Click "Discovery" → Notice pattern-focused approach

### Part B: Compare All Harnesses (2 minutes)

1. **Keep the same problem** (12 × 8, student answered 94)

2. **Click "📊 Compare All Harnesses"**

3. **Watch as it tests all 5 strategies** (takes ~5 seconds)

4. **Compare Responses:**
   - **Socratic:** "What happens when you multiply 12 by 8?"
   - **Direct:** "To multiply 12 × 8, let me show you..."
   - **Step-by-Step:** "Let's break this down. Step 1: ..."
   - **Discovery:** "Look at these patterns: 10×8=80, 11×8=88, 12×8=?"
   - **Adaptive:** "Let me check what you know first..."

5. **Notice Differences:**
   - Question marks vs. statements
   - Scaffolding approach
   - Conceptual depth

### Part C: Different Scenarios (1 minute)

**Scenario 2 - Correct Answer:**
```
Question: What is 5 + 3?
Correct Answer: 8
Student's Answer: 8
Check: "Answer is correct" ✓
```

Click "Test Harness" → See celebration responses!

**Scenario 3 - Multiple Attempts:**
```
Question: What is 15 - 7?
Correct Answer: 8
Student's Answer: 9
Attempt: 3 (select from dropdown)
```

Click "Test Harness" → See how coaching changes on final attempt!

---

## 🔧 Demo 2: API Exploration (3 minutes)

### Part A: Interactive API Docs (2 minutes)

1. **Open** http://localhost:8000/docs

2. **Explore Endpoints:**
   - `GET /api/health` - Server status
   - `GET /api/harnesses` - List strategies
   - `POST /api/coach` - Get coaching
   - `POST /api/reset/{harness}` - Reset conversation

3. **Try Health Check:**
   - Click on `GET /api/health`
   - Click "Try it out"
   - Click "Execute"
   - See response:
   ```json
   {
     "status": "healthy",
     "ai_available": false,
     "harnesses_loaded": 0,
     "modes": ["static", "ai"]
   }
   ```

4. **Test Coach Endpoint:**
   - Click on `POST /api/coach`
   - Click "Try it out"
   - Use the pre-filled example or paste:
   ```json
   {
     "mode": "static",
     "harness": "socratic",
     "context": {
       "question": "What is 7 × 6?",
       "correct_answer": 42,
       "student_answer": 40,
       "attempt": 1,
       "is_correct": false,
       "hint": "Think about 7 groups of 6"
     }
   }
   ```
   - Click "Execute"
   - See coaching response!

### Part B: Command Line Testing (1 minute)

```bash
# Terminal test
curl -X POST http://localhost:8000/api/coach \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "static",
    "harness": "direct",
    "context": {
      "question": "What is 9 + 6?",
      "correct_answer": 15,
      "student_answer": 14,
      "attempt": 1,
      "is_correct": false,
      "hint": "Count on from 9"
    }
  }' | python3 -m json.tool
```

**Output:**
```json
{
  "message": "That's not it. Think about what the question is really asking.",
  "hint": "Count on from 9",
  "show_hint": true,
  "show_answer": false,
  "encouragement": "You can do this!"
}
```

---

## 🧪 Demo 3: Automated Evaluation (10 minutes)

### Part A: Quick Experiment (5 minutes)

1. **Open a new terminal** (keep server running in first terminal)

2. **Run experiment on 3 problems:**
   ```bash
   cd HarnessEval
   source venv/bin/activate
   python run_experiment.py 3
   ```

3. **Watch the Progress:**
   ```
   ############################################################
   # Starting Experiment: Testing 5 Harnesses
   # Problems to test: 3
   ############################################################

   ============================================================
   Testing Socratic Method with problem #1
   Problem: How do I solve 2x + 5 = 13?
   ============================================================

   [Turn 1] Student: How do I solve 2x + 5 = 13?
   [Turn 1] Socratic Method: Good question! What operation...

   [Turn 2] Student: I'm not sure where to start
   [Turn 2] Socratic Method: Let's think about this...
   ```

4. **Wait for completion** (~3-4 minutes for 3 problems × 5 harnesses)

5. **See Summary:**
   ```
   ## Summary Statistics by Harness:

   ### Socratic Method
     Success Rate: 100.0%
     Avg Interactions: 4.0
     Avg Hints Given: 3.0
     Avg Questions Asked: 6.7
     Avg Concepts Explained: 2.3
     Avg Understanding: 0.83

   ### Direct Instruction
     Success Rate: 100.0%
     Avg Interactions: 3.0
     Avg Hints Given: 1.0
     Avg Questions Asked: 2.0
     Avg Concepts Explained: 4.7
     Avg Understanding: 0.77
   ```

### Part B: Results Dashboard (5 minutes)

1. **Launch Dashboard:**
   ```bash
   python src/dashboard.py
   ```

2. **Opens at** http://127.0.0.1:8050

3. **Explore Tabs:**

   **Tab 1: Performance Comparison**
   - 6 charts comparing metrics
   - Bar charts for each dimension
   - Hover for exact values

   **Tab 2: Radar View**
   - Multi-dimensional radar chart
   - Each harness has distinct shape
   - Circular = well-rounded, Spiky = specialized

   **Tab 3: Problem Analysis**
   - Performance by problem ID
   - Grouped bar chart
   - Shows which harness works best for which problem

   **Tab 4: Interaction Timeline**
   - Scatter plot over time
   - Bubble size = response length
   - Color = harness type

   **Tab 5: Raw Data**
   - Full data tables
   - Sortable columns
   - Export-ready

4. **Key Insights to Point Out:**
   - Socratic has highest questions asked
   - Direct has most concepts explained
   - Step-by-Step has consistent interaction count
   - Discovery has varied response lengths
   - Adaptive adjusts based on problem

---

## 📊 Demo 4: Interactive Analysis (5 minutes)

### Part A: Python REPL Analysis (3 minutes)

```bash
python -i analysis_notebook.py
```

**Output:**
```
====================================
Data loaded successfully!
====================================
Sessions: 15 rows
Interactions: 60 rows
Harnesses: ['Socratic Method', 'Direct Instruction', ...]

Quick Examples: [shows usage examples]
```

**Try These Commands:**

1. **Compare harnesses on understanding:**
   ```python
   >>> compare_harnesses('estimated_understanding')
   ```
   Output:
   ```
                        mean       std  count
   harness_name
   Socratic Method     0.833333  0.057735     3
   Adaptive            0.766667  0.057735     3
   Direct Instruction  0.766667  0.057735     3
   ```

2. **Get detailed profile:**
   ```python
   >>> harness_profile('Socratic Method')
   ```
   Output:
   ```python
   {
       'sessions': 3,
       'avg_understanding': 0.833,
       'success_rate': 1.0,
       'avg_interactions': 4.0,
       'avg_hints': 3.0,
       'avg_questions': 6.67,
       'avg_concepts': 2.33
   }
   ```

3. **Problem analysis:**
   ```python
   >>> problem_analysis()
   ```
   Shows performance metrics by problem ID.

4. **Best harness for problem:**
   ```python
   >>> best_for_problem(1)
   ```
   Output:
   ```
   Socratic Method      0.90
   Step-by-Step         0.85
   Adaptive             0.80
   ```

### Part B: Custom Queries (2 minutes)

**Correlation analysis:**
```python
>>> df_sessions[['total_hints', 'estimated_understanding']].corr()
```

**Filter by difficulty:**
```python
>>> df_sessions[df_sessions['problem_id'] <= 2]  # Easy problems
```

**Plot custom chart:**
```python
>>> import plotly.express as px
>>> fig = px.scatter(df_sessions, x='total_hints', y='estimated_understanding', 
...                  color='harness_name', title='Hints vs Understanding')
>>> fig.show()
```

---

## 🎨 Demo 5: Custom Scenarios (5 minutes)

### Scenario A: Testing Word Problems

1. **In Web UI:**
   ```
   Question: Sarah has 12 apples. She gives 5 to her friend. 
             How many does she have left?
   Correct Answer: 7
   Student's Answer: 6
   Attempt: 1
   ```

2. **Compare all harnesses** - see how each approaches word problems

### Scenario B: Testing with AI Mode (if API key available)

1. **Add API key:**
   ```bash
   echo "ANTHROPIC_API_KEY=sk-ant-your-key" > .env
   ```

2. **Restart server**

3. **In Web UI:**
   - Select "AI (Harnesses)" mode
   - Test same problem
   - **Notice:** Responses are now dynamic and contextual!
   - Each test generates unique coaching based on context

4. **Compare Static vs AI:**
   - Test once in Static mode
   - Test same problem in AI mode
   - See how AI provides more nuanced, context-aware coaching

### Scenario C: Conversation History

1. **Reset harness:**
   ```bash
   curl -X POST http://localhost:8000/api/reset/socratic
   ```

2. **Test sequential problems** to see conversation build-up (AI mode only)

### Scenario D: Edge Cases

**Very wrong answer:**
```
Question: What is 2 + 2?
Student's Answer: 10
```

**Complex problem:**
```
Question: Solve x² + 5x + 6 = 0
Student's Answer: I don't know
```

**Correct on first try:**
```
Question: What is 1 + 1?
Student's Answer: 2
Check: ✓ Answer is correct
```

---

## 📈 Demo Summary Checklist

Use this to ensure you've covered all features:

- [ ] Web UI loaded at localhost:8000
- [ ] Tested single harness
- [ ] Compared all harnesses side-by-side
- [ ] Tried different scenarios (wrong, correct, multiple attempts)
- [ ] Explored API documentation
- [ ] Ran automated experiment
- [ ] Viewed results dashboard (all 5 tabs)
- [ ] Used interactive Python analysis
- [ ] Tested both Static and AI modes (if API key available)
- [ ] Showed customization possibilities

---

## 🎤 Presentation Script

**Intro (1 min):**
> "This is an AI tutoring evaluation system that compares 5 different teaching strategies. Instead of hardcoded responses, we use AI with different pedagogical approaches - Socratic questioning, direct instruction, step-by-step guidance, discovery learning, and adaptive teaching."

**Web UI Demo (3 min):**
> "Let's see it in action. [Open localhost:8000] Here's a student who answered 94 instead of 96 for 12 times 8. [Click Test] The Socratic method asks guiding questions. [Click Direct] Direct instruction explains clearly. [Click Compare All] We can test all 5 strategies at once and see how differently they approach the same problem."

**Evaluation Demo (2 min):**
> "For research, we can run automated experiments. [Run experiment] It tests each harness on multiple problems, tracking metrics like hints given, questions asked, and understanding achieved. [Show dashboard] Here's the results - Socratic asks more questions but achieves higher understanding, while Direct is faster but less deep."

**Wrap-up (1 min):**
> "This system lets us scientifically compare teaching approaches, integrate AI tutoring into existing apps, and continuously improve based on data. It's open source and ready to use."

---

## 🐛 Common Demo Issues & Fixes

**Issue:** Web UI shows "Backend offline"
**Fix:** 
```bash
cd backend && python server.py
```

**Issue:** "No results" in dashboard
**Fix:**
```bash
python run_experiment.py 3  # Generate data first
```

**Issue:** Port 8000 already in use
**Fix:**
```bash
lsof -i :8000  # Find process
kill -9 <PID>  # Kill it
```

**Issue:** AI mode not working
**Fix:** Add `ANTHROPIC_API_KEY` to `.env` file

---

## 💡 Demo Tips

1. **Start simple** - Use Static mode first (no API key needed)
2. **Show contrast** - Always compare at least 2 harnesses
3. **Use real examples** - Math problems people can relate to
4. **Highlight metrics** - Point out specific numbers in results
5. **Keep browser tab ready** - Pre-load localhost:8000 before demo
6. **Have backup** - Screenshots in case of technical issues
7. **Practice timing** - Full demo is ~30 min, have 15 min short version ready

---

## 📸 Screenshot Locations for Documentation

If creating slides or documentation, capture:
1. Web UI homepage (localhost:8000)
2. Single harness response
3. All harnesses comparison view
4. API docs (localhost:8000/docs)
5. Dashboard radar chart
6. Dashboard comparison charts
7. Terminal showing experiment run
8. Python REPL with results

---

**Ready to demo!** 🎉

For questions during demo, refer to:
- Technical details: [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)
- Integration: [REACT_INTEGRATION.md](REACT_INTEGRATION.md)
- Analysis: [ANALYSIS_GUIDE.md](ANALYSIS_GUIDE.md)
