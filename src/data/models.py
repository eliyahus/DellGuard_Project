"""Data models for DellGuard"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ServerMetrics:
    """Server performance metrics"""
    timestamp: float
    cpu_usage: float
    latency_ms: float
    error_rate: float
    status: str = "Normal"
    
    def is_critical(self) -> bool:
        """Check if metrics indicate critical status"""
        return self.status == "CRITICAL"


@dataclass
class ThresholdConfig:
    """Threshold configuration for monitoring"""
    cpu_threshold: float
    sigma: float = 3.0
    
    def is_breached(self, cpu_usage: float) -> bool:
        """Check if CPU usage breaches threshold"""
        return cpu_usage > self.cpu_threshold


@dataclass
class IncidentReport:
    """Incident report with AI diagnosis"""
    timestamp: datetime
    cpu_usage: float
    threshold: float
    ai_diagnosis: Optional[str]
    action_taken: str
    
    def breach_percentage(self) -> float:
        """Calculate percentage over threshold"""
        return ((self.cpu_usage - self.threshold) / self.threshold) * 100
