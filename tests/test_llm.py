#!/usr/bin/env python3
"""
test_llm.py - Tests for LLM provider integrations
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arubaclaw import ArubaClawAgent, PROVIDERS


class TestLLMProviders(unittest.TestCase):
    """Test LLM provider API formatting."""
    
    def test_provider_list(self):
        """Test all providers are configured."""
        expected_providers = ["openai", "anthropic", "ollama", "groq", "perplexity", "openrouter"]
        for provider in expected_providers:
            self.assertIn(provider, PROVIDERS)
    
    def test_openai_format(self):
        """Test OpenAI format request."""
        messages = [{"role": "user", "content": "test message"}]
        agent = ArubaClawAgent()
        agent.config["llm_provider"] = "openai"
        formatted = agent._format_api_request(messages)
        
        self.assertEqual(formatted["model"], "gpt-4o-mini")
        self.assertEqual(formatted["messages"], messages)
        self.assertEqual(formatted["temperature"], 0.7)
    
    def test_anthropic_format(self):
        """Test Anthropic format request."""
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "test message"}
        ]
        agent = ArubaClawAgent()
        agent.config["llm_provider"] = "anthropic"
        formatted = agent._format_api_request(messages)
        
        self.assertIn("model", formatted)
        self.assertIn("messages", formatted)
        self.assertIn("system", formatted)
    
    def test_groq_format(self):
        """Test Groq format request (OpenAI compatible)."""
        messages = [{"role": "user", "content": "test"}]
        agent = ArubaClawAgent()
        agent.config["llm_provider"] = "groq"
        formatted = agent._format_api_request(messages)
        
        self.assertEqual(formatted["model"], "gpt-4o-mini")  # Default model
        self.assertEqual(formatted["messages"], messages)
    
    def test_perplexity_format(self):
        """Test Perplexity format request."""
        messages = [{"role": "user", "content": "test"}]
        agent = ArubaClawAgent()
        agent.config["llm_provider"] = "perplexity"
        formatted = agent._format_api_request(messages)
        
        self.assertEqual(formatted["messages"], messages)
    
    def test_openrouter_format(self):
        """Test OpenRouter format request."""
        messages = [{"role": "user", "content": "test"}]
        agent = ArubaClawAgent()
        agent.config["llm_provider"] = "openrouter"
        formatted = agent._format_api_request(messages)
        
        self.assertEqual(formatted["messages"], messages)
        self.assertIn("HTTP-Referer", agent._call_llm.__code__.co_names)


class TestChatMethod(unittest.TestCase):
    """Test the chat method."""
    
    @patch("urllib.request.urlopen")
    def test_chat_success(self, mock_urlopen):
        """Test successful chat response."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"choices":[{"message":{"content":"Hello!"}}]}'
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        agent = ArubaClawAgent()
        response = agent.chat("Hello, how are you?")
        
        self.assertEqual(response, "Hello!")
    
    @patch("urllib.request.urlopen")
    def test_chat_error(self, mock_urlopen):
        """Test chat error handling."""
        mock_urlopen.side_effect = Exception("Connection failed")
        
        agent = ArubaClawAgent()
        response = agent.chat("Test message")
        
        self.assertIn("Error", response)


if __name__ == "__main__":
    unittest.main()
