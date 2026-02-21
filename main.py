import os
import subprocess
import sys

def check_dependencies():
    """
    Checks if the Ollama service is active and the 'ollama' Python library 
    is installed before proceeding with AI analysis.
    """
    print("--- [0/3] Pre-flight Check ---")
    try:
        import ollama
        # Attempt to list local models to verify connection to the Ollama server
        ollama.list()
        print("✅ Ollama service is active and responsive.")
    except Exception:
        print("❌ Error: Ollama is not running or the 'ollama' library is missing.")
        print("Required: Run 'ollama run llama3' in your terminal and install requirements.txt")
        sys.exit(1)

def main():
    """
    Main execution pipeline for the DellGuard system.
    Orchestrates data generation, anomaly detection, AI diagnosis, and reporting.
    """
    print("\n--- STARTING DELLGUARD COMPLETE PIPELINE ---\n")
    
    # 0. Initial environment and dependency check
    check_dependencies()

    # 1. Data Generation Phase
    # Generates a baseline of healthy telemetry data and saves it to CSV
    print("\n[1/3] Generating System Metrics...")
    from simulate import generate_mock_data
    generate_mock_data() 

    # 2. Monitoring & AI Analysis Phase
    # Monitors real-time metrics, detects anomalies using 3-Sigma, 
    # and consults Llama 3 for incident root-cause analysis.
    print("\n[2/3] Executing Guard System & AI Diagnosis...")
    from guard import run_guard_system
    run_guard_system()

    # 3. Post-Incident Reporting & Visualization
    # Generates a visual health chart showing the anomaly peak and rollback point.
    print("\n[3/3] Generating Visual Health Reports...")
    # The visualization is handled by the guard system or a dedicated reporter
    
    print("\n" + "="*45)
    print("🚀 PIPELINE COMPLETED SUCCESSFULLY")
    print("Output: 'incidents.log' (Logs) and 'server_health_chart.png' (Chart)")
    print("="*45 + "\n")

if __name__ == "__main__":
    main()
