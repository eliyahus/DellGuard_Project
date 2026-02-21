"""AI provider abstraction for dependency injection"""

from abc import ABC, abstractmethod


class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    def analyze(self, prompt: str) -> str:
        """
        Analyze incident data and provide diagnosis.
        
        Args:
            prompt: Formatted prompt with incident data
            
        Returns:
            AI analysis response
        """
        pass


class OllamaProvider(AIProvider):
    """Ollama AI provider implementation"""
    
    def __init__(self, model: str = "llama3") -> None:
        self.model = model
    
    def analyze(self, prompt: str) -> str:
        """Analyze using Ollama"""
        import ollama
        
        try:
            response = ollama.chat(model=self.model, messages=[
                {'role': 'user', 'content': prompt}
            ])
            return response['message']['content']
        except Exception as e:
            return f"Could not connect to Ollama: {e}. Make sure the app is running!"


class MockAIProvider(AIProvider):
    """Mock AI provider for testing"""
    
    def __init__(self, response: str = "Mock AI analysis: CPU threshold breached") -> None:
        self.response = response
    
    def analyze(self, prompt: str) -> str:
        """Return mock response"""
        return self.response
