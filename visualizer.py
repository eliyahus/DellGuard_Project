import pandas as pd
import matplotlib.pyplot as plt
import os

def create_dashboard():
    # 1. Path setup
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "server_metrics.csv")
    
    if not os.path.exists(file_path):
        print("Error: server_metrics.csv not found!")
        return

    # 2. Load data
    df = pd.read_csv(file_path)
    
    # 3. Create the plot
    plt.figure(figsize=(12, 6))
    
    # Plotting CPU usage
    plt.plot(df.index, df['CPU_Usage'], label='CPU Usage (%)', color='blue', linewidth=2)
    
    # Add a red horizontal line for our Threshold (from Step 2)
    # Let's take the mean of normal data + 3 std as we did before
    normal_cpu = df[df['Status'] == 'Normal']['CPU_Usage']
    threshold = normal_cpu.mean() + (3 * normal_cpu.std())
    
    plt.axhline(y=threshold, color='red', linestyle='--', label=f'Threshold ({threshold:.2f}%)')
    
    # Highlighting the Incident area
    plt.fill_between(df.index, 0, 100, where=(df['Status'] == 'CRITICAL'), 
                     color='red', alpha=0.2, label='Incident Zone')

    # 4. Styling the chart
    plt.title('Dell Server Health Monitor: Incident Detection', fontsize=16)
    plt.xlabel('Time (Samples)', fontsize=12)
    plt.ylabel('CPU Load (%)', fontsize=12)
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.ylim(0, 110) # Keeping it clear

    # 5. Save and Show
    output_image = os.path.join(script_dir, "server_health_chart.png")
    plt.savefig(output_image)
    print(f"Chart saved as: {output_image}")
    plt.show()

if __name__ == "__main__":
    create_dashboard()