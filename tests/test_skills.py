#!/usr/bin/env python3
"""
test_skills.py - Tests for ArubaClawV2 skills
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestNetworkSkills(unittest.TestCase):
    """Test network automation skills."""
    
    def test_show_bgp(self):
        """Test BGP neighbor display."""
        from skills.network import show_bgp
        response = show_bgp()
        self.assertIn("BGP", response)
        self.assertIn("Neighbors", response)
    
    def test_show_bgp_neighbor(self):
        """Test specific BGP neighbor display."""
        from skills.network import show_bgp
        response = show_bgp(neighborip="10.1.1.1")
        self.assertIn("10.1.1.1", response)
    
    def test_show_vlan(self):
        """Test VLAN display."""
        from skills.network import show_vlan
        response = show_vlan()
        self.assertIn("VLAN", response)
        self.assertIn("Information", response)
    
    def test_show_vlan_id(self):
        """Test specific VLAN display."""
        from skills.network import show_vlan
        response = show_vlan(vlanid=10)
        self.assertIn("10", response)
    
    def test_show_interface(self):
        """Test interface display."""
        from skills.network import show_interface
        response = show_interface()
        self.assertIn("Interface", response)
        self.assertIn("Status", response)
    
    def test_show_stp(self):
        """Test STP display."""
        from skills.network import show_stp
        response = show_stp()
        self.assertIn("STP", response)
        self.assertIn("Information", response)
    
    def test_show_arp(self):
        """Test ARP table display."""
        from skills.network import show_arp
        response = show_arp()
        self.assertIn("ARP", response)
        self.assertIn("Table", response)


class TestSystemSkills(unittest.TestCase):
    """Test system information skills."""
    
    def test_show_version(self):
        """Test version display."""
        from skills.system import show_version
        response = show_version()
        self.assertIn("Version", response)
        self.assertIn("Aruba CX", response)
    
    def test_show_cpu(self):
        """Test CPU display."""
        from skills.system import show_cpu
        response = show_cpu()
        self.assertIn("CPU", response)
        self.assertIn("Utilization", response)
    
    def test_show_memory(self):
        """Test memory display."""
        from skills.system import show_memory
        response = show_memory()
        self.assertIn("Memory", response)
        self.assertIn("Utilization", response)
    
    def test_show_temperature(self):
        """Test temperature display."""
        from skills.system import show_temperature
        response = show_temperature()
        self.assertIn("Temperature", response)
        self.assertIn("Sensors", response)
    
    def test_show_power(self):
        """Test power display."""
        from skills.system import show_power
        response = show_power()
        self.assertIn("Power", response)
        self.assertIn("Supplies", response)
    
    def test_show_fans(self):
        """Test fans display."""
        from skills.system import show_fans
        response = show_fans()
        self.assertIn("Fans", response)
    
    def test_show_uptime(self):
        """Test uptime display."""
        from skills.system import show_uptime
        response = show_uptime()
        self.assertIn("Uptime", response)
        self.assertIn("Time", response)


if __name__ == "__main__":
    unittest.main()
