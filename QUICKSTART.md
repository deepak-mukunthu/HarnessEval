# Quick Start Guide

## Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your API key**
   ```bash
   cp .env.example .env
   # Edit .env and add your Anthropic API key
   ```

3. **Verify installation**
   ```bash
   python -m pytest tests/test_harnesses.py
   ```

## Running Experiments

### Basic Experiment (3 problems)
```bash
python run_experiment.py
```

### Extended Experiment (all 10 problems)
```bash
python run_experiment.py 10
```

### Custom Experiment
```python
from run_experiment import run_experiment
evaluator = run_experiment(num_problems=5)
```

## Viewing Results

### Launch Dashboard
```bash
python src/dashboard.py
```

Then open your browser to http://127.0.0.1:8050/

### Manual Analysis
Results are saved in `data/results/` as JSON files:
- `*_sessions.json` - Aggregate metrics per session
- `*_interactions.json` - Individual interaction details

## Understanding the Harnesses

### 1. Socratic Method
- **Strategy**: Guides through questioning
- **Best for**: Deep conceptual understanding
- **Temperature**: 0.8 (creative questioning)

### 2. Direct Instruction
- **Strategy**: Clear explanations with examples
- **Best for**: Quick knowledge transfer
- **Temperature**: 0.4 (precise, consistent)

### 3. Step-by-Step
- **Strategy**: Breaks problems into manageable steps
- **Best for**: Complex multi-step problems
- **Temperature**: 0.6 (balanced)

### 4. Discovery Learning
- **Strategy**: Pattern recognition and exploration
- **Best for**: Building intuition
- **Temperature**: 0.9 (highly exploratory)

### 5. Adaptive
- **Strategy**: Adjusts based on student performance
- **Best for**: Diverse student skill levels
- **Temperature**: 0.7 (flexible)

## Evaluation Metrics

- **Success Rate**: % of sessions where student reached answer
- **Avg Interactions**: Number of back-and-forth exchanges
- **Hints Given**: Frequency of scaffolding support
- **Questions Asked**: Socratic vs. explanatory style
- **Concepts Explained**: Depth of conceptual teaching
- **Understanding Score**: Estimated comprehension level

## Customization

### Adding New Test Problems
Edit `data/test_problems.json`:
```json
{
  "id": 11,
  "category": "your_category",
  "difficulty": "beginner|intermediate|advanced",
  "problem": "Your problem statement",
  "correct_answer": "Expected answer",
  "concepts": ["concept1", "concept2"],
  "follow_up": "Follow-up question"
}
```

### Creating a New Harness
1. Copy an existing harness from `src/harnesses/`
2. Modify the `SYSTEM_PROMPT`
3. Adjust `temperature` parameter
4. Add to `src/harnesses/__init__.py`
5. Include in `run_experiment.py`

### Modifying Evaluation Metrics
Edit `src/evaluator.py` to add custom metrics:
- `_count_hints()` - Pattern matching for hints
- `_count_concepts()` - Concept explanation detection
- `record_interaction()` - Per-message metrics
- `record_session()` - Aggregate session metrics

## Tips for Best Results

1. **API Rate Limits**: Add delays between requests if hitting limits
2. **Cost Management**: Start with fewer problems (1-3) for testing
3. **Reproducibility**: Set random seeds if needed for consistency
4. **Data Analysis**: Export results to CSV for external analysis

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
- Make sure `.env` file exists in project root
- Verify the key is correctly formatted
- Try: `export ANTHROPIC_API_KEY=your_key` before running

### Import Errors
```bash
pip install -r requirements.txt --upgrade
```

### Dashboard Won't Start
- Check port 8050 is available
- Try a different port: Edit `dashboard.py`, change `port=8050`

### No Results in Dashboard
- Run `run_experiment.py` first to generate data
- Check `data/results/` contains JSON files
