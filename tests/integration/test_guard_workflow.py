"""Integration tests for full guard system workflow"""

import pytest
from src.core.monitor import GuardSystem
from src.ai.providers import MockAIProvider
from src.data.loader import MockDataLoader
from src.reporting.reporter import ConsoleReporter
from tools.simulate import DellServerSimulator


def test_full_monitoring_workflow_no_breach():
    """Test complete monitoring workflow without breach"""
    data_loader = MockDataLoader(mean=40.0, std=5.0)
    ai_provider = MockAIProvider()
    reporter = ConsoleReporter()
    
    guard = GuardSystem(
        data_loader=data_loader,
        ai_provider=ai_provider,
        reporter=reporter,
        sigma=3.0
    )
    
    # Create simulator that won't breach (all normal)
    simulator = DellServerSimulator()
    
    # Monitor for 5 steps (all should be stable)
    guard.monitor(simulator, steps=5)
    
    # Check metrics
    assert guard.metrics.total_checks == 5
    assert guard.metrics.threshold_breaches == 0
    assert guard.metrics.ai_calls == 0


def test_full_monitoring_workflow_with_breach():
    """Test complete monitoring workflow with breach"""
    data_loader = MockDataLoader(mean=40.0, std=5.0)
    ai_provider = MockAIProvider(response="Test AI diagnosis")
    reporter = ConsoleReporter()
    
    guard = GuardSystem(
        data_loader=data_loader,
        ai_provider=ai_provider,
        reporter=reporter,
        sigma=3.0
    )
    
    simulator = DellServerSimulator()
    
    # Monitor for 10 steps (breach at step 6)
    guard.monitor(simulator, steps=10)
    
    # Check metrics
    assert guard.metrics.total_checks == 6  # Stops at breach
    assert guard.metrics.threshold_breaches == 1
    assert guard.metrics.ai_calls == 1


def test_threshold_calculation_integration():
    """Test threshold calculation with different sigma values"""
    data_loader = MockDataLoader(mean=50.0, std=10.0)
    ai_provider = MockAIProvider()
    reporter = ConsoleReporter()
    
    # Test with sigma=2
    guard = GuardSystem(
        data_loader=data_loader,
        ai_provider=ai_provider,
        reporter=reporter,
        sigma=2.0
    )
    
    threshold = guard.calculate_threshold()
    assert threshold.cpu_threshold == 70.0  # 50 + (2 * 10)
    assert threshold.sigma == 2.0


def test_metrics_tracking_integration():
    """Test metrics are properly tracked throughout workflow"""
    data_loader = MockDataLoader(mean=40.0, std=5.0)
    ai_provider = MockAIProvider()
    reporter = ConsoleReporter()
    
    guard = GuardSystem(
        data_loader=data_loader,
        ai_provider=ai_provider,
        reporter=reporter,
        sigma=3.0
    )
    
    simulator = DellServerSimulator()
    guard.monitor(simulator, steps=10)
    
    summary = guard.metrics.get_summary()
    
    assert summary['total_checks'] > 0
    assert summary['breach_rate'] >= 0
    assert 'uptime_seconds' in summary
    assert 'ai_success_rate' in summary


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
