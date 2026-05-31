"""Base MathTutor implementation using Claude API."""

import os
from typing import List, Dict, Optional
from anthropic import Anthropic
from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class TutorResponse(BaseModel):
    message: str
    hint_given: bool
    concept_explained: str
    estimated_understanding: float


class MathTutor:
    """Base math tutor that different harnesses will build upon."""

    def __init__(self, api_key: Optional[str] = None):
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.conversation_history: List[Message] = []
        self.model = "claude-sonnet-4-6"

    def get_response(
        self,
        student_message: str,
        system_prompt: str,
        temperature: float = 1.0
    ) -> TutorResponse:
        """Get a response from the tutor using the specified system prompt."""

        self.conversation_history.append(
            Message(role="user", content=student_message)
        )

        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in self.conversation_history
        ]

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            temperature=temperature,
            system=system_prompt,
            messages=messages
        )

        assistant_message = response.content[0].text

        self.conversation_history.append(
            Message(role="assistant", content=assistant_message)
        )

        hint_given = any(word in assistant_message.lower()
                        for word in ["hint", "try", "consider", "think about"])

        concept_words = ["because", "therefore", "means", "represents", "formula"]
        concept_explained = any(word in assistant_message.lower() for word in concept_words)

        question_marks = assistant_message.count("?")
        understanding_estimate = min(1.0, max(0.0, 1.0 - (question_marks * 0.1)))

        return TutorResponse(
            message=assistant_message,
            hint_given=hint_given,
            concept_explained="general" if concept_explained else "none",
            estimated_understanding=understanding_estimate
        )

    def reset(self):
        """Reset conversation history."""
        self.conversation_history = []
