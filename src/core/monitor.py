import pandas as pd
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional
from tools.simulate import DellServerSimulator
from src.ai.client import analyze_incident_with_ai
from src.utils.config import get_config
from src.data.models import ThresholdConfig, IncidentReport


def run_guard_system() -> None:
    """Main guard system monitoring loop"""
    config = get_config()
    
    # Configure logging from config
    log_config = config.logging
    logging.basicConfig(
        filename=log_config['file'], 
        level=getattr(logging, log_config['level']),
        format=log_config['format'],
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Get file path from config
    project_root = Path(__file__).parent.parent.parent
    file_path = project_root / config.get('data', 'metrics_file')

    try:
        df = pd.read_csv(file_path)
        baseline_status: str = config.get('data', 'baseline_status')
        healthy_data = df[df['Status'] == baseline_status]
        
        sigma: float = config.get('monitoring', 'threshold_sigma')
        threshold_value: float = healthy_data['CPU_Usage'].mean() + (sigma * healthy_data['CPU_Usage'].std())
        
        threshold = ThresholdConfig(cpu_threshold=threshold_value, sigma=sigma)
        
        logging.info("--- SYSTEM START: Guard initialized ---")
        logging.info(f"Threshold set to: {threshold.cpu_threshold:.2f}% ({sigma}-Sigma)")
        
        print(f"--- GUARD SYSTEM ACTIVE. Monitoring... ---")
    except Exception as e:
        logging.error(f"Failed to load baseline: {e}")
        return

    sim = DellServerSimulator()
    
    for i in range(1, 11):
        has_incident: bool = i >= 6
        metrics = sim.get_metrics(is_broken=has_incident)
        current_cpu: float = metrics['cpu_usage']
        
        if threshold.is_breached(current_cpu):
            # 1. LOG THE ALERT
            logging.warning(f"THRESHOLD BREACHED: CPU reached {current_cpu:.2f}%")
            print(f"STEP {i}: CPU {current_cpu:.2f}% --> [🚨 ALERT!]")
            
            # 2. AI ANALYSIS START
            print("\n[SYSTEM]: Consulting AI for incident diagnosis...")
            incident_data = f"Current CPU: {current_cpu:.2f}%, Threshold: {threshold.cpu_threshold:.2f}%, Status: Critical"
            
            # Calling our AI module
            ai_verdict: str = analyze_incident_with_ai(incident_data)
            
            print("="*50)
            print(f"🤖 AI DIAGNOSIS:\n{ai_verdict}")
            print("="*50 + "\n")
            
            # 3. CREATE INCIDENT REPORT
            incident = IncidentReport(
                timestamp=datetime.now(),
                cpu_usage=current_cpu,
                threshold=threshold.cpu_threshold,
                ai_diagnosis=ai_verdict,
                action_taken="AUTOMATIC ROLLBACK"
            )
            
            # 4. RECORD TO LOG FILE
            logging.error(f"AUTOMATIC ROLLBACK INITIATED. AI Verdict: {ai_verdict}")
            logging.error(f"Breach: {incident.breach_percentage():.1f}% over threshold")
            
            print("LOGGED TO incidents.log. INITIATING ROLLBACK...")
            return 
        else:
            print(f"STEP {i}: CPU {current_cpu:.2f}% --> [✅ STABLE]")

    logging.info("--- SYSTEM END: Deployment successful ---")

if __name__ == "__main__":
    run_guard_system()
