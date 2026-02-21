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
from src.utils.config import get_config
from src.data.models import ThresholdConfig, IncidentReport


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
        mean_cpu, std_cpu = self.data_loader.load_baseline_data()
        threshold_value = mean_cpu + (self.sigma * std_cpu)
        
        self.logger.info(f"Threshold calculated: {threshold_value:.2f}% ({self.sigma}-Sigma)")
        
        return ThresholdConfig(cpu_threshold=threshold_value, sigma=self.sigma)
    
    def analyze_incident(self, cpu_usage: float, threshold: float) -> str:
        """Analyze incident using AI provider"""
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
            except Exception as e:
                self.metrics.record_ai_call(timer.duration_ms, success=False)
                log_ai_analysis(self.logger, timer.duration_ms, success=False)
                return f"AI analysis failed: {e}"
    
    def monitor(self, simulator: DellServerSimulator, steps: int = 10) -> None:
        """
        Run monitoring loop.
        
        Args:
            simulator: Server simulator for metrics
            steps: Number of monitoring steps
        """
        threshold = self.calculate_threshold()
        
        log_system_start(self.logger, threshold.cpu_threshold, self.sigma)
        print(f"--- GUARD SYSTEM ACTIVE. Monitoring... ---")
        
        for i in range(1, steps + 1):
            self.metrics.record_check()
            
            has_incident: bool = i >= 6
            metrics = simulator.get_metrics(is_broken=has_incident)
            current_cpu: float = metrics['cpu_usage']
            
            if threshold.is_breached(current_cpu):
                self.metrics.record_breach()
                
                breach_pct = ((current_cpu - threshold.cpu_threshold) / threshold.cpu_threshold) * 100
                log_threshold_breach(self.logger, current_cpu, threshold.cpu_threshold, breach_pct)
                print(f"STEP {i}: CPU {current_cpu:.2f}% --> [🚨 ALERT!]")
                
                print("\n[SYSTEM]: Consulting AI for incident diagnosis...")
                ai_verdict: str = self.analyze_incident(current_cpu, threshold.cpu_threshold)
                
                print("="*50)
                print(f"🤖 AI DIAGNOSIS:\n{ai_verdict}")
                print("="*50 + "\n")
                
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
                print(f"STEP {i}: CPU {current_cpu:.2f}% --> [✅ STABLE]")
        
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
    project_root = Path(__file__).parent.parent.parent
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
