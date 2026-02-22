import pandas as pd
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional
from tools.simulate import DellServerSimulator
from src.ai.providers import AIProvider, OllamaProvider
from src.data.loader import DataLoader, CSVDataLoader
from src.reporting.reporter import IncidentReporter, LoggingReporter
from src.reporting.logger import setup_logging, log_threshold_breach, log_system_start, log_ai_analysis, log_incident
from src.reporting.metrics import PerformanceMetrics, Timer
from src.utils.config import get_config, get_project_root
from src.data.models import ThresholdConfig, IncidentReport
from src.utils.exceptions import MonitoringError, ThresholdCalculationError, AIProviderError, DataLoadError

# Monitoring constants
INCIDENT_START_STEP = 6  # Step at which simulator triggers incident (matches simulator behavior)
SEPARATOR_WIDTH = 50  # Width of separator lines in console output
DEFAULT_MONITORING_STEPS = 10  # Default number of monitoring cycles


class GuardSystem:
    """Main guard system with dependency injection"""
    
    def __init__(
        self,
        data_loader: DataLoader,
        ai_provider: AIProvider,
        reporter: IncidentReporter,
        sigma: float = 3.0,
        logger: Optional[logging.Logger] = None
    ) -> None:
        """
        Initialize guard system with dependencies.
        
        Args:
            data_loader: Data loading implementation
            ai_provider: AI provider implementation
            reporter: Incident reporter implementation
            sigma: Threshold sigma multiplier
            logger: Optional logger instance
        """
        self.data_loader = data_loader
        self.ai_provider = ai_provider
        self.reporter = reporter
        self.sigma = sigma
        self.logger = logger or logging.getLogger(__name__)
        self.metrics = PerformanceMetrics()
    
    def calculate_threshold(self) -> ThresholdConfig:
        """Calculate monitoring threshold from baseline data"""
        try:
            mean_cpu, std_cpu = self.data_loader.load_baseline_data()
            threshold_value = mean_cpu + (self.sigma * std_cpu)
            
            self.logger.info(f"Threshold calculated: {threshold_value:.2f}% ({self.sigma}-Sigma)")
            
            return ThresholdConfig(cpu_threshold=threshold_value, sigma=self.sigma)
        except DataLoadError as e:
            raise ThresholdCalculationError(f"Failed to calculate threshold: {e}")
    
    def analyze_incident(self, cpu_usage: float, threshold: float) -> str:
        """Analyze incident using AI provider with graceful degradation"""
        prompt = f"""
    Analyze this server telemetry from a Dell server. 
    A rollback was triggered. What is the most likely cause?
    
    Data:
    Current CPU: {cpu_usage:.2f}%, Threshold: {threshold:.2f}%, Status: Critical
    
    Provide a concise answer in 2-3 sentences.
    """
        
        with Timer() as timer:
            try:
                result = self.ai_provider.analyze(prompt)
                self.metrics.record_ai_call(timer.duration_ms, success=True)
                log_ai_analysis(self.logger, timer.duration_ms, success=True)
                return result
            except AIProviderError as e:
                self.metrics.record_ai_call(timer.duration_ms, success=False)
                log_ai_analysis(self.logger, timer.duration_ms, success=False)
                self.logger.warning(f"AI analysis unavailable: {e}")
                return f"AI analysis unavailable. Manual investigation required. (CPU: {cpu_usage:.2f}% exceeded threshold: {threshold:.2f}%)"
            except Exception as e:
                self.metrics.record_ai_call(timer.duration_ms, success=False)
                log_ai_analysis(self.logger, timer.duration_ms, success=False)
                self.logger.error(f"Unexpected error during AI analysis: {e}")
                return f"AI analysis failed unexpectedly. Manual investigation required."
    
    def monitor(self, simulator: DellServerSimulator, steps: int = DEFAULT_MONITORING_STEPS) -> None:
        """
        Run monitoring loop to detect anomalies and trigger rollback if needed.
        
        The monitoring loop:
        1. Calculates threshold from baseline data
        2. Checks server metrics at each step
        3. Compares against threshold (3-sigma by default)
        4. If breached: consults AI, logs incident, triggers rollback
        5. If stable: continues monitoring
        
        Args:
            simulator: Server simulator for metrics
            steps: Number of monitoring steps (default: 10)
        """
        threshold = self.calculate_threshold()
        
        log_system_start(self.logger, threshold.cpu_threshold, self.sigma)
        print(f"--- GUARD SYSTEM ACTIVE. Monitoring... ---")
        
        for step in range(1, steps + 1):
            self.metrics.record_check()
            
            # Simulate incident starting at step 6 (for demo purposes)
            has_incident: bool = step >= INCIDENT_START_STEP
            metrics = simulator.get_metrics(is_broken=has_incident)
            current_cpu: float = metrics['cpu_usage']
            
            if threshold.is_breached(current_cpu):
                # CRITICAL: Threshold breached - initiate incident response
                self.metrics.record_breach()
                
                breach_pct = ((current_cpu - threshold.cpu_threshold) / threshold.cpu_threshold) * 100
                log_threshold_breach(self.logger, current_cpu, threshold.cpu_threshold, breach_pct)
                print(f"STEP {step}: CPU {current_cpu:.2f}% --> [🚨 ALERT!]")
                
                # Consult AI for root cause analysis
                print("\n[SYSTEM]: Consulting AI for incident diagnosis...")
                ai_verdict: str = self.analyze_incident(current_cpu, threshold.cpu_threshold)
                
                print("=" * SEPARATOR_WIDTH)
                print(f"🤖 AI DIAGNOSIS:\n{ai_verdict}")
                print("=" * SEPARATOR_WIDTH + "\n")
                
                incident = IncidentReport(
                    timestamp=datetime.now(),
                    cpu_usage=current_cpu,
                    threshold=threshold.cpu_threshold,
                    ai_diagnosis=ai_verdict,
                    action_taken="AUTOMATIC ROLLBACK"
                )
                
                log_incident(
                    self.logger,
                    current_cpu,
                    threshold.cpu_threshold,
                    ai_verdict,
                    "AUTOMATIC ROLLBACK"
                )
                
                self.reporter.report_incident(incident)
                
                # Log metrics summary
                summary = self.metrics.get_summary()
                self.logger.info(f"Performance metrics: {summary}")
                
                print("LOGGED TO incidents.log. INITIATING ROLLBACK...")
                return
            else:
                print(f"STEP {step}: CPU {current_cpu:.2f}% --> [✅ STABLE]")
        
        self.logger.info("--- SYSTEM END: Deployment successful ---")
        summary = self.metrics.get_summary()
        self.logger.info(f"Final metrics: {summary}")


def run_guard_system() -> None:
    """Main entry point with dependency setup"""
    config = get_config()
    
    # Setup structured logging
    log_config = config.logging
    logger = setup_logging(
        log_file=log_config['file'],
        log_level=log_config['level'],
        log_format=log_config['format']
    )
    
    # Setup dependencies
    project_root = get_project_root()
    file_path = project_root / config.get('data', 'metrics_file')
    
    data_loader = CSVDataLoader(
        file_path=file_path,
        baseline_status=config.get('data', 'baseline_status')
    )
    
    ai_provider = OllamaProvider(model=config.ai['model'])
    
    reporter = LoggingReporter(logger)
    
    sigma: float = config.get('monitoring', 'threshold_sigma')
    
    # Create and run guard system
    guard = GuardSystem(
        data_loader=data_loader,
        ai_provider=ai_provider,
        reporter=reporter,
        sigma=sigma,
        logger=logger
    )
    
    simulator = DellServerSimulator()
    
    try:
        guard.monitor(simulator)
    except Exception as e:
        logger.error(f"Guard system failed: {e}")
        raise

if __name__ == "__main__":
    run_guard_system()
