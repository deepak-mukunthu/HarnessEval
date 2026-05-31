# 🌐 Web Interfaces Guide

You have **3 web interfaces** to visualize and test the harnesses!

## 1. ✨ Interactive Harness Tester (Recommended to Start!)

**Best for**: Real-time testing without generating data first.

### Launch:
```bash
# Terminal 1: Start backend
cd backend
python server.py

# Terminal 2: Open web interface
open frontend/index.html
# Or just double-click frontend/index.html in Finder
```

**URL**: Opens directly in browser (file:// protocol)

**Features**:
- Test single harnesses
- Compare all 5 side-by-side
- Real-time coaching responses
- No data generation needed!
- Beautiful modern UI

**Use this to**: Test different harnesses instantly, see how each one responds to the same problem.

---

## 2. 🔧 API Documentation (Swagger UI)

**Best for**: Technical API testing, understanding endpoints.

### Launch:
```bash
cd backend
python server.py
```

**URL**: http://localhost:8000/docs

**Features**:
- Interactive API testing
- Try all endpoints
- See request/response formats
- Built-in by FastAPI

**Use this to**: Understand the API, test endpoints programmatically.

---

## 3. 📊 Results Dashboard (Dash/Plotly)

**Best for**: Analyzing experiment results with charts.

### Launch:
```bash
# FIRST: Generate experiment data (required!)
python run_experiment.py 3

# THEN: Launch dashboard
python src/dashboard.py
```

**URL**: http://127.0.0.1:8050/

**Features**:
- Performance comparison charts
- Radar charts
- Problem analysis
- Interaction timelines
- Raw data tables

**Use this to**: Analyze and visualize experiment results.

---

## Troubleshooting

### "http://127.0.0.1:8050/ is not accessible"

**Cause**: No experiment data generated yet.

**Fix**:
```bash
# Generate data first
python run_experiment.py 3

# Then launch dashboard
python src/dashboard.py
```

### "Backend offline" in Harness Tester

**Cause**: Backend API not running.

**Fix**:
```bash
cd backend
python server.py
```

### Port 8050 already in use

**Fix**: Edit `src/dashboard.py`, change line at the bottom:
```python
app.run_server(debug=True, port=8051)  # Changed from 8050
```

### Can't install dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install
pip install -r requirements.txt
cd backend
pip install -r requirements.txt
```

---

## Quick Comparison

| Interface | Requires Data? | Requires Backend? | Best Use Case |
|-----------|---------------|-------------------|---------------|
| **Harness Tester** | ❌ No | ✅ Yes | Real-time testing |
| **API Docs** | ❌ No | ✅ Yes | API exploration |
| **Results Dashboard** | ✅ Yes | ❌ No | Data visualization |

---

## Recommended Workflow

### First Time (5 minutes):
```bash
# 1. Start backend
cd backend
pip install -r requirements.txt
python server.py

# 2. Open Harness Tester
open frontend/index.html

# 3. Test different harnesses!
```

### For Research/Analysis (15 minutes):
```bash
# 1. Run experiment
pip install -r requirements.txt
python run_experiment.py 3

# 2. Launch dashboard
python src/dashboard.py

# 3. View results at http://127.0.0.1:8050/
```

### For React Integration:
See [REACT_INTEGRATION.md](REACT_INTEGRATION.md)

---

## Screenshots & Examples

### Harness Tester Interface
- Left panel: Input form (question, answer, attempt)
- Right panel: Harness selection (click to choose)
- Bottom: Response display or comparison grid

### API Docs Interface
- List of all endpoints
- "Try it out" buttons
- Request/response examples
- Schema definitions

### Results Dashboard
- Tab 1: Performance comparison bars
- Tab 2: Radar charts
- Tab 3: Problem analysis
- Tab 4: Interaction timeline
- Tab 5: Raw data tables

---

## Next Steps

**Start here**: Open `frontend/index.html` after starting the backend!

This is the fastest way to see the harnesses in action.
