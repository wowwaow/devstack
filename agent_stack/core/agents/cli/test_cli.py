#!/usr/bin/env python3

import unittest
import os
from . import AgentCLI, get_agent_context

class TestAgentCLI(unittest.TestCase):
    def setUp(self):
        self.cli = AgentCLI()
        self.test_agent_id = "test_agent_cli"
    
    def test_agent_registration(self):
        """Test agent registration process."""
        result = self.cli.register(self.test_agent_id, "active")
        self.assertTrue(result['success'], f"Agent registration failed: {result.get('error')}")
    
    def test_agent_context(self):
        """Test agent context functionality."""
        agent = get_agent_context(self.test_agent_id)
        self.assertEqual(agent.agent_id, self.test_agent_id)
        
        # Test heartbeat
        result = agent.heartbeat()
        self.assertTrue(result['success'], f"Heartbeat failed: {result.get('error')}")
        
        # Test status
        result = agent.get_status()
        self.assertTrue(result['success'], f"Status check failed: {result.get('error')}")
    
    def test_task_management(self):
        """Test task creation and assignment."""
        task_id = "test_task_001"
        description = "Test task for CLI testing"
        
        # Create task
        result = self.cli.create_task(task_id, description, self.test_agent_id)
        self.assertTrue(result['success'], f"Task creation failed: {result.get('error')}")
        
        # Assign task
        result = self.cli.assign_task(self.test_agent_id, task_id)
        self.assertTrue(result['success'], f"Task assignment failed: {result.get('error')}")
    
    def test_system_operations(self):
        """Test system-wide operations."""
        # Check system health
        result = self.cli.system_health()
        self.assertTrue(result['success'], f"Health check failed: {result.get('error')}")
        
        # Create backup
        result = self.cli.create_backup("test_backup")
        self.assertTrue(result['success'], f"Backup creation failed: {result.get('error')}")

if __name__ == '__main__':
    unittest.main()

