import pandas as pd
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional
from tools.simulate import DellServerSimulator
from src.ai.providers import AIProvider, OllamaProvider
from src.data.loader import DataLoader, CSVDataLoader
from src.reporting.reporter import IncidentReporter, LoggingReporter
from src.utils.config import get_config
from src.data.models import ThresholdConfig, IncidentReport


class GuardSystem:
    """Main guard system with dependency injection"""
    
    def __init__(
        self,
        data_loader: DataLoader,
        ai_provider: AIProvider,
        reporter: IncidentReporter,
        sigma: float = 3.0
    ) -> None:
        """
        Initialize guard system with dependencies.
        
        Args:
            data_loader: Data loading implementation
            ai_provider: AI provider implementation
            reporter: Incident reporter implementation
            sigma: Threshold sigma multiplier
        """
        self.data_loader = data_loader
        self.ai_provider = ai_provider
        self.reporter = reporter
        self.sigma = sigma
        self.logger = logging.getLogger(__name__)
    
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
        return self.ai_provider.analyze(prompt)
    
    def monitor(self, simulator: DellServerSimulator, steps: int = 10) -> None:
        """
        Run monitoring loop.
        
        Args:
            simulator: Server simulator for metrics
            steps: Number of monitoring steps
        """
        threshold = self.calculate_threshold()
        
        self.logger.info("--- SYSTEM START: Guard initialized ---")
        print(f"--- GUARD SYSTEM ACTIVE. Monitoring... ---")
        
        for i in range(1, steps + 1):
            has_incident: bool = i >= 6
            metrics = simulator.get_metrics(is_broken=has_incident)
            current_cpu: float = metrics['cpu_usage']
            
            if threshold.is_breached(current_cpu):
                self.logger.warning(f"THRESHOLD BREACHED: CPU reached {current_cpu:.2f}%")
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
                
                self.reporter.report_incident(incident)
                
                print("LOGGED TO incidents.log. INITIATING ROLLBACK...")
                return
            else:
                print(f"STEP {i}: CPU {current_cpu:.2f}% --> [✅ STABLE]")
        
        self.logger.info("--- SYSTEM END: Deployment successful ---")


def run_guard_system() -> None:
    """Main entry point with dependency setup"""
    config = get_config()
    
    # Configure logging
    log_config = config.logging
    logging.basicConfig(
        filename=log_config['file'], 
        level=getattr(logging, log_config['level']),
        format=log_config['format'],
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Setup dependencies
    project_root = Path(__file__).parent.parent.parent
    file_path = project_root / config.get('data', 'metrics_file')
    
    data_loader = CSVDataLoader(
        file_path=file_path,
        baseline_status=config.get('data', 'baseline_status')
    )
    
    ai_provider = OllamaProvider(model=config.ai['model'])
    
    logger = logging.getLogger(__name__)
    reporter = LoggingReporter(logger)
    
    sigma: float = config.get('monitoring', 'threshold_sigma')
    
    # Create and run guard system
    guard = GuardSystem(
        data_loader=data_loader,
        ai_provider=ai_provider,
        reporter=reporter,
        sigma=sigma
    )
    
    simulator = DellServerSimulator()
    
    try:
        guard.monitor(simulator)
    except Exception as e:
        logger.error(f"Guard system failed: {e}")
        raise

if __name__ == "__main__":
    run_guard_system()
