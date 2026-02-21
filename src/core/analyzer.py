import pandas as pd
from pathlib import Path
from typing import Optional
from src.utils.config import get_config


def calculate_release_thresholds() -> Optional[float]:
    """
    Calculate CPU threshold based on baseline data.
    
    Returns:
        CPU threshold value or None if calculation fails
    """
    config = get_config()
    
    # Get project root and construct file path
    project_root = Path(__file__).parent.parent.parent
    file_path = project_root / config.get('data', 'metrics_file')
    
    print(f"Looking for data in: {file_path}")

    if not file_path.exists():
        print(f"Error: Could not find {file_path}")
        print("Please run simulator.py first to generate the data!")
        return None

    try:
        df = pd.read_csv(file_path)
        
        # Filter: learn only from healthy data
        baseline_status: str = config.get('data', 'baseline_status')
        healthy_data = df[df['Status'] == baseline_status]
        
        avg_cpu: float = healthy_data['CPU_Usage'].mean()
        std_cpu: float = healthy_data['CPU_Usage'].std()
        
        # Get sigma from config
        sigma: float = config.get('monitoring', 'threshold_sigma')
        cpu_threshold: float = avg_cpu + (sigma * std_cpu)
        
        print("\n--- BASELINE CALCULATED ---")
        print(f"Average CPU: {avg_cpu:.2f}%")
        print(f"Critical Threshold ({sigma}-Sigma): {cpu_threshold:.2f}%")
        
        return cpu_threshold
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    calculate_release_thresholds()