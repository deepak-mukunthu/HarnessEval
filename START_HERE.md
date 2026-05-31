# 🚀 START HERE

Welcome to the MathTutor Harness Evaluation Project!

## What You Have

A complete experimental framework for evaluating **5 different AI tutoring strategies** using Claude AI. This project helps you discover which teaching approaches work best for math education.

## Quick Start (5 minutes)

### Option 1: Automated Setup
```bash
./GET_STARTED.sh
```

### Option 2: Manual Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up your API key
cp .env.example .env
# Edit .env and add: ANTHROPIC_API_KEY=your_key_here

# 3. Run experiment
python run_experiment.py

# 4. View results
python src/dashboard.py
```

## The 5 Harnesses You'll Test

1. **Socratic Method** 🤔 - Guides through questions
2. **Direct Instruction** 📚 - Clear explanations with examples
3. **Step-by-Step** 👣 - Breaks problems into manageable chunks
4. **Discovery Learning** 🔍 - Encourages pattern exploration
5. **Adaptive** 🎯 - Adjusts to student level

## Project Structure

```
HarnessEval/
├── 📄 START_HERE.md          ← You are here!
├── 📄 README.md              ← Project overview
├── 📄 QUICKSTART.md          ← Detailed setup guide
├── 📄 ANALYSIS_GUIDE.md      ← How to interpret results
├── 📄 PROJECT_OVERVIEW.md    ← Technical deep dive
│
├── 🐍 run_experiment.py      ← Run experiments
├── 🐍 analysis_notebook.py   ← Interactive analysis
│
├── 📁 src/
│   ├── math_tutor.py         ← Base tutor implementation
│   ├── evaluator.py          ← Metrics & evaluation
│   ├── dashboard.py          ← Results visualization
│   └── harnesses/            ← 5 teaching strategies
│       ├── socratic.py
│       ├── direct.py
│       ├── step_by_step.py
│       ├── discovery.py
│       └── adaptive.py
│
├── 📁 data/
│   ├── test_problems.json    ← 10 math problems
│   └── results/              ← Experiment results (auto-generated)
│
└── 📁 tests/
    └── test_harnesses.py     ← Unit tests
```

## Usage Examples

### Basic Experiment (3 problems)
```bash
python run_experiment.py
```

### Full Experiment (all 10 problems)
```bash
python run_experiment.py 10
```

### Launch Dashboard
```bash
python src/dashboard.py
# Open browser to: http://127.0.0.1:8050/
```

### Interactive Analysis
```bash
python -i analysis_notebook.py
# Then try:
>>> compare_harnesses('estimated_understanding')
>>> harness_profile('Socratic Method')
>>> problem_analysis()
```

## What Gets Evaluated

Each harness is tested on:
- ✅ **Effectiveness**: Does student reach understanding?
- ⚡ **Efficiency**: How quickly?
- 💬 **Engagement**: How interactive?
- 🧠 **Depth**: How much conceptual teaching?
- 🤝 **Support**: How much scaffolding?
- 📊 **Consistency**: Performance across problems?

## Dashboard Views

The dashboard provides 5 views:

1. **Performance Comparison** - Bar charts of key metrics
2. **Radar View** - Multi-dimensional comparison
3. **Problem Analysis** - Performance by problem type
4. **Interaction Timeline** - Temporal patterns
5. **Raw Data** - Full data tables

## Key Questions Answered

- Which harness produces the deepest understanding?
- Which is most efficient for time-constrained learning?
- Which works best for different problem types?
- What's the trade-off between speed and depth?
- Which approach engages students most?

## Sample Output

After running the experiment, you'll see:

```
### Socratic Method
  Success Rate: 85.0%
  Avg Interactions: 4.2
  Avg Hints Given: 3.1
  Avg Questions Asked: 6.5
  Avg Concepts Explained: 2.8
  Avg Understanding: 0.82

### Direct Instruction
  Success Rate: 90.0%
  Avg Interactions: 2.8
  Avg Hints Given: 1.2
  Avg Questions Asked: 2.1
  Avg Concepts Explained: 4.5
  Avg Understanding: 0.78
...
```

## Customization

### Add New Problems
Edit [data/test_problems.json](data/test_problems.json):
```json
{
  "id": 11,
  "problem": "Your math problem",
  "correct_answer": "Answer",
  "concepts": ["algebra"],
  "follow_up": "Follow-up question"
}
```

### Create New Harness
Copy any harness from `src/harnesses/`, modify the `SYSTEM_PROMPT`, and add to the experiment runner.

### Adjust Metrics
Edit `src/evaluator.py` to add custom evaluation metrics.

## Cost Estimate

Using Claude Sonnet 4.6:
- **Quick test** (3 problems): ~$0.10-0.20
- **Full test** (10 problems): ~$0.30-0.50
- Per problem per harness: ~$0.01-0.02

## Documentation Map

Start with the guide that matches your goal:

| Your Goal | Read This |
|-----------|-----------|
| Just get started | [QUICKSTART.md](QUICKSTART.md) |
| Understand results | [ANALYSIS_GUIDE.md](ANALYSIS_GUIDE.md) |
| Technical details | [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) |
| General overview | [README.md](README.md) |

## Troubleshooting

### API Key Error
```bash
# Make sure .env exists and contains:
ANTHROPIC_API_KEY=sk-ant-...
```

### Import Errors
```bash
pip install -r requirements.txt --upgrade
```

### No Results in Dashboard
```bash
# Run experiment first:
python run_experiment.py
# Then check data/results/ exists and has JSON files
```

### Port Already in Use
Edit `src/dashboard.py`, line with `app.run_server`, change `port=8050` to another port.

## Next Steps

1. ✅ Run `./GET_STARTED.sh` or manual setup
2. ✅ Add your API key to `.env`
3. ✅ Run quick experiment: `python run_experiment.py`
4. ✅ Launch dashboard: `python src/dashboard.py`
5. ✅ Explore results and iterate on harness prompts
6. ✅ Read [ANALYSIS_GUIDE.md](ANALYSIS_GUIDE.md) for interpretation
7. ✅ Experiment with different prompts and strategies!

## Get Help

- Read [QUICKSTART.md](QUICKSTART.md) for detailed setup
- Check [ANALYSIS_GUIDE.md](ANALYSIS_GUIDE.md) for result interpretation
- Review [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for architecture

## Key Files to Explore

1. **Harness Prompts**: [`src/harnesses/*.py`](src/harnesses/) - See the actual teaching prompts
2. **Test Problems**: [`data/test_problems.json`](data/test_problems.json) - Math problems used
3. **Evaluator**: [`src/evaluator.py`](src/evaluator.py) - How metrics are calculated
4. **Dashboard**: [`src/dashboard.py`](src/dashboard.py) - Visualization code

## The Big Picture

```
┌───────────────┐
│ Math Problems │
└───────┬───────┘
        │
        ▼
┌───────────────────────────────────────┐
│   5 Different Teaching Harnesses      │
│  (Different prompts & strategies)     │
└───────────────┬───────────────────────┘
                │
                ▼
┌───────────────────────────────────────┐
│   Claude API (Sonnet 4.6)             │
│   Simulates tutoring sessions         │
└───────────────┬───────────────────────┘
                │
                ▼
┌───────────────────────────────────────┐
│   Evaluator                            │
│   Records: hints, questions, concepts  │
└───────────────┬───────────────────────┘
                │
                ▼
┌───────────────────────────────────────┐
│   Results Dashboard                    │
│   Compares effectiveness               │
└───────────────────────────────────────┘
```

## What Makes This Useful

✨ **Research-backed**: Based on established pedagogical theories
✨ **Practical**: Real AI tutoring strategies you can deploy
✨ **Extensible**: Easy to add new harnesses or problems
✨ **Visual**: Interactive dashboard for exploration
✨ **Complete**: Full pipeline from experiment to analysis

---

**Ready to start?** Run: `./GET_STARTED.sh` 🚀

**Questions?** Check [QUICKSTART.md](QUICKSTART.md) for more details.

**Want to dive deep?** Read [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md).

**Happy experimenting!** 🎓
