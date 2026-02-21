"""Incident reporter abstraction"""

from abc import ABC, abstractmethod
from src.data.models import IncidentReport


class IncidentReporter(ABC):
    """Abstract base class for incident reporting"""
    
    @abstractmethod
    def report_incident(self, incident: IncidentReport) -> None:
        """
        Report an incident.
        
        Args:
            incident: Incident report to log
        """
        pass


class LoggingReporter(IncidentReporter):
    """Logging-based incident reporter"""
    
    def __init__(self, logger) -> None:
        self.logger = logger
    
    def report_incident(self, incident: IncidentReport) -> None:
        """Report incident to log file"""
        self.logger.error(f"AUTOMATIC ROLLBACK INITIATED. AI Verdict: {incident.ai_diagnosis}")
        self.logger.error(f"Breach: {incident.breach_percentage():.1f}% over threshold")


class ConsoleReporter(IncidentReporter):
    """Console-based incident reporter for testing"""
    
    def report_incident(self, incident: IncidentReport) -> None:
        """Report incident to console"""
        print(f"[INCIDENT] {incident.timestamp}")
        print(f"[INCIDENT] CPU: {incident.cpu_usage:.2f}% (Threshold: {incident.threshold:.2f}%)")
        print(f"[INCIDENT] Breach: {incident.breach_percentage():.1f}%")
        print(f"[INCIDENT] Action: {incident.action_taken}")
        if incident.ai_diagnosis:
            print(f"[INCIDENT] AI: {incident.ai_diagnosis}")
