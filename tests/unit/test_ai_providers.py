"""Unit tests for AI providers"""

import pytest
from src.ai.providers import AIProvider, OllamaProvider, MockAIProvider


def test_mock_ai_provider_default_response():
    """Test MockAIProvider with default response"""
    provider = MockAIProvider()
    result = provider.analyze("test prompt")
    
    assert result == "Mock AI analysis: CPU threshold breached"


def test_mock_ai_provider_custom_response():
    """Test MockAIProvider with custom response"""
    custom_response = "Custom test response"
    provider = MockAIProvider(response=custom_response)
    result = provider.analyze("test prompt")
    
    assert result == custom_response


def test_mock_ai_provider_multiple_calls():
    """Test MockAIProvider returns same response for multiple calls"""
    provider = MockAIProvider(response="Test")
    
    result1 = provider.analyze("prompt 1")
    result2 = provider.analyze("prompt 2")
    
    assert result1 == result2 == "Test"


def test_ollama_provider_initialization():
    """Test OllamaProvider initialization"""
    provider = OllamaProvider(model="llama3")
    
    assert provider.model == "llama3"


def test_ollama_provider_default_model():
    """Test OllamaProvider uses default model"""
    provider = OllamaProvider()
    
    assert provider.model == "llama3"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
