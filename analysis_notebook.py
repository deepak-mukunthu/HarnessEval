"""
Interactive Analysis Notebook (run with: python -i analysis_notebook.py)

This provides a Python REPL environment pre-loaded with your experiment results.
Useful for ad-hoc queries and custom visualizations.
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go


# Load latest results
def load_latest():
    results_dir = Path("data/results")

    session_files = sorted(results_dir.glob("*_sessions.json"))
    interaction_files = sorted(results_dir.glob("*_interactions.json"))

    if not session_files:
        print("No results found. Run 'python run_experiment.py' first.")
        return None, None

    with open(session_files[-1]) as f:
        sessions = json.load(f)

    with open(interaction_files[-1]) as f:
        interactions = json.load(f)

    print(f"Loaded: {session_files[-1].name}")
    return pd.DataFrame(sessions), pd.DataFrame(interactions)


# Load data
df_sessions, df_interactions = load_latest()

if df_sessions is not None:
    print(f"\n{'='*60}")
    print(f"Data loaded successfully!")
    print(f"{'='*60}")
    print(f"Sessions: {len(df_sessions)} rows")
    print(f"Interactions: {len(df_interactions)} rows")
    print(f"Harnesses: {df_sessions['harness_name'].unique().tolist()}")
    print(f"\nColumns available in df_sessions:")
    print(f"  {df_sessions.columns.tolist()}")
    print(f"\n{'='*60}")
    print(f"Quick Examples:")
    print(f"{'='*60}")
    print("""
# View summary by harness
df_sessions.groupby('harness_name').agg({
    'estimated_understanding': 'mean',
    'total_hints': 'sum',
    'student_reached_answer': 'mean'
})

# Best performing harness by understanding
df_sessions.groupby('harness_name')['estimated_understanding'].mean().sort_values(ascending=False)

# Most efficient harness (fewest interactions)
df_sessions.groupby('harness_name')['total_interactions'].mean().sort_values()

# Success rate by problem
df_sessions.groupby('problem_id')['student_reached_answer'].mean()

# Correlation between hints and understanding
df_sessions[['total_hints', 'estimated_understanding']].corr()

# Plot comparison
fig = px.bar(
    df_sessions.groupby('harness_name')['estimated_understanding'].mean().reset_index(),
    x='harness_name', y='estimated_understanding',
    title='Average Understanding by Harness'
)
fig.show()
    """)
    print(f"\n{'='*60}")
    print(f"Ready for analysis! Type your pandas/plotly commands.")
    print(f"{'='*60}\n")


# Helper functions
def compare_harnesses(metric='estimated_understanding'):
    """Quick comparison of harnesses on a given metric."""
    result = df_sessions.groupby('harness_name')[metric].agg(['mean', 'std', 'count'])
    return result.sort_values('mean', ascending=False)


def problem_analysis():
    """Analyze performance by problem."""
    return df_sessions.groupby('problem_id').agg({
        'estimated_understanding': 'mean',
        'total_interactions': 'mean',
        'student_reached_answer': 'mean',
        'total_hints': 'mean'
    }).round(2)


def harness_profile(harness_name):
    """Get detailed profile of a specific harness."""
    data = df_sessions[df_sessions['harness_name'] == harness_name]

    return {
        'sessions': len(data),
        'avg_understanding': data['estimated_understanding'].mean(),
        'success_rate': data['student_reached_answer'].mean(),
        'avg_interactions': data['total_interactions'].mean(),
        'avg_hints': data['total_hints'].mean(),
        'avg_questions': data['total_questions'].mean(),
        'avg_concepts': data['total_concepts'].mean(),
    }


def best_for_problem(problem_id):
    """Find which harness works best for a specific problem."""
    problem_data = df_sessions[df_sessions['problem_id'] == problem_id]
    return problem_data.groupby('harness_name')['estimated_understanding'].mean().sort_values(ascending=False)


print("Helper functions available:")
print("  - compare_harnesses(metric)")
print("  - problem_analysis()")
print("  - harness_profile(harness_name)")
print("  - best_for_problem(problem_id)")
print("\nExample: harness_profile('Socratic Method')")
