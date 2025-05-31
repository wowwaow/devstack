#!/usr/bin/env python3

import unittest
import os
import sys
from pathlib import Path
import subprocess

# Add the parent directory to Python path for imports
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from agent_stack.core.agents.cli import AgentCLI, get_agent_context

class TestAgentCLI(unittest.TestCase):
    def setUp(self):
        self.cli = AgentCLI()
        self.test_agent_id = "test_agent_cli"
        
        # Verify warp_system.sh exists and is executable
        self.assertTrue(os.path.exists(self.cli.warp_system), 
                       f"warp_system.sh not found at {self.cli.warp_system}")
        self.assertTrue(os.access(self.cli.warp_system, os.X_OK),
                       f"warp_system.sh is not executable at {self.cli.warp_system}")
        
        # Print script contents for debugging
        try:
            with open(self.cli.warp_system, 'r') as f:
                print(f"\nwarp_system.sh contents:\n{f.read()}\n")
        except Exception as e:
            print(f"Error reading warp_system.sh: {e}")
    
    def test_agent_registration(self):
        """Test agent registration process."""
        result = self.cli.register(self.test_agent_id, "active")
        print(f"\nRegistration result: {result}")
        self.assertTrue(result['success'], 
                       f"Agent registration failed: {result.get('error')}\nOutput: {result.get('output')}")
    
    def test_agent_context(self):
        """Test agent context functionality."""
        agent = get_agent_context(self.test_agent_id)
        self.assertEqual(agent.agent_id, self.test_agent_id)
        
        # Test heartbeat
        result = agent.heartbeat()
        print(f"\nHeartbeat result: {result}")
        self.assertTrue(result['success'], 
                       f"Heartbeat failed: {result.get('error')}\nOutput: {result.get('output')}")
        
        # Test status
        result = agent.get_status()
        print(f"\nStatus result: {result}")
        self.assertTrue(result['success'], 
                       f"Status check failed: {result.get('error')}\nOutput: {result.get('output')}")
    
    def test_task_management(self):
        """Test task creation and assignment."""
        task_id = "test_task_001"
        description = "Test task for CLI testing"
        
        # Create task
        result = self.cli.create_task(task_id, description, self.test_agent_id)
        print(f"\nTask creation result: {result}")
        self.assertTrue(result['success'], 
                       f"Task creation failed: {result.get('error')}\nOutput: {result.get('output')}")
        
        # Assign task
        result = self.cli.assign_task(self.test_agent_id, task_id)
        print(f"\nTask assignment result: {result}")
        self.assertTrue(result['success'], 
                       f"Task assignment failed: {result.get('error')}\nOutput: {result.get('output')}")
    
    def test_system_operations(self):
        """Test system-wide operations."""
        # Check system health
        result = self.cli.system_health()
        print(f"\nHealth check result: {result}")
        self.assertTrue(result['success'], 
                       f"Health check failed: {result.get('error')}\nOutput: {result.get('output')}")
        
        # Create backup
        result = self.cli.create_backup("test_backup")
        print(f"\nBackup creation result: {result}")
        self.assertTrue(result['success'], 
                       f"Backup creation failed: {result.get('error')}\nOutput: {result.get('output')}")

if __name__ == '__main__':
    unittest.main(verbosity=2)

