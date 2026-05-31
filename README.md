# MathTutor Harness Evaluation Project

This project evaluates 5 different harness strategies for a MathTutor AI system.

## Project Structure

```
.
├── src/
│   ├── math_tutor.py          # Base MathTutor implementation
│   ├── harnesses/              # 5 different harness strategies
│   │   ├── socratic.py         # Socratic method
│   │   ├── direct.py           # Direct instruction
│   │   ├── step_by_step.py     # Guided steps
│   │   ├── discovery.py        # Discovery-based learning
│   │   └── adaptive.py         # Adaptive difficulty
│   ├── evaluator.py            # Evaluation framework
│   └── dashboard.py            # Results visualization
├── data/
│   ├── test_problems.json      # Test problem set
│   └── results/                # Experiment results
├── tests/
│   └── test_harnesses.py       # Unit tests
├── requirements.txt
└── run_experiment.py           # Main experiment runner
```

## Harness Strategies

1. **Socratic Method**: Guides through questioning
2. **Direct Instruction**: Clear explanations with examples
3. **Step-by-Step**: Breaks down problems into manageable steps
4. **Discovery Learning**: Encourages exploration and pattern recognition
5. **Adaptive**: Adjusts difficulty based on student performance

## Evaluation Metrics

- Student understanding (comprehension score)
- Time to solution
- Number of hints needed
- Engagement level
- Concept retention

## Running Experiments

```bash
python run_experiment.py
python src/dashboard.py
```
