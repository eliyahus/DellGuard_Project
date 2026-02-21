import numpy as np
import time

# Healthy server baseline metrics
NORMAL_CPU_PERCENT = 40.0
NORMAL_LATENCY_MS = 100.0
NORMAL_ERROR_RATE = 0.02  # 2% error rate
NOISE_LEVEL = 0.05  # 5% natural fluctuation

# Incident multipliers - simulate degraded performance
CPU_SPIKE_MULTIPLIER = 2.5  # CPU usage increases 2.5x during incident
LATENCY_SPIKE_MULTIPLIER = 5.0  # Latency increases 5x during incident
ERROR_SPIKE_MULTIPLIER = 10.0  # Error rate increases 10x during incident

# Data generation constants
BASELINE_SAMPLE_COUNT = 100  # Number of healthy samples to generate
INCIDENT_SAMPLE_COUNT = 10  # Number of incident samples to generate


class DellServerSimulator:
    def __init__(self):
        """Initialize simulator with baseline healthy server metrics"""
        self.normal_cpu = NORMAL_CPU_PERCENT
        self.normal_latency = NORMAL_LATENCY_MS
        self.normal_errors = NORMAL_ERROR_RATE
        self.noise_level = NOISE_LEVEL

    def get_metrics(self, is_broken=False):
        """
        Generates server metrics.
        
        Args:
            is_broken: If True, simulates degraded performance after bad deployment
            
        Returns:
            Dict with timestamp, cpu_usage, latency_ms, error_rate
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
            cpu = self.normal_cpu * (CPU_SPIKE_MULTIPLIER + noise)
            latency = self.normal_latency * (LATENCY_SPIKE_MULTIPLIER + noise)
            errors = self.normal_errors * (ERROR_SPIKE_MULTIPLIER + noise)
            
        return {
            "timestamp": time.time(),
            "cpu_usage": round(cpu, 2),
            "latency_ms": round(latency, 2),
            "error_rate": round(errors, 4)
        }


import csv


if __name__ == "__main__":
    sim = DellServerSimulator()
    filename = "server_metrics.csv"
    
    print(f"Generating report and saving to {filename}...")
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the table header
        writer.writerow(["Timestamp", "CPU_Usage", "Latency_MS", "Error_Rate", "Status"])
        
        # Generate baseline (healthy) data
        for _ in range(BASELINE_SAMPLE_COUNT):
            m = sim.get_metrics(is_broken=False)
            writer.writerow([m["timestamp"], m["cpu_usage"], m["latency_ms"], m["error_rate"], "Normal"])
            
        # Generate incident (critical) data
        for _ in range(INCIDENT_SAMPLE_COUNT):
            m = sim.get_metrics(is_broken=True)
            writer.writerow([m["timestamp"], m["cpu_usage"], m["latency_ms"], m["error_rate"], "CRITICAL"])

    print("Success! Your first dataset is ready.")