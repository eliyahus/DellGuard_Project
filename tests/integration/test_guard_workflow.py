"""Integration tests for full guard system workflow"""

import pytest
from src.core.monitor import GuardSystem
from tools.simulate import DellServerSimulator
from tests.constants import (
    TEST_BASELINE_MEAN_ALT,
    TEST_BASELINE_STD_ALT,
    TEST_SIGMA,
    TEST_SIGMA_ALT,
    TEST_STEPS_SHORT,
    TEST_STEPS_FULL,
    TEST_BREACH_STEP,
    TEST_EXPECTED_THRESHOLD_ALT
)


def test_full_monitoring_workflow_no_breach(guard_system) -> None:
    """Test complete monitoring workflow without breach"""
    simulator = DellServerSimulator()
    
    # Monitor for short cycle (all should be stable, breach at step 6)
    guard_system.monitor(simulator, steps=TEST_STEPS_SHORT)
    
    # Check metrics
    assert guard_system.metrics.total_checks == TEST_STEPS_SHORT
    assert guard_system.metrics.threshold_breaches == 0
    assert guard_system.metrics.ai_calls == 0


def test_full_monitoring_workflow_with_breach(mock_data_loader, console_reporter) -> None:
    """Test complete monitoring workflow with breach"""
    from src.ai.providers import MockAIProvider
    
    ai_provider = MockAIProvider(response="Test AI diagnosis")
    guard = GuardSystem(
        data_loader=mock_data_loader,
        ai_provider=ai_provider,
        reporter=console_reporter,
        sigma=TEST_SIGMA
    )
    
    simulator = DellServerSimulator()
    
    # Monitor for full cycle (breach at TEST_BREACH_STEP)
    guard.monitor(simulator, steps=TEST_STEPS_FULL)
    
    # Check metrics - stops at breach
    assert guard.metrics.total_checks == TEST_BREACH_STEP
    assert guard.metrics.threshold_breaches == 1
    assert guard.metrics.ai_calls == 1


def test_threshold_calculation_integration(console_reporter) -> None:
    """Test threshold calculation with different sigma values"""
    from src.ai.providers import MockAIProvider
    from src.data.loader import MockDataLoader
    
    data_loader = MockDataLoader(mean=TEST_BASELINE_MEAN_ALT, std=TEST_BASELINE_STD_ALT)
    ai_provider = MockAIProvider()
    
    # Test with alternative sigma
    guard = GuardSystem(
        data_loader=data_loader,
        ai_provider=ai_provider,
        reporter=console_reporter,
        sigma=TEST_SIGMA_ALT
    )
    
    threshold = guard.calculate_threshold()
    assert threshold.cpu_threshold == TEST_EXPECTED_THRESHOLD_ALT
    assert threshold.sigma == TEST_SIGMA_ALT


def test_metrics_tracking_integration(guard_system) -> None:
    """Test metrics are properly tracked throughout workflow"""
    simulator = DellServerSimulator()
    guard_system.monitor(simulator, steps=TEST_STEPS_FULL)
    
    summary = guard_system.metrics.get_summary()
    
    assert summary['total_checks'] > 0
    assert summary['breach_rate'] >= 0
    assert 'uptime_seconds' in summary
    assert 'ai_success_rate' in summary


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
