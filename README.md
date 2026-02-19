# DellGuard: Automated Deployment Safety System

**DellGuard** is a proactive incident response prototype designed to protect server infrastructure during software updates. It automatically detects performance anomalies and triggers an immediate rollback to prevent system-wide crashes.

## 🚀 Key Features
- **Statistical Baseline**: Automatically calculates "Healthy" server behavior using the 3-Sigma rule.
- **Real-time Guard**: Intercepts CPU spikes during deployment steps.
- **Automated Rollback**: Stops deployment and restores stable versions instantly upon anomaly detection.
- **Audit Logging**: Keeps a detailed `incidents.log` for post-mortem analysis.
- **Visual Analytics**: Generates health charts for incident visualization.

## 📁 Project Structure
* `main.py` - The central controller to run the entire pipeline.
* `simulator.py` - Dell server environment emulator.
* `analyzer.py` - Statistical engine for baseline calculation.
* `guard.py` - Monitoring and rollback logic.
* `visualizer.py` - Reporting tool (generates PNG charts).

## 🛠 Installation & Usage

1. **Clone the repository**:
 git clone [https://github.com/YOUR_USERNAME/DellGuard-System.git](https://github.com/YOUR_USERNAME/DellGuard-System.git)
   cd DellGuard-System

2. **Install dependencies**:
   bash
pip install -r requirements.txt

4. **Run the system**:
   bash
python3 main.py

📊 Roadmap
[x] Statistical Anomaly Detection

[x] Automated Incident Response (Rollback)

[x] System Logging

[ ] Next Step: AI-Driven Root Cause Analysis using LLMs (Ollama/Llama3)

[ ] Next Step: Integration with Prometheus/Grafana APIs
