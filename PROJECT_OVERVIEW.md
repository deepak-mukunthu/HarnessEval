# MathTutor Harness Evaluation - Project Overview

## What This Project Does

This project evaluates 5 different AI tutoring approaches (harnesses) to determine which teaching strategies are most effective for math education. Each harness uses the Claude API with different system prompts and teaching philosophies.

## The 5 Harnesses

| Harness | Teaching Philosophy | Key Characteristic | Temperature |
|---------|-------------------|-------------------|------------|
| **Socratic Method** | Guide through questions | Promotes discovery and critical thinking | 0.8 |
| **Direct Instruction** | Clear explanations | Efficient knowledge transfer | 0.4 |
| **Step-by-Step** | Sequential guidance | Breaks complexity into manageable chunks | 0.6 |
| **Discovery Learning** | Pattern exploration | Builds mathematical intuition | 0.9 |
| **Adaptive** | Personalized approach | Adjusts to student level | 0.7 |

## Project Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Run Experiment                        │
│  (run_experiment.py)                                    │
└────────────┬────────────────────────────────────────────┘
             │
             ├─► Load Test Problems (data/test_problems.json)
             │
             ├─► For each problem × harness combination:
             │   │
             │   ├─► Initialize Harness
             │   │   └─► MathTutor (math_tutor.py)
             │   │       └─► Claude API
             │   │
             │   ├─► Simulate Student Interaction
             │   │   └─► Multiple turns of Q&A
             │   │
             │   └─► Record Metrics (evaluator.py)
             │       ├─► Interaction level
             │       └─► Session level
             │
             └─► Save Results (data/results/)
                 ├─► *_interactions.json
                 └─► *_sessions.json

┌─────────────────────────────────────────────────────────┐
│                   Dashboard                              │
│  (src/dashboard.py)                                     │
└────────────┬────────────────────────────────────────────┘
             │
             ├─► Load Results
             │
             ├─► Generate Visualizations
             │   ├─► Performance Comparison
             │   ├─► Radar Chart
             │   ├─► Problem Analysis
             │   └─► Interaction Timeline
             │
             └─► Serve Web Dashboard (Dash)
                 └─► http://127.0.0.1:8050/
```

## Key Components

### 1. MathTutor Base Class (`src/math_tutor.py`)
- Manages conversation with Claude API
- Handles message history
- Extracts basic metrics from responses

### 2. Harness Implementations (`src/harnesses/`)
Each harness:
- Defines a unique `SYSTEM_PROMPT`
- Sets appropriate `temperature`
- Implements `teach()` method
- Can be reset between problems

### 3. Evaluator (`src/evaluator.py`)
Tracks two levels of metrics:

**Interaction Metrics** (per message):
- Response length
- Hints given
- Questions asked
- Concepts explained

**Session Metrics** (per problem attempt):
- Total interactions
- Time to completion
- Success rate
- Estimated understanding

### 4. Dashboard (`src/dashboard.py`)
Interactive Plotly Dash application with:
- Summary statistics cards
- Multiple visualization tabs
- Raw data tables
- Real-time filtering

## Evaluation Dimensions

The experiment evaluates harnesses across multiple dimensions:

1. **Effectiveness**: Does the student reach understanding?
2. **Efficiency**: How quickly is understanding achieved?
3. **Engagement**: How interactive is the learning?
4. **Depth**: How much conceptual explanation occurs?
5. **Scaffolding**: How much support is provided?
6. **Consistency**: Performance across different problems?

## Workflow

### Development Workflow
1. Design harness → Edit prompt in `src/harnesses/`
2. Test on sample → `python run_experiment.py 1`
3. Review results → `python src/dashboard.py`
4. Iterate on prompt
5. Full evaluation → `python run_experiment.py 10`

### Analysis Workflow
1. Run experiment → Generates JSON data
2. Launch dashboard → Visual exploration
3. Deep dive → Use `analysis_notebook.py`
4. Statistical testing → Custom analysis
5. Report findings → Use ANALYSIS_GUIDE.md

## Design Decisions

### Why These 5 Harnesses?
- **Coverage**: Span major teaching philosophies
- **Contrast**: Distinct enough to show differences
- **Relevance**: Based on established pedagogical theories
- **Practicality**: Implementable via prompt engineering

### Why Claude API?
- High-quality reasoning for educational content
- Good at following system prompt instructions
- Supports various temperature settings
- Suitable for this style of prompt-based differentiation

### Why Simulation vs. Real Students?
- **Initial Phase**: Simulation allows rapid iteration
- **Cost Effective**: Test many variations quickly
- **Reproducible**: Same "student" behavior across tests
- **Scalable**: Easy to test on many problems
- **Next Step**: After validation, move to real user testing

### Limitations
1. **Simulated Students**: Not real student behavior
2. **Limited Problems**: 10 test problems
3. **No Retention Testing**: Only immediate understanding
4. **Single Turn Context**: Each problem is independent
5. **Manual Scoring**: Understanding estimated, not measured

## Extensibility

### Adding a New Harness
```python
# src/harnesses/your_harness.py
from ..math_tutor import MathTutor, TutorResponse

class YourHarness:
    SYSTEM_PROMPT = """Your teaching philosophy..."""

    def __init__(self, api_key: str = None):
        self.tutor = MathTutor(api_key)
        self.name = "Your Harness Name"

    def teach(self, student_message: str) -> TutorResponse:
        return self.tutor.get_response(
            student_message=student_message,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.7
        )

    def reset(self):
        self.tutor.reset()
```

### Adding New Metrics
```python
# In src/evaluator.py
def _count_your_metric(self, text: str) -> int:
    # Your custom metric logic
    return score

# Add to InteractionMetrics dataclass
@dataclass
class InteractionMetrics:
    ...
    your_new_metric: int
```

### Adding New Visualizations
```python
# In src/dashboard.py
def create_your_chart(df_sessions):
    fig = px.bar(...)  # Your plotly figure
    return fig

# Add tab in app.layout
dcc.Tab(label='Your View', children=[
    dcc.Graph(figure=create_your_chart(df_sessions))
])
```

## Future Enhancements

### Short Term
- [ ] Add confidence intervals to metrics
- [ ] Implement A/B testing framework
- [ ] Add problem difficulty scoring
- [ ] Export results to CSV/Excel
- [ ] Add cost tracking (API token usage)

### Medium Term
- [ ] Real student testing interface
- [ ] Multi-session learning tracking
- [ ] Adaptive problem selection
- [ ] Student persona simulation agents
- [ ] Hybrid harness approaches

### Long Term
- [ ] Integration with learning management systems
- [ ] Retention and transfer testing
- [ ] Multi-subject expansion beyond math
- [ ] Teacher feedback loop
- [ ] Production deployment as tutoring service

## Related Research

This project draws inspiration from:
- Socratic teaching methods (Plato, 399 BC)
- Direct Instruction (Engelmann, 1960s)
- Discovery Learning (Bruner, 1961)
- Adaptive Learning (Bloom's 2-Sigma, 1984)
- AI Tutoring Systems (VanLehn, 2011)

## Contributing

Ideas for contributions:
1. New harness implementations
2. More test problems (diverse difficulty/topics)
3. Better student simulation
4. Enhanced evaluation metrics
5. Real classroom studies

## License

This is a personal project for educational experimentation.
Feel free to adapt for your own research or teaching.

## Questions to Explore

1. Does Socratic method really produce deeper understanding?
2. Is there a trade-off between efficiency and depth?
3. Which harness works best for different problem types?
4. Can we predict which student benefits from which harness?
5. Do hybrid approaches outperform pure strategies?
6. How much does temperature setting matter?
7. Is adaptive really better than fixed approaches?

Run the experiments and find out! 🚀
