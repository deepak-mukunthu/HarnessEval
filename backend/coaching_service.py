"""
Coaching Service that provides feedback using different harness strategies.
Integrates with existing MathTutor React app.
"""

import sys
from pathlib import Path

# Add parent directory to path to import harnesses
sys.path.append(str(Path(__file__).parent.parent))

from src.harnesses import (
    SocraticHarness,
    DirectHarness,
    StepByStepHarness,
    DiscoveryHarness,
    AdaptiveHarness,
)
from pydantic import BaseModel
from typing import Optional, Literal
import random


class CoachingContext(BaseModel):
    """Context for coaching request."""
    question: str
    correct_answer: float
    student_answer: Optional[float] = None
    attempt: int = 1
    hint_used: bool = False
    is_correct: bool = False
    explanation: Optional[str] = None
    hint: Optional[str] = None


class CoachingResponse(BaseModel):
    """Response from coaching service."""
    message: str
    hint: Optional[str] = None
    show_hint: bool = False
    show_answer: bool = False
    encouragement: str = ""


class CoachingService:
    """Service that provides coaching feedback."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.harnesses = {}

        if api_key:
            self.harnesses = {
                "socratic": SocraticHarness(api_key),
                "direct": DirectHarness(api_key),
                "step-by-step": StepByStepHarness(api_key),
                "discovery": DiscoveryHarness(api_key),
                "adaptive": AdaptiveHarness(api_key),
            }

    def get_static_coaching(
        self, context: CoachingContext
    ) -> CoachingResponse:
        """Original hardcoded coaching messages from MathTutor."""

        if context.is_correct:
            messages = [
                "That's right! See? You knew how to do it.",
                "Perfect! Your hard work is paying off.",
                "Exactly! You're getting stronger with each question.",
                "Yes! That's the kind of thinking I like to see.",
                "Nailed it! Keep up that excellent work."
            ]
            return CoachingResponse(
                message=random.choice(messages),
                encouragement="Great job!",
                show_hint=False,
                show_answer=False
            )

        # Incorrect feedback based on attempt
        if context.attempt == 1:
            messages = [
                "Not quite. Take another look at the problem. What are you solving for?",
                "That's not it. Think about what the question is really asking.",
                "Close, but not quite right. Let me give you a hint to help you figure it out.",
                "Good try, but check your work. What step might you have missed?"
            ]
            return CoachingResponse(
                message=random.choice(messages),
                hint=context.hint,
                show_hint=True,
                show_answer=False,
                encouragement="You can do this!"
            )
        elif context.attempt == 2:
            messages = [
                "Still not there. Look at the hint carefully - it's telling you exactly what to do.",
                "You're struggling with this one. Break it down step by step.",
                "Not yet. Read the hint again and think through each part of the problem.",
                "I know this is tough, but you can get it. Use the hint to guide your thinking."
            ]
            return CoachingResponse(
                message=random.choice(messages),
                hint=context.hint,
                show_hint=True,
                show_answer=False,
                encouragement="Keep trying!"
            )
        else:  # attempt 3+
            messages = [
                "Okay, you've given it a solid effort. Let me show you how to solve this one.",
                "Alright, this one's tricky. Let me walk you through it so you understand.",
                "You tried hard, and that's what matters. Now let's learn from this together.",
                "Good persistence! Now let me show you the right approach so you can use it next time."
            ]
            return CoachingResponse(
                message=random.choice(messages),
                hint=context.hint,
                show_hint=True,
                show_answer=True,
                encouragement="Let's learn together."
            )

    def get_ai_coaching(
        self, harness_name: str, context: CoachingContext
    ) -> CoachingResponse:
        """Get coaching from AI harness."""

        if harness_name not in self.harnesses:
            raise ValueError(f"Unknown harness: {harness_name}")

        harness = self.harnesses[harness_name]

        # Build the student message for the AI
        if context.is_correct:
            student_msg = f"I answered {context.student_answer} and it was correct!"
        else:
            student_msg = (
                f"Question: {context.question}\n"
                f"My answer: {context.student_answer}\n"
                f"This is attempt #{context.attempt}.\n"
            )
            if context.hint_used and context.hint:
                student_msg += f"I saw this hint: {context.hint}\n"
            student_msg += "What should I do?"

        # Get response from harness
        try:
            response = harness.teach(student_msg)

            return CoachingResponse(
                message=response.message,
                hint=context.hint if context.attempt > 0 else None,
                show_hint=context.attempt > 0 and not context.is_correct,
                show_answer=context.attempt >= 3 and not context.is_correct,
                encouragement="You're doing great!" if context.is_correct else "Keep going!"
            )
        except Exception as e:
            # Fallback to static if AI fails
            print(f"AI coaching failed: {e}, falling back to static")
            return self.get_static_coaching(context)

    def coach(
        self,
        mode: Literal["static", "ai"],
        context: CoachingContext,
        harness: str = "socratic"
    ) -> CoachingResponse:
        """Main coaching method."""

        if mode == "static":
            return self.get_static_coaching(context)
        else:
            return self.get_ai_coaching(harness, context)

    def reset_harness(self, harness_name: str):
        """Reset conversation history for a harness."""
        if harness_name in self.harnesses:
            self.harnesses[harness_name].reset()
