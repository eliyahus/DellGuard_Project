import pandas as pd
import os # Library for working with the operating system

def calculate_release_thresholds():
    # MAGIC LINE: Find the folder where THIS script is saved
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create the full path to the CSV file in that same folder
    file_path = os.path.join(script_dir, "server_metrics.csv")
    
    print(f"Looking for data in: {file_path}")

    # Check if the file actually exists before trying to open it
    if not os.path.exists(file_path):
        print(f"Error: Could not find {file_path}")
        print("Please run simulator.py first to generate the data!")
        return

    try:
        df = pd.read_csv(file_path)
        
        # Filter: learn only from healthy data
        healthy_data = df[df['Status'] == 'Normal']
        
        avg_cpu = healthy_data['CPU_Usage'].mean()
        std_cpu = healthy_data['CPU_Usage'].std()
        
        # 3-Sigma threshold
        cpu_threshold = avg_cpu + (3 * std_cpu)
        
        print("\n--- BASELINE CALCULATED ---")
        print(f"Average CPU: {avg_cpu:.2f}%")
        print(f"Critical Threshold: {cpu_threshold:.2f}%")
        
        return cpu_threshold
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    calculate_release_thresholds()