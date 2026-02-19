import os

def run_all():
    print("--- STARTING DELLGUARD COMPLETE PIPELINE ---")
    
    # 1. Run Simulate (Generates data)
    print("\n[1/3] Generating Metrics...")
    os.system('python3 simulate.py')
    
    # 2. Run Guard (Analyzes and tests rollback)
    print("\n[2/3] Running Guard System...")
    os.system('python3 guard.py')
    
    # 3. Run Visualizer (Shows the result)
    print("\n[3/3] Creating Visualization...")
    os.system('python3 visualizer.py')
    
    print("\n--- ALL DONE. CHECK incidents.log AND PNG CHART ---")

if __name__ == "__main__":
    run_all()