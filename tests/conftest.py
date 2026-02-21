"""Pytest configuration and shared fixtures for DellGuard tests"""

import pytest
from src.ai.providers import MockAIProvider
from src.data.loader import MockDataLoader
from src.reporting.reporter import ConsoleReporter
from src.core.monitor import GuardSystem
from tests.constants import (
    TEST_BASELINE_MEAN,
    TEST_BASELINE_STD,
    TEST_SIGMA,
    TEST_AI_RESPONSE_DEFAULT
)


@pytest.fixture
def mock_data_loader():
    """Fixture providing a MockDataLoader with standard test values"""
    return MockDataLoader(mean=TEST_BASELINE_MEAN, std=TEST_BASELINE_STD)


@pytest.fixture
def mock_ai_provider():
    """Fixture providing a MockAIProvider with default response"""
    return MockAIProvider(response=TEST_AI_RESPONSE_DEFAULT)


@pytest.fixture
def console_reporter():
    """Fixture providing a ConsoleReporter for test output"""
    return ConsoleReporter()


@pytest.fixture
def guard_system(mock_data_loader, mock_ai_provider, console_reporter):
    """Fixture providing a fully configured GuardSystem for testing"""
    return GuardSystem(
        data_loader=mock_data_loader,
        ai_provider=mock_ai_provider,
        reporter=console_reporter,
        sigma=TEST_SIGMA
    )
