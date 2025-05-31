"""
AI Agent Stack - Monitoring System
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import threading
import time

class HeartbeatMonitor:
    """System-wide agent heartbeat monitoring"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(HeartbeatMonitor, cls).__new__(cls)
                    cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the heartbeat monitor"""
        self.agent_heartbeats = {}
        self.monitoring_config = {
            "scan_interval_seconds": 30,
            "soft_timeout_minutes": 5,
            "hard_timeout_minutes": 10,
            "critical_timeout_minutes": 15,
            "max_missed_heartbeats": 5,
            "auto_reassignment_enabled": True
        }
        self._start_monitoring()
        
    def _start_monitoring(self):
        """Start the background monitoring thread"""
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            daemon=True
        )
        self.monitor_thread.start()
        
    def _monitor_loop(self):
        """Main monitoring loop"""
        while True:
            self._check_heartbeats()
            time.sleep(self.monitoring_config["scan_interval_seconds"])
            
    def _check_heartbeats(self):
        """Check all agent heartbeats"""
        current_time = datetime.utcnow()
        timeout_events = []
        
        for agent_id, heartbeat in self.agent_heartbeats.items():
            last_heartbeat = heartbeat["last_heartbeat"]
            time_since_heartbeat = (current_time - last_heartbeat).total_seconds() / 60
            
            # Check for timeouts
            if time_since_heartbeat > self.monitoring_config["soft_timeout_minutes"]:
                self._handle_soft_timeout(agent_id, time_since_heartbeat)
                
            if time_since_heartbeat > self.monitoring_config["hard_timeout_minutes"]:
                self._handle_hard_timeout(agent_id, time_since_heartbeat)
                
            if time_since_heartbeat > self.monitoring_config["critical_timeout_minutes"]:
                self._handle_critical_timeout(agent_id, time_since_heartbeat)
                
    def _handle_soft_timeout(self, agent_id: str, timeout_duration: float):
        """Handle soft timeout"""
        from agent_stack.core.logging import SystemLogger
        
        SystemLogger.warning(
            f"Agent soft timeout: {agent_id}",
            extra={
                "agent_id": agent_id,
                "timeout_duration": timeout_duration,
                "timeout_type": "SOFT"
            }
        )
        
        # Send ping request to agent
        self._ping_agent(agent_id)
        
    def _handle_hard_timeout(self, agent_id: str, timeout_duration: float):
        """Handle hard timeout"""
        from agent_stack.core.logging import SystemLogger
        from agent_stack.core.task_pool import TaskPool
        
        SystemLogger.error(
            f"Agent hard timeout: {agent_id}",
            extra={
                "agent_id": agent_id,
                "timeout_duration": timeout_duration,
                "timeout_type": "HARD"
            }
        )
        
        # Get agent's current tasks
        agent_tasks = TaskPool.get_agent_tasks(agent_id)
        
        if self.monitoring_config["auto_reassignment_enabled"]:
            for task in agent_tasks:
                TaskPool.reassign_task(task.task_id)
                
    def _handle_critical_timeout(self, agent_id: str, timeout_duration: float):
        """Handle critical timeout"""
        from agent_stack.core.logging import SystemLogger
        from agent_stack.core.registry import AgentRegistry
        
        SystemLogger.critical(
            f"Agent critical timeout: {agent_id}",
            extra={
                "agent_id": agent_id,
                "timeout_duration": timeout_duration,
                "timeout_type": "CRITICAL"
            }
        )
        
        # Mark agent as failed
        AgentRegistry.mark_agent_failed(agent_id)
        
        # Notify system administrators
        self._escalate_to_supervisor(agent_id, "CRITICAL_TIMEOUT")
        
    def _ping_agent(self, agent_id: str):
        """Attempt to ping an agent"""
        # Implementation depends on agent communication method
        pass
        
    def _escalate_to_supervisor(self, agent_id: str, reason: str):
        """Escalate issues to system supervisor"""
        from agent_stack.core.supervisor import SystemSupervisor
        
        SystemSupervisor.escalate_issue(
            agent_id=agent_id,
            reason=reason,
            severity="CRITICAL"
        )
        
    @classmethod
    def initialize_agent(cls, agent_id: str):
        """Initialize monitoring for a new agent"""
        instance = cls()
        instance.agent_heartbeats[agent_id] = {
            "last_heartbeat": datetime.utcnow(),
            "status": "INITIALIZING",
            "health_status": "UNKNOWN"
        }
        
    @classmethod
    def update_heartbeat(cls, agent_id: str, agent_state: Dict):
        """Update agent heartbeat"""
        instance = cls()
        instance.agent_heartbeats[agent_id] = {
            "last_heartbeat": datetime.utcnow(),
            "status": agent_state.status,
            "health_status": agent_state.health_status,
            "current_task": agent_state.current_task,
            "progress": agent_state.progress,
            "resource_usage": agent_state.resource_usage
        }
        
    @classmethod
    def get_agent_status(cls, agent_id: str) -> Optional[Dict]:
        """Get current status of an agent"""
        instance = cls()
        return instance.agent_heartbeats.get(agent_id)
        
    @classmethod
    def get_system_health(cls) -> Dict:
        """Get overall system health status"""
        instance = cls()
        current_time = datetime.utcnow()
        
        total_agents = len(instance.agent_heartbeats)
        agents_in_timeout = 0
        healthy_agents = 0
        
        for heartbeat in instance.agent_heartbeats.values():
            time_since_heartbeat = (current_time - heartbeat["last_heartbeat"]).total_seconds() / 60
            
            if time_since_heartbeat > instance.monitoring_config["soft_timeout_minutes"]:
                agents_in_timeout += 1
            if heartbeat["health_status"] == "HEALTHY":
                healthy_agents += 1
                
        return {
            "total_agents": total_agents,
            "agents_in_timeout": agents_in_timeout,
            "healthy_agents": healthy_agents,
            "health_percentage": (healthy_agents / total_agents * 100) if total_agents > 0 else 0
        }
