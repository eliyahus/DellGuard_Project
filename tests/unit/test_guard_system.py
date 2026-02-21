"""Unit tests for GuardSystem"""

import pytest
from src.core.monitor import GuardSystem
from src.data.models import ThresholdConfig
from tests.constants import (
    TEST_BASELINE_MEAN,
    TEST_BASELINE_STD,
    TEST_SIGMA,
    TEST_EXPECTED_THRESHOLD
)


def test_threshold_calculation(guard_system) -> None:
    """Test threshold calculation with mock data"""
    threshold = guard_system.calculate_threshold()
    
    # TEST_BASELINE_MEAN + (TEST_SIGMA * TEST_BASELINE_STD) = 40 + (3 * 5) = 55
    assert threshold.cpu_threshold == TEST_EXPECTED_THRESHOLD
    assert threshold.sigma == TEST_SIGMA


def test_threshold_breach_detection() -> None:
    """Test threshold breach detection"""
    threshold = ThresholdConfig(cpu_threshold=50.0, sigma=TEST_SIGMA)
    
    assert threshold.is_breached(60.0) is True
    assert threshold.is_breached(40.0) is False
    assert threshold.is_breached(50.0) is False


def test_ai_analysis(mock_data_loader, console_reporter) -> None:
    """Test AI analysis with mock provider"""
    from src.ai.providers import MockAIProvider
    
    ai_provider = MockAIProvider(response="Test AI response")
    guard = GuardSystem(
        data_loader=mock_data_loader,
        ai_provider=ai_provider,
        reporter=console_reporter
    )
    
    result = guard.analyze_incident(cpu_usage=98.5, threshold=50.0)
    
    assert result == "Test AI response"


def test_guard_system_integration(guard_system) -> None:
    """Test full guard system with mocks"""
    threshold = guard_system.calculate_threshold()
    assert threshold.cpu_threshold == TEST_EXPECTED_THRESHOLD


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
