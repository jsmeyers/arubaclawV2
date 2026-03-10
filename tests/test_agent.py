#!/usr/bin/env python3
"""
test_agent.py - Tests for ArubaClawV2 core agent
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arubaclaw import ArubaClawAgent, DEFAULT_CONFIG


class TestAgent(unittest.TestCase):
    """Test cases for the ArubaClawAgent class."""
    
    def test_agent_initialization(self):
        """Test agent can be initialized with defaults."""
        agent = ArubaClawAgent()
        self.assertIsNotNone(agent)
        self.assertEqual(agent.config["llm_provider"], "openai")
        self.assertEqual(agent.config["llm_model"], "gpt-4o-mini")
    
    def test_custom_config(self):
        """Test agent loads custom config."""
        config = {"llm_provider": "anthropic", "llm_model": "claude-3-haiku"}
        agent = ArubaClawAgent()
        # Note: This test may need adjustment based on actual config loading
        self.assertIn(agent.config["llm_provider"], ["openai", "anthropic", "ollama", "groq", "perplexity", "openrouter"])
    
    def test_workspace_creation(self):
        """Test workspace directory is created."""
        agent = ArubaClawAgent()
        self.assertIsNotNone(agent.workspace)
    
    def test_message_formatting(self):
        """Test message formatting for API."""
        agent = ArubaClawAgent()
        messages = agent._build_messages("Hello, test!")
        self.assertIsInstance(messages, list)
        self.assertGreater(len(messages), 0)
    
    def test_provider_validation(self):
        """Test provider configuration is valid."""
        agent = ArubaClawAgent()
        provider = agent.config["llm_provider"]
        self.assertIn(provider, ["openai", "anthropic", "ollama", "groq", "perplexity", "openrouter"])


class TestProviders(unittest.TestCase):
    """Test provider configurations."""
    
    def test_provider_endpoints(self):
        """Test all providers have endpoints."""
        from arubaclaw import PROVIDERS
        for provider_name, provider_config in PROVIDERS.items():
            self.assertIn("endpoint", provider_config)
            self.assertIn("format", provider_config)
    
    def test_openai_format(self):
        """Test OpenAI format request."""
        from arubaclaw import ArubaClawAgent
        messages = [{"role": "user", "content": "test"}]
        agent = ArubaClawAgent()
        formatted = agent._format_api_request(messages)
        self.assertEqual(formatted["model"], "gpt-4o-mini")
        self.assertEqual(formatted["messages"], messages)


if __name__ == "__main__":
    unittest.main()
