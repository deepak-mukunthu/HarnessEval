"""Evaluation framework for comparing harness effectiveness."""

import json
import time
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class InteractionMetrics:
    """Metrics for a single student-tutor interaction."""
    harness_name: str
    problem_id: int
    student_message: str
    tutor_response: str
    timestamp: float
    response_length: int
    hints_given: int
    questions_asked: int
    concepts_explained: int


@dataclass
class SessionMetrics:
    """Aggregate metrics for a complete tutoring session."""
    harness_name: str
    problem_id: int
    total_interactions: int
    total_time: float
    avg_response_length: float
    total_hints: int
    total_questions: int
    total_concepts: int
    student_reached_answer: bool
    estimated_understanding: float


class Evaluator:
    """Evaluates harness effectiveness across multiple dimensions."""

    def __init__(self, results_dir: str = "data/results"):
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.interactions: List[InteractionMetrics] = []
        self.sessions: List[SessionMetrics] = []

    def record_interaction(
        self,
        harness_name: str,
        problem_id: int,
        student_message: str,
        tutor_response: str,
    ) -> InteractionMetrics:
        """Record a single interaction for analysis."""

        metrics = InteractionMetrics(
            harness_name=harness_name,
            problem_id=problem_id,
            student_message=student_message,
            tutor_response=tutor_response,
            timestamp=time.time(),
            response_length=len(tutor_response),
            hints_given=self._count_hints(tutor_response),
            questions_asked=tutor_response.count("?"),
            concepts_explained=self._count_concepts(tutor_response),
        )

        self.interactions.append(metrics)
        return metrics

    def record_session(
        self,
        harness_name: str,
        problem_id: int,
        interactions: List[InteractionMetrics],
        student_reached_answer: bool,
        estimated_understanding: float,
    ) -> SessionMetrics:
        """Record aggregate session metrics."""

        if not interactions:
            return None

        total_time = (
            interactions[-1].timestamp - interactions[0].timestamp
            if len(interactions) > 1
            else 0
        )

        session = SessionMetrics(
            harness_name=harness_name,
            problem_id=problem_id,
            total_interactions=len(interactions),
            total_time=total_time,
            avg_response_length=sum(i.response_length for i in interactions)
            / len(interactions),
            total_hints=sum(i.hints_given for i in interactions),
            total_questions=sum(i.questions_asked for i in interactions),
            total_concepts=sum(i.concepts_explained for i in interactions),
            student_reached_answer=student_reached_answer,
            estimated_understanding=estimated_understanding,
        )

        self.sessions.append(session)
        return session

    def _count_hints(self, text: str) -> int:
        """Count hint-giving phrases in response."""
        hint_phrases = [
            "try", "consider", "think about", "what if", "hint",
            "remember", "recall", "notice", "observe"
        ]
        return sum(1 for phrase in hint_phrases if phrase in text.lower())

    def _count_concepts(self, text: str) -> int:
        """Count concept explanation indicators."""
        concept_phrases = [
            "because", "therefore", "this means", "the reason",
            "formula", "rule", "principle", "definition"
        ]
        return sum(1 for phrase in concept_phrases if phrase in text.lower())

    def save_results(self, experiment_name: str = None):
        """Save all results to JSON files."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = experiment_name or f"experiment_{timestamp}"

        interactions_file = self.results_dir / f"{name}_interactions.json"
        sessions_file = self.results_dir / f"{name}_sessions.json"

        with open(interactions_file, "w") as f:
            json.dump(
                [asdict(i) for i in self.interactions],
                f,
                indent=2
            )

        with open(sessions_file, "w") as f:
            json.dump(
                [asdict(s) for s in self.sessions],
                f,
                indent=2
            )

        print(f"Results saved to {self.results_dir}")
        print(f"  - Interactions: {interactions_file.name}")
        print(f"  - Sessions: {sessions_file.name}")

        return interactions_file, sessions_file

    def generate_summary(self) -> Dict[str, Any]:
        """Generate summary statistics across all harnesses."""
        if not self.sessions:
            return {"error": "No sessions recorded"}

        harness_stats = {}

        for harness_name in set(s.harness_name for s in self.sessions):
            harness_sessions = [s for s in self.sessions if s.harness_name == harness_name]

            harness_stats[harness_name] = {
                "total_sessions": len(harness_sessions),
                "avg_interactions": sum(s.total_interactions for s in harness_sessions)
                / len(harness_sessions),
                "avg_time": sum(s.total_time for s in harness_sessions)
                / len(harness_sessions),
                "avg_hints": sum(s.total_hints for s in harness_sessions)
                / len(harness_sessions),
                "avg_questions": sum(s.total_questions for s in harness_sessions)
                / len(harness_sessions),
                "avg_concepts": sum(s.total_concepts for s in harness_sessions)
                / len(harness_sessions),
                "success_rate": sum(
                    1 for s in harness_sessions if s.student_reached_answer
                ) / len(harness_sessions),
                "avg_understanding": sum(s.estimated_understanding for s in harness_sessions)
                / len(harness_sessions),
            }

        return harness_stats
