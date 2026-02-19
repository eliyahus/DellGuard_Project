import pandas as pd
import time
import os
import logging # Standard professional logging library
from simulate import DellServerSimulator

# --- LOGGING SETUP ---
# This configures the file 'incidents.log'
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
            # RECORDING THE INCIDENT TO FILE
            logging.warning(f"THRESHOLD BREACHED: CPU reached {current_cpu:.2f}%")
            logging.error("AUTOMATIC ROLLBACK INITIATED")
            
            print(f"STEP {i}: CPU {current_cpu:.2f}% --> [🚨 ALERT!]")
            print("LOGGED TO incidents.log. INITIATING ROLLBACK...")
            return 
        else:
            print(f"STEP {i}: CPU {current_cpu:.2f}% --> [✅ STABLE]")
            # We don't log every stable step to keep the file clean, 
            # only start and critical events.

    logging.info("--- SYSTEM END: Deployment successful ---")

if __name__ == "__main__":
    run_guard_system()