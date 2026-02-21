import ollama
from src.utils.config import get_config

def analyze_incident_with_ai(metrics_text):
    """
    Sends telemetry data to Llama 3 and requests a diagnostic verdict.
    """
    config = get_config()
    ai_config = config.ai
    
    print("\n[SYSTEM]: Sending data to AI for analysis...")
    
    prompt = f"""
    Analyze this server telemetry from a Dell server. 
    A rollback was triggered. What is the most likely cause?
    
    Data:
    {metrics_text}
    
    Provide a concise answer in 2-3 sentences.
    """

    try:
        # Requesting a response from the local Ollama server
        response = ollama.chat(model=ai_config['model'], messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])
        return response['message']['content']
    except Exception as e:
        return f"Could not connect to {ai_config['provider']}: {e}. Make sure the app is running!"

# Testing the module
if __name__ == "__main__":
    # Simulating an incident: CPU spikes to 98% and high latency
    test_data = "timestamp: 14:05:22, CPU: 98.4%, RAM: 45%, Latency: 800ms"
    result = analyze_incident_with_ai(test_data)
    print("\n--- AI ANALYSIS RESULT ---")
    print(result)