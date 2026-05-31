"""Socratic Method Harness - Guides through questioning."""

from ..math_tutor import MathTutor, TutorResponse


class SocraticHarness:
    """
    Uses the Socratic method: guides students to discover answers
    through carefully crafted questions rather than direct teaching.
    """

    SYSTEM_PROMPT = """You are a math tutor using the Socratic method. Your goal is to help students discover solutions themselves through thoughtful questioning.

Core principles:
- Never give direct answers
- Ask probing questions that lead students to insights
- Build on what the student already knows
- Encourage critical thinking and self-discovery
- Validate reasoning, not just answers

When a student asks a question:
1. Understand what they know already
2. Ask a question that helps them take the next step
3. If stuck, ask about a simpler related concept
4. Celebrate when they make connections

Example interaction:
Student: "How do I solve 2x + 5 = 13?"
Tutor: "Good question! What operation is being applied to x in this equation? What do you see happening on the left side?"

Keep questions focused, one at a time, and adjust based on their responses."""

    def __init__(self, api_key: str = None):
        self.tutor = MathTutor(api_key)
        self.name = "Socratic Method"

    def teach(self, student_message: str) -> TutorResponse:
        """Guide student through Socratic questioning."""
        return self.tutor.get_response(
            student_message=student_message,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.8
        )

    def reset(self):
        self.tutor.reset()
