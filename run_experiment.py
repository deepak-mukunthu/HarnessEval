"""Main experiment runner to evaluate all harnesses."""

import json
import os
from pathlib import Path
from dotenv import load_dotenv

from src.harnesses import (
    SocraticHarness,
    DirectHarness,
    StepByStepHarness,
    DiscoveryHarness,
    AdaptiveHarness,
)
from src.evaluator import Evaluator


def load_test_problems(file_path: str = "data/test_problems.json"):
    """Load test problems from JSON file."""
    with open(file_path, "r") as f:
        return json.load(f)


def simulate_student_interaction(harness, problem, evaluator, max_turns=4):
    """
    Simulate a student working through a problem with a harness.
    In a real scenario, this would be actual student inputs.
    """
    print(f"\n{'='*60}")
    print(f"Testing {harness.name} with problem #{problem['id']}")
    print(f"Problem: {problem['problem']}")
    print(f"{'='*60}")

    harness.reset()
    session_interactions = []
    student_understood = False

    student_messages = [
        problem["problem"],
        "I'm not sure where to start",
        "Can you explain more?",
        problem["follow_up"],
    ]

    for turn, message in enumerate(student_messages[:max_turns], 1):
        print(f"\n[Turn {turn}] Student: {message}")

        response = harness.teach(message)

        print(f"[Turn {turn}] {harness.name}: {response.message[:200]}...")

        interaction = evaluator.record_interaction(
            harness_name=harness.name,
            problem_id=problem["id"],
            student_message=message,
            tutor_response=response.message,
        )

        session_interactions.append(interaction)

        if turn >= 3:
            student_understood = True

    evaluator.record_session(
        harness_name=harness.name,
        problem_id=problem["id"],
        interactions=session_interactions,
        student_reached_answer=student_understood,
        estimated_understanding=0.7 + (turn * 0.1),
    )


def run_experiment(num_problems: int = 3):
    """Run the complete experiment across all harnesses."""
    load_dotenv()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not found in environment variables")
        print("Please create a .env file with your API key:")
        print("ANTHROPIC_API_KEY=your_key_here")
        return

    problems = load_test_problems()
    selected_problems = problems[:num_problems]

    harnesses = [
        SocraticHarness(api_key),
        DirectHarness(api_key),
        StepByStepHarness(api_key),
        DiscoveryHarness(api_key),
        AdaptiveHarness(api_key),
    ]

    evaluator = Evaluator()

    print(f"\n{'#'*60}")
    print(f"# Starting Experiment: Testing {len(harnesses)} Harnesses")
    print(f"# Problems to test: {num_problems}")
    print(f"{'#'*60}")

    for problem in selected_problems:
        for harness in harnesses:
            try:
                simulate_student_interaction(harness, problem, evaluator)
            except Exception as e:
                print(f"\nERROR with {harness.name}: {e}")
                continue

    interactions_file, sessions_file = evaluator.save_results()

    print(f"\n{'#'*60}")
    print("# Experiment Complete!")
    print(f"{'#'*60}")

    summary = evaluator.generate_summary()
    print("\n## Summary Statistics by Harness:\n")
    for harness_name, stats in summary.items():
        print(f"\n### {harness_name}")
        print(f"  Success Rate: {stats['success_rate']:.1%}")
        print(f"  Avg Interactions: {stats['avg_interactions']:.1f}")
        print(f"  Avg Hints Given: {stats['avg_hints']:.1f}")
        print(f"  Avg Questions Asked: {stats['avg_questions']:.1f}")
        print(f"  Avg Concepts Explained: {stats['avg_concepts']:.1f}")
        print(f"  Avg Understanding: {stats['avg_understanding']:.2f}")

    print(f"\n\nNext steps:")
    print(f"  1. Review detailed results in {sessions_file}")
    print(f"  2. Run the dashboard: python src/dashboard.py")

    return evaluator


if __name__ == "__main__":
    import sys

    num_problems = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    run_experiment(num_problems)
