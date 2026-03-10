#!/usr/bin/env python3
"""
simple-chat.py - Simple chat example for ArubaClawV2

Demonstrates basic agent usage.
"""

from arubaclaw import ArubaClawAgent


def main():
    """Run a simple chat demo."""
    print("ArubaClawV2 - Simple Chat Demo")
    print("=" * 40)
    print()
    
    # Initialize agent (demo mode - no API key required)
    agent = ArubaClawAgent()
    
    # Send a message
    response = agent.chat("Hello, ArubaClaw! What can you do?")
    print(f"User: Hello, ArubaClaw! What can you do?")
    print(f"Agent: {response}")
    print()
    
    # Show available skills
    response = agent.chat("Show me the available skills")
    print(f"User: Show me the available skills")
    print(f"Agent: {response}")
    print()
    
    print("Demo complete!")


if __name__ == "__main__":
    main()
