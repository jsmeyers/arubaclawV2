#!/usr/bin/env python3
"""
scheduled-task.py - Scheduled task example for ArubaClawV2

Demonstrates running scheduled tasks.
"""

from tasks.health_check import run_health_check, format_health_report
from typing import Dict, Any


def main():
    """Run a scheduled health check demo."""
    print("ArubaClawV2 - Scheduled Task Demo")
    print("=" * 40)
    print()
    
    # Run health check
    print("Running health check...")
    print()
    
    results = run_health_check()
    print(results)
    
    print()
    print("Scheduled task demo complete!")


if __name__ == "__main__":
    main()
