import pandas as pd
import time
from src.ai.client import analyze_incident_with_ai
import os
import logging
from tools.simulate import DellServerSimulator

# --- LOGGING SETUP ---
logging.basicConfig(
    filename='incidents.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def run_guard_system():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "server_metrics.csv")

    try:
        df = pd.read_csv(file_path)
        healthy_data = df[df['Status'] == 'Normal']
        threshold = healthy_data['CPU_Usage'].mean() + (3 * healthy_data['CPU_Usage'].std())
        
        logging.info("--- SYSTEM START: Guard initialized ---")
        logging.info(f"Threshold set to: {threshold:.2f}%")
        
        print(f"--- GUARD SYSTEM ACTIVE. Monitoring... ---")
    except Exception as e:
        logging.error(f"Failed to load baseline: {e}")
        return

    sim = DellServerSimulator()
    
    for i in range(1, 11):
        has_incident = True if i >= 6 else False
        metrics = sim.get_metrics(is_broken=has_incident)
        current_cpu = metrics['cpu_usage']
        
        if current_cpu > threshold:
            # 1. LOG THE ALERT
            logging.warning(f"THRESHOLD BREACHED: CPU reached {current_cpu:.2f}%")
            print(f"STEP {i}: CPU {current_cpu:.2f}% --> [🚨 ALERT!]")
            
            # 2. AI ANALYSIS START
            print("\n[SYSTEM]: Consulting AI for incident diagnosis...")
            incident_data = f"Current CPU: {current_cpu:.2f}%, Threshold: {threshold:.2f}%, Status: Critical"
            
            # Calling our Llama 3 module
            ai_verdict = analyze_incident_with_ai(incident_data)
            
            print("="*50)
            print(f"🤖 AI DIAGNOSIS:\n{ai_verdict}")
            print("="*50 + "\n")
            
            # 3. RECORD AI VERDICT TO LOG FILE
            logging.error(f"AUTOMATIC ROLLBACK INITIATED. AI Verdict: {ai_verdict}")
            
            print("LOGGED TO incidents.log. INITIATING ROLLBACK...")
            return 
        else:
            print(f"STEP {i}: CPU {current_cpu:.2f}% --> [✅ STABLE]")

    logging.info("--- SYSTEM END: Deployment successful ---")

if __name__ == "__main__":
    run_guard_system()
