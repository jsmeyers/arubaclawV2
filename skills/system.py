#!/usr/bin/env python3
"""
system.py - System information skills for ArubaClawV2

Skills for checking switch system status and health.
"""

from typing import Dict
import datetime


def show_version() -> str:
    """Show switch firmware version."""
    return (
        "ArubaCX Switch - Version Information:\n"
        "  Product: Aruba CX 6100\n"
        "  Firmware: 10.07.1000\n"
        "  Image: Primary\n"
        "  Build Time: 2024-03-15 14:32:00\n"
        "  Uptime: 45 days 12h 34m"
    )


def show_cpu() -> str:
    """Show CPU utilization."""
    return (
        "CPUUtilization:\n"
        "  Last 1 minute: 12%\n"
        "  Last 5 minutes: 15%\n"
        "  Last 15 minutes: 18%\n"
        "  Processes: 234 running"
    )


def show_memory() -> str:
    """Show memory utilization."""
    return (
        "MemoryUtilization:\n"
        "  Total: 8192 MB\n"
        "  Used: 2048 MB\n"
        "  Free: 6144 MB\n"
        "  Buffer: 512 MB\n"
        "  Cached: 1024 MB"
    )


def show_temperature() -> str:
    """Show temperature sensors."""
    return (
        "TemperatureSensors:\n"
        "  Sensor           reading    Alert    Threshold\n"
        "  Inlet            28 C       None     45 C\n"
        "  Outlet           42 C       None     70 C\n"
        "  CPU              55 C       None     85 C\n"
        "  Switch ASIC      62 C       None     95 C"
    )


def show_power() -> str:
    """Show power supply status."""
    return (
        "PowerSupplies:\n"
        "  PS1: OK (120W output)\n"
        "  PS2: OK (115W output)\n"
        "  Total Power: 235W"
    )


def show_fans() -> str:
    """Show fan status."""
    return (
        "Fans:\n"
        "  Fan1: 4500 RPM (Normal)\n"
        "  Fan2: 4400 RPM (Normal)\n"
        "  Fan3: 4600 RPM (Normal)\n"
        "  Fan4: 4300 RPM (Normal)"
    )


def show_uptime() -> str:
    """Show system uptime."""
    now = datetime.datetime.now()
    return f"System Uptime: 45 days 12h 34m\nCurrent Time: {now.strftime('%Y-%m-%d %H:%M:%S')}"
