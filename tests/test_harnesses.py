"""Unit tests for harness implementations."""

import pytest
import os
from unittest.mock import Mock, patch
from src.harnesses import (
    SocraticHarness,
    DirectHarness,
    StepByStepHarness,
    DiscoveryHarness,
    AdaptiveHarness,
)


@pytest.fixture
def mock_api_key():
    return "test_api_key"


def test_socratic_harness_initialization(mock_api_key):
    harness = SocraticHarness(mock_api_key)
    assert harness.name == "Socratic Method"
    assert "Socratic" in harness.SYSTEM_PROMPT


def test_direct_harness_initialization(mock_api_key):
    harness = DirectHarness(mock_api_key)
    assert harness.name == "Direct Instruction"
    assert "direct instruction" in harness.SYSTEM_PROMPT


def test_step_by_step_harness_initialization(mock_api_key):
    harness = StepByStepHarness(mock_api_key)
    assert harness.name == "Step-by-Step"
    assert "step" in harness.SYSTEM_PROMPT.lower()


def test_discovery_harness_initialization(mock_api_key):
    harness = DiscoveryHarness(mock_api_key)
    assert harness.name == "Discovery Learning"
    assert "discovery" in harness.SYSTEM_PROMPT.lower()


def test_adaptive_harness_initialization(mock_api_key):
    harness = AdaptiveHarness(mock_api_key)
    assert harness.name == "Adaptive"
    assert harness.difficulty_level == 1


def test_all_harnesses_have_unique_names(mock_api_key):
    harnesses = [
        SocraticHarness(mock_api_key),
        DirectHarness(mock_api_key),
        StepByStepHarness(mock_api_key),
        DiscoveryHarness(mock_api_key),
        AdaptiveHarness(mock_api_key),
    ]

    names = [h.name for h in harnesses]
    assert len(names) == len(set(names)), "Harness names must be unique"


def test_harness_reset(mock_api_key):
    harness = SocraticHarness(mock_api_key)
    harness.tutor.conversation_history.append(
        Mock(role="user", content="test")
    )
    assert len(harness.tutor.conversation_history) > 0

    harness.reset()
    assert len(harness.tutor.conversation_history) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
