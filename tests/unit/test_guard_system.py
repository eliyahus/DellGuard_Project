"""Unit tests for GuardSystem"""

import pytest
from datetime import datetime
from src.core.monitor import GuardSystem
from src.ai.providers import MockAIProvider
from src.data.loader import MockDataLoader
from src.reporting.reporter import ConsoleReporter
from src.data.models import ThresholdConfig
from tools.simulate import DellServerSimulator


def test_threshold_calculation():
    """Test threshold calculation with mock data"""
    data_loader = MockDataLoader(mean=40.0, std=5.0)
    ai_provider = MockAIProvider()
    reporter = ConsoleReporter()
    
    guard = GuardSystem(
        data_loader=data_loader,
        ai_provider=ai_provider,
        reporter=reporter,
        sigma=3.0
    )
    
    threshold = guard.calculate_threshold()
    
    # 40 + (3 * 5) = 55
    assert threshold.cpu_threshold == 55.0
    assert threshold.sigma == 3.0


def test_threshold_breach_detection():
    """Test threshold breach detection"""
    threshold = ThresholdConfig(cpu_threshold=50.0, sigma=3.0)
    
    assert threshold.is_breached(60.0) is True
    assert threshold.is_breached(40.0) is False
    assert threshold.is_breached(50.0) is False


def test_ai_analysis():
    """Test AI analysis with mock provider"""
    data_loader = MockDataLoader()
    ai_provider = MockAIProvider(response="Test AI response")
    reporter = ConsoleReporter()
    
    guard = GuardSystem(
        data_loader=data_loader,
        ai_provider=ai_provider,
        reporter=reporter
    )
    
    result = guard.analyze_incident(cpu_usage=98.5, threshold=50.0)
    
    assert result == "Test AI response"


def test_guard_system_integration():
    """Test full guard system with mocks"""
    data_loader = MockDataLoader(mean=40.0, std=5.0)
    ai_provider = MockAIProvider(response="Mock diagnosis")
    reporter = ConsoleReporter()
    
    guard = GuardSystem(
        data_loader=data_loader,
        ai_provider=ai_provider,
        reporter=reporter,
        sigma=3.0
    )
    
    # Should not raise any exceptions
    threshold = guard.calculate_threshold()
    assert threshold.cpu_threshold == 55.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
