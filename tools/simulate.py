import numpy as np
import time

class DellServerSimulator:
    def __init__(self):
        # Base metrics for a "healthy" server
        self.normal_cpu = 40.0      # CPU usage %
        self.normal_latency = 100.0 # Response latency in ms
        self.normal_errors = 0.02   # 2% error rate is normal
        self.noise_level = 0.05     # Natural fluctuations (noise)

    def get_metrics(self, is_broken=False):
        """
        Generates server metrics.
        If is_broken=True, simulates a bug following a release.
        """
        # Add random noise to ensure data isn't "sterile"
        noise = np.random.uniform(-self.noise_level, self.noise_level)
        
        if not is_broken:
            # Healthy state
            cpu = self.normal_cpu * (1 + noise)
            latency = self.normal_latency * (1 + noise)
            errors = self.normal_errors * (1 + np.random.uniform(0, 0.01))
        else:
            # "Incident" state after a bad release
            # CPU starts leaking, latency spikes
            cpu = self.normal_cpu * (2.5 + noise)      # 2.5x spike
            latency = self.normal_latency * (5 + noise) # 5x spike
            errors = self.normal_errors * (10 + noise)  # Errors increased 10x
            
        return {
            "timestamp": time.time(),
            "cpu_usage": round(cpu, 2),
            "latency_ms": round(latency, 2),
            "error_rate": round(errors, 4)
        }

import csv # Library for working with tabular data (CSV)

if __name__ == "__main__":
    sim = DellServerSimulator()
    filename = "server_metrics.csv"
    
    print(f"Generating report and saving to {filename}...")
    
    # Open the file for writing
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the table header (column names)
        writer.writerow(["Timestamp", "CPU_Usage", "Latency_MS", "Error_Rate", "Status"])
        
        # Generate 100 rows of normal (healthy) data
        for _ in range(100):
            m = sim.get_metrics(is_broken=False)
            writer.writerow([m["timestamp"], m["cpu_usage"], m["latency_ms"], m["error_rate"], "Normal"])
            
        # Generate 10 rows of critical (incident) data
        for _ in range(10):
            m = sim.get_metrics(is_broken=True)
            writer.writerow([m["timestamp"], m["cpu_usage"], m["latency_ms"], m["error_rate"], "CRITICAL"])

    print("Success! Your first dataset is ready.")