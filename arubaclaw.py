#!/usr/bin/env python3
"""
arubaclaw.py - Nanobot-inspired agent for Aruba CX 6100 switches

Ultra-lightweight AI agent with OpenClaw-style capabilities.
Python 3.12+ runtime, stdlib only (no external dependencies).

Author: jsmeyers
License: MIT
"""

import os
import sys
import json
import ssl
import urllib.request
import urllib.error
import hashlib
import datetime
import uuid
from typing import List, Dict, Optional, Any
from pathlib import Path

# Constants
VERSION = "0.1.0"
DEFAULT_CONFIG = {
    "llm_provider": "openai",
    "llm_model": "gpt-4o-mini",
    "api_key": "",
    "api_timeout": 30,
    "temperature": 0.7,
    "workspace": "~/.arubaclaw/workspace"
}

# Provider configurations
PROVIDERS = {
    "openai": {
        "endpoint": "https://api.openai.com/v1/chat/completions",
        "format": "openai",
        "required": ["api_key"]
    },
    "anthropic": {
        "endpoint": "https://api.anthropic.com/v1/messages",
        "format": "anthropic",
        "required": ["api_key"]
    },
    "ollama": {
        "endpoint": "http://localhost:11434/api/chat",
        "format": "openai",
        "required": []
    },
    "groq": {
        "endpoint": "https://api.groq.com/openai/v1/chat/completions",
        "format": "openai",
        "required": ["api_key"]
    },
    "perplexity": {
        "endpoint": "https://api.perplexity.ai/chat/completions",
        "format": "openai",
        "required": ["api_key"]
    },
    "openrouter": {
        "endpoint": "https://openrouter.ai/api/v1/chat/completions",
        "format": "openai",
        "required": ["api_key"]
    }
}

# Supported models per provider
SUPPORTED_MODELS = {
    "openai": {"gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo", "gpt-4-turbo"},
    "anthropic": {"claude-3-5-sonnet", "claude-3-opus", "claude-3-haiku"},
    "ollama": {"llama3", "mistral", "codellama", "phi3"},
    "groq": {"llama3-70b", "llama3-8b", "mixtral-8x7b"},
    "perplexity": {"llama-3-70b-instruct", "llama-3-8b-instruct", "sonar-pro"},
    "openrouter": {"auto"}
}


class ArubaClawAgent:
    """Core agent class for Aruba CX switches."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the agent with configuration."""
        self.config = self._load_config(config_path)
        self.workspace = Path(self.config["workspace"]).expanduser()
        self.state = self._load_state()
        self.history = self.state.get("history", [])
        
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        config = DEFAULT_CONFIG.copy()
        
        # Try environment variables first
        if os.environ.get("ARUBACLAW_API_KEY"):
            config["api_key"] = os.environ.get("ARUBACLAW_API_KEY")
        if os.environ.get("ARUBACLAW_PROVIDER"):
            config["llm_provider"] = os.environ.get("ARUBACLOW_PROVIDER")
        if os.environ.get("ARUBACLAW_MODEL"):
            config["llm_model"] = os.environ.get("ARUBACLAW_MODEL")
        if os.environ.get("ARUBACLAW_TIMEOUT"):
            try:
                config["api_timeout"] = int(os.environ.get("ARUBACLAW_TIMEOUT"))
            except ValueError:
                pass
        
        # Try config file
        if config_path:
            try:
                with open(config_path, "r") as f:
                    file_config = json.load(f)
                    config.update(file_config)
            except (FileNotFoundError, json.JSONDecodeError):
                pass
        
        # Validate provider
        if config["llm_provider"] not in PROVIDERS:
            config["llm_provider"] = "openai"
        
        return config
    
    def _load_state(self) -> Dict[str, Any]:
        """Load agent state from workspace."""
        state_file = self.workspace / "state.json"
        if state_file.exists():
            try:
                with open(state_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass
        return {"id": str(uuid.uuid4()), "history": [], "created": datetime.datetime.now().isoformat()}
    
    def _save_state(self):
        """Save agent state to workspace."""
        self.state["history"] = self.history[-100:]  # Keep last 100 messages
        state_file = self.workspace / "state.json"
        state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(state_file, "w") as f:
            json.dump(self.state, f, indent=2)
    
    def _build_messages(self, user_message: str) -> List[Dict[str, str]]:
        """Build message history for LLM."""
        messages = []
        
        # System prompt
        messages.append({
            "role": "system",
            "content": self._get_system_prompt()
        })
        
        # Add conversation history
        for msg in self.history[-8:]:  # Last 8 messages
            messages.append(msg)
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        return messages
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for the agent."""
        return (
            "You are ArubaClaw, an AI assistant specialized for Aruba CX network switches. "
            "You can help with network configuration, troubleshooting, and automation. "
            "Be concise and provide actionable information."
        )
    
    def _format_api_request(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Format request for specific provider."""
        provider = PROVIDERS[self.config["llm_provider"]]
        fmt = provider["format"]
        
        if fmt == "anthropic":
            # Convert OpenAI format to Anthropic format
            return {
                "model": self.config["llm_model"],
                "messages": [
                    {"role": m["role"], "content": m["content"]}
                    for m in messages if m["role"] != "system"
                ],
                "system": next((m["content"] for m in messages if m["role"] == "system"), None),
                "temperature": self.config["temperature"],
                "max_tokens": 4096
            }
        else:  # OpenAI format
            return {
                "model": self.config["llm_model"],
                "messages": messages,
                "temperature": self.config["temperature"],
                "max_tokens": 4096
            }
    
    def _call_llm(self, formatted_request: Dict[str, Any]) -> Optional[str]:
        """Make API call to LLM provider."""
        provider = PROVIDERS[self.config["llm_provider"]]
        endpoint = provider["endpoint"]
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Add provider-specific headers
        if self.config["llm_provider"] == "anthropic":
            headers["x-api-key"] = self.config["api_key"]
            headers["anthropic-version"] = "2023-06-01"
        elif self.config["llm_provider"] == "openai":
            headers["Authorization"] = f"Bearer {self.config['api_key']}"
        elif self.config["llm_provider"] == "groq":
            headers["Authorization"] = f"Bearer {self.config['api_key']}"
        elif self.config["llm_provider"] == "perplexity":
            headers["Authorization"] = f"Bearer {self.config['api_key']}"
        elif self.config["llm_provider"] == "openrouter":
            headers["Authorization"] = f"Bearer {self.config['api_key']}"
            headers["HTTP-Referer"] = "https://github.com/jsmeyers/arubaclawV2"
        
        try:
            data = json.dumps(formatted_request).encode("utf-8")
            req = urllib.request.Request(endpoint, data=data, headers=headers)
            
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            with urllib.request.urlopen(req, timeout=self.config["api_timeout"], context=ctx) as response:
                result = json.loads(response.read().decode("utf-8"))
                
                # Extract response based on provider format
                if self.config["llm_provider"] == "anthropic":
                    return result.get("content", [{}])[0].get("text", "")
                else:
                    return result.get("choices", [{}])[0].get("message", {}).get("content", "")
                    
        except urllib.error.HTTPError as e:
            print(f"API error: {e.code} - {e.reason}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def chat(self, message: str) -> str:
        """Send a message and get response."""
        # Build message history
        messages = self._build_messages(message)
        
        # Format for API
        formatted = self._format_api_request(messages)
        
        # Call LLM
        response = self._call_llm(formatted)
        
        if response:
            # Update history
            self.history.append({"role": "user", "content": message})
            self.history.append({"role": "assistant", "content": response})
            self._save_state()
            
            return response
        else:
            return "Error: Could not get response from LLM. Check your API key and provider configuration."
    
    def execute_task(self, task_name: str, **kwargs) -> str:
        """Execute a skill/task."""
        # Import skills dynamically
        try:
            from skills.network import show_bgp, show_vlan, show_interface
            skills = {
                "show_bgp": show_bgp,
                "show_vlan": show_vlan,
                "show_interface": show_interface
            }
            
            if task_name in skills:
                return skills[task_name](**kwargs)
            else:
                return f"Error: Task '{task_name}' not found. Available tasks: {list(skills.keys())}"
        except ImportError:
            return "Error: Skills not loaded. skills/ directory missing or incomplete."
    
    def web_search(self, query: str, count: int = 5) -> List[Dict[str, str]]:
        """Search the web using Brave API."""
        if not self.config["api_key"]:
            return [{"title": "Demo mode", "url": "https://brave.com/search/", "description": "API key not configured. Show search results here."}]
        
        # Use Brave Search API
        # This is a placeholder - implement with actual API
        return [{"title": f"Demo result: {query}", "url": "https://brave.com/search/", "description": "Implement Brave Search API integration"}]


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="ArubaClaw - Agent for Aruba CX switches")
    parser.add_argument("-c", "--config", help="Path to config file")
    parser.add_argument("-m", "--message", help="Send a single message")
    parser.add_argument("--test", action="store_true", help="Run test mode")
    parser.add_argument("--cli", action="store_true", help="Start interactive CLI")
    args = parser.parse_args()
    
    agent = ArubaClawAgent(config_path=args.config)
    
    if args.test:
        # Test mode - no API key required
        print("ArubaClaw Test Mode")
        print(f"Version: {VERSION}")
        print(f"Provider: {agent.config['llm_provider']}")
        print(f"Model: {agent.config['llm_model']}")
        print(f"Workspace: {agent.workspace}")
        
        # Test chat with simulated response
        response = agent.chat("Hello, ArubaClaw!")
        print(f"Response: {response}")
        
    elif args.message:
        # Single message mode
        response = agent.chat(args.message)
        print(response)
        
    elif args.cli:
        # Interactive CLI
        print(f"ArubaClaw {VERSION} - Interactive CLI")
        print(f"Type 'quit' or 'exit' to leave")
        print()
        
        while True:
            try:
                user_input = input(">>> ").strip()
                if user_input.lower() in ("quit", "exit"):
                    break
                if not user_input:
                    continue
                response = agent.chat(user_input)
                print(response)
            except KeyboardInterrupt:
                break
            except EOFError:
                break
        
        print("Goodbye!")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
