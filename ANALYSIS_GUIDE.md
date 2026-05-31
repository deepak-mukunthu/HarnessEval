# Analysis Guide

## Interpreting Results

### Key Questions to Answer

1. **Which harness is most effective overall?**
   - Look at success rate and understanding scores
   - Consider the balance of efficiency vs. depth

2. **Which harness fits different learning styles?**
   - High questions → Socratic, good for engaged learners
   - High concepts → Direct/Step-by-Step, good for knowledge acquisition
   - High hints → Discovery/Adaptive, good for exploratory learners

3. **Which harness is most efficient?**
   - Fewest interactions to reach understanding
   - Balance response length vs. effectiveness

4. **Which harness scales best?**
   - Performance across different problem difficulties
   - Consistency across problem types

### Metrics Deep Dive

#### Success Rate
- **High (>80%)**: Harness reliably guides students to answers
- **Medium (60-80%)**: Works well for some problem types
- **Low (<60%)**: May need prompt refinement

#### Avg Interactions
- **Low (1-2)**: Direct, efficient (but may sacrifice depth)
- **Medium (3-4)**: Balanced approach
- **High (5+)**: Deep engagement (but may lose student attention)

#### Hints Given
- **High**: More scaffolding, good for struggling students
- **Low**: More independence, good for advanced students

#### Questions Asked
- **High**: Socratic style, promotes critical thinking
- **Low**: Explanatory style, more direct knowledge transfer

#### Concepts Explained
- **High**: Deep conceptual teaching
- **Low**: More procedural/practical focus

### Dashboard Views

#### 1. Performance Comparison Tab
- **Purpose**: Compare raw metrics across harnesses
- **Look for**: Clear winners in specific metrics
- **Insight**: No single harness dominates all metrics

#### 2. Radar View Tab
- **Purpose**: Holistic multi-dimensional comparison
- **Look for**: Shape patterns (balanced vs. specialized)
- **Insight**: 
  - Circular shape = well-rounded
  - Spiky shape = specialized strengths

#### 3. Problem Analysis Tab
- **Purpose**: Performance by problem difficulty
- **Look for**: Which harness handles which problems best
- **Insight**: Some harnesses may excel at certain problem types

#### 4. Interaction Timeline Tab
- **Purpose**: Temporal patterns and response sizes
- **Look for**: 
  - Clustering = batch processing
  - Large bubbles = verbose responses
- **Insight**: Response length vs. effectiveness trade-off

## Expected Findings

Based on the harness designs, you might expect:

### Socratic Method
- **Strengths**: Highest engagement, develops critical thinking
- **Weaknesses**: May be slower, requires active student participation
- **Best for**: Conceptual understanding, engaged learners

### Direct Instruction
- **Strengths**: Fast, clear, efficient knowledge transfer
- **Weaknesses**: Lower engagement, may not develop deep understanding
- **Best for**: Factual learning, time-constrained scenarios

### Step-by-Step
- **Strengths**: Systematic, builds confidence, clear progress
- **Weaknesses**: May be rigid, doesn't adapt to student needs
- **Best for**: Complex multi-step problems, beginners

### Discovery Learning
- **Strengths**: Builds intuition, memorable insights, pattern recognition
- **Weaknesses**: Can be frustrating, may miss key concepts
- **Best for**: Mathematical maturity, creative problem solvers

### Adaptive
- **Strengths**: Personalized, flexible, meets students where they are
- **Weaknesses**: May be inconsistent, requires good assessment
- **Best for**: Diverse student populations, varying skill levels

## Hypothesis Testing

### Hypothesis 1: Socratic method produces highest understanding
**Test**: Compare `estimated_understanding` scores
**Expected**: Socratic > others due to deep engagement

### Hypothesis 2: Direct instruction is most efficient
**Test**: Compare `total_interactions` and `avg_time`
**Expected**: Direct has fewest interactions

### Hypothesis 3: Adaptive performs consistently across problems
**Test**: Calculate variance in performance across problem IDs
**Expected**: Adaptive has lowest variance

### Hypothesis 4: Discovery learning generates most "aha" moments
**Test**: Qualitative analysis of response content
**Expected**: More insight-oriented language

## Advanced Analysis

### Statistical Significance
```python
from scipy import stats

# Compare two harnesses on understanding
harness1_scores = df_sessions[df_sessions['harness_name'] == 'Socratic Method']['estimated_understanding']
harness2_scores = df_sessions[df_sessions['harness_name'] == 'Direct Instruction']['estimated_understanding']

t_stat, p_value = stats.ttest_ind(harness1_scores, harness2_scores)
print(f"p-value: {p_value}")
# p < 0.05 means statistically significant difference
```

### Correlation Analysis
```python
import pandas as pd

# Are hints correlated with understanding?
correlation = df_sessions[['total_hints', 'estimated_understanding']].corr()
print(correlation)
```

### Problem Type Analysis
```python
# Load problems
with open('data/test_problems.json') as f:
    problems = json.load(f)

# Merge with results
df_sessions['category'] = df_sessions['problem_id'].map(
    {p['id']: p['category'] for p in problems}
)

# Group by category and harness
category_performance = df_sessions.groupby(
    ['category', 'harness_name']
)['estimated_understanding'].mean()
```

## Recommendations Format

After analysis, structure recommendations as:

```
## Executive Summary
[1-2 sentences on overall findings]

## Recommendations

### For Quick Knowledge Transfer
Recommended: [Harness Name]
Why: [Evidence from metrics]
When to use: [Scenarios]

### For Deep Understanding
Recommended: [Harness Name]
Why: [Evidence from metrics]
When to use: [Scenarios]

### For Mixed Ability Groups
Recommended: [Harness Name]
Why: [Evidence from metrics]
When to use: [Scenarios]

## Trade-offs
[Key trade-offs between approaches]

## Future Experiments
[Ideas for improving harnesses or evaluation]
```

## Sharing Results

### Export for Presentation
```python
# In dashboard.py or Jupyter notebook
import plotly.io as pio

fig = create_comparison_chart(df_sessions)
pio.write_image(fig, 'comparison_chart.png')
pio.write_html(fig, 'comparison_chart.html')
```

### Generate Report
```python
summary = evaluator.generate_summary()

with open('experiment_report.md', 'w') as f:
    f.write("# Experiment Report\n\n")
    for harness, stats in summary.items():
        f.write(f"## {harness}\n")
        for metric, value in stats.items():
            f.write(f"- {metric}: {value}\n")
        f.write("\n")
```

## Next Steps

1. **Refine Prompts**: Based on weaknesses identified
2. **Add Problem Types**: Test on more diverse problems
3. **Hybrid Approaches**: Combine strengths of multiple harnesses
4. **Student Personas**: Create realistic student simulation agents
5. **Longitudinal Study**: Track retention over multiple sessions
6. **Real User Testing**: Replace simulation with actual students
