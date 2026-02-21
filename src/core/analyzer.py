import pandas as pd
import os
from pathlib import Path
from src.utils.config import get_config

def calculate_release_thresholds():
    config = get_config()
    
    # Get project root and construct file path
    project_root = Path(__file__).parent.parent.parent
    file_path = project_root / config.get('data', 'metrics_file')
    
    print(f"Looking for data in: {file_path}")

    if not file_path.exists():
        print(f"Error: Could not find {file_path}")
        print("Please run simulator.py first to generate the data!")
        return

    try:
        df = pd.read_csv(file_path)
        
        # Filter: learn only from healthy data
        baseline_status = config.get('data', 'baseline_status')
        healthy_data = df[df['Status'] == baseline_status]
        
        avg_cpu = healthy_data['CPU_Usage'].mean()
        std_cpu = healthy_data['CPU_Usage'].std()
        
        # Get sigma from config
        sigma = config.get('monitoring', 'threshold_sigma')
        cpu_threshold = avg_cpu + (sigma * std_cpu)
        
        print("\n--- BASELINE CALCULATED ---")
        print(f"Average CPU: {avg_cpu:.2f}%")
        print(f"Critical Threshold ({sigma}-Sigma): {cpu_threshold:.2f}%")
        
        return cpu_threshold
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    calculate_release_thresholds()