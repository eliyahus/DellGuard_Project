import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from src.utils.config import get_config

def create_dashboard():
    config = get_config()
    
    # Get paths from config
    project_root = Path(__file__).parent.parent.parent
    file_path = project_root / config.get('data', 'metrics_file')
    
    if not file_path.exists():
        print(f"Error: {file_path} not found!")
        return

    # Load data
    df = pd.read_csv(file_path)
    
    # Get visualization config
    viz_config = config.visualization
    fig_size = viz_config['figure_size']
    dpi = viz_config['dpi']
    
    # Create the plot
    plt.figure(figsize=tuple(fig_size), dpi=dpi)
    
    # Plotting CPU usage
    plt.plot(df.index, df['CPU_Usage'], label='CPU Usage (%)', color='blue', linewidth=2)
    
    # Add threshold line
    baseline_status = config.get('data', 'baseline_status')
    normal_cpu = df[df['Status'] == baseline_status]['CPU_Usage']
    sigma = config.get('monitoring', 'threshold_sigma')
    threshold = normal_cpu.mean() + (sigma * normal_cpu.std())
    
    plt.axhline(y=threshold, color='red', linestyle='--', label=f'Threshold ({threshold:.2f}%)')
    
    # Highlighting the Incident area
    plt.fill_between(df.index, 0, 100, where=(df['Status'] == 'CRITICAL'), 
                     color='red', alpha=0.2, label='Incident Zone')

    # Styling the chart
    plt.title('Dell Server Health Monitor: Incident Detection', fontsize=16)
    plt.xlabel('Time (Samples)', fontsize=12)
    plt.ylabel('CPU Load (%)', fontsize=12)
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.ylim(0, 110)

    # Save and Show
    output_image = project_root / viz_config['output_file']
    plt.savefig(output_image)
    print(f"Chart saved as: {output_image}")
    plt.show()

if __name__ == "__main__":
    create_dashboard()