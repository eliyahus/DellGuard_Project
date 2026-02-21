"""AI provider abstraction for dependency injection"""

from abc import ABC, abstractmethod
from src.utils.retry import retry
from src.utils.exceptions import AIProviderError


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
    
    @retry(max_attempts=3, delay=1.0, backoff=2.0)
    def analyze(self, prompt: str) -> str:
        """Analyze using Ollama with retry logic"""
        import ollama
        
        try:
            response = ollama.chat(model=self.model, messages=[
                {'role': 'user', 'content': prompt}
            ])
            return response['message']['content']
        except KeyError as e:
            raise AIProviderError(f"Invalid AI response format: missing {e}")
        except ConnectionError:
            raise AIProviderError(f"Cannot connect to Ollama. Ensure service is running.")
        except Exception as e:
            raise AIProviderError(f"AI analysis failed: {e}")


class MockAIProvider(AIProvider):
    """Mock AI provider for testing"""
    
    def __init__(self, response: str = "Mock AI analysis: CPU threshold breached") -> None:
        self.response = response
    
    def analyze(self, prompt: str) -> str:
        """Return mock response"""
        return self.response
