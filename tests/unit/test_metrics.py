"""Unit tests for performance metrics"""

import pytest
from datetime import datetime, timedelta
from src.reporting.metrics import PerformanceMetrics, Timer
import time


def test_performance_metrics_initialization():
    """Test PerformanceMetrics initializes with zeros"""
    metrics = PerformanceMetrics()
    
    assert metrics.total_checks == 0
    assert metrics.threshold_breaches == 0
    assert metrics.ai_calls == 0
    assert metrics.ai_failures == 0
    assert metrics.total_ai_duration_ms == 0.0


def test_performance_metrics_record_check():
    """Test recording monitoring checks"""
    metrics = PerformanceMetrics()
    
    metrics.record_check()
    metrics.record_check()
    metrics.record_check()
    
    assert metrics.total_checks == 3


def test_performance_metrics_record_breach():
    """Test recording threshold breaches"""
    metrics = PerformanceMetrics()
    
    metrics.record_breach()
    metrics.record_breach()
    
    assert metrics.threshold_breaches == 2


def test_performance_metrics_record_ai_call_success():
    """Test recording successful AI call"""
    metrics = PerformanceMetrics()
    
    metrics.record_ai_call(duration_ms=1500.0, success=True)
    
    assert metrics.ai_calls == 1
    assert metrics.ai_failures == 0
    assert metrics.total_ai_duration_ms == 1500.0


def test_performance_metrics_record_ai_call_failure():
    """Test recording failed AI call"""
    metrics = PerformanceMetrics()
    
    metrics.record_ai_call(duration_ms=500.0, success=False)
    
    assert metrics.ai_calls == 1
    assert metrics.ai_failures == 1
    assert metrics.total_ai_duration_ms == 500.0


def test_performance_metrics_summary():
    """Test metrics summary calculation"""
    metrics = PerformanceMetrics()
    
    # Simulate some activity
    for _ in range(10):
        metrics.record_check()
    
    metrics.record_breach()
    metrics.record_breach()
    
    metrics.record_ai_call(1000.0, success=True)
    metrics.record_ai_call(1500.0, success=True)
    metrics.record_ai_call(500.0, success=False)
    
    summary = metrics.get_summary()
    
    assert summary['total_checks'] == 10
    assert summary['threshold_breaches'] == 2
    assert summary['breach_rate'] == 0.2  # 2/10
    assert summary['ai_calls'] == 3
    assert summary['ai_failures'] == 1
    assert summary['ai_success_rate'] == pytest.approx(0.667, rel=0.01)
    assert summary['avg_ai_duration_ms'] == 1000.0  # (1000+1500+500)/3


def test_timer_context_manager():
    """Test Timer context manager"""
    with Timer() as timer:
        time.sleep(0.01)  # Sleep for 10ms
    
    assert timer.duration_ms >= 10.0
    assert timer.start is not None
    assert timer.end is not None


def test_timer_multiple_uses():
    """Test Timer can be used multiple times"""
    timer1 = Timer()
    with timer1:
        time.sleep(0.01)
    
    timer2 = Timer()
    with timer2:
        time.sleep(0.02)
    
    assert timer1.duration_ms < timer2.duration_ms


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
