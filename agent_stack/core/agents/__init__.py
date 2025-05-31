# Initialize agents package

"""
AI Agent Stack - Core Agent System
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
import uuid

@dataclass
class AgentState:
    """Agent state information"""
    status: str
    current_task: Optional[str]
    progress: int
    last_heartbeat: datetime
    health_status: str
    resource_usage: Dict
    capability_tags: List[str]
    max_concurrent_tasks: int
    current_task_count: int

class Agent:
    """Base Agent class for AI Agent Stack"""
    
    def __init__(self, agent_id: Optional[str] = None):
        self.agent_id = agent_id or f"agent_{uuid.uuid4().hex[:8]}"
        self.state = AgentState(
            status="INITIALIZING",
            current_task=None,
            progress=0,
            last_heartbeat=datetime.utcnow(),
            health_status="UNKNOWN",
            resource_usage={},
            capability_tags=[],
            max_concurrent_tasks=1,
            current_task_count=0
        )
        
    def initialize(self):
        """Initialize the agent"""
        self._register_agent()
        self._setup_heartbeat()
        self._load_capabilities()
        self.state.status = "IDLE"
        self.state.health_status = "HEALTHY"
        
    def _register_agent(self):
        """Register agent with the system"""
        from agent_stack.core.registry import AgentRegistry
        AgentRegistry.register_agent(self)
        
    def _setup_heartbeat(self):
        """Setup agent heartbeat monitoring"""
        from agent_stack.core.monitoring import HeartbeatMonitor
        HeartbeatMonitor.initialize_agent(self.agent_id)
        
    def _load_capabilities(self):
        """Load agent capabilities"""
        # Load from configuration or determine dynamically
        self.state.capability_tags = ["basic_tasks", "communication"]
        
    def send_heartbeat(self):
        """Send agent heartbeat"""
        from agent_stack.core.monitoring import HeartbeatMonitor
        self.state.last_heartbeat = datetime.utcnow()
        HeartbeatMonitor.update_heartbeat(
            self.agent_id,
            self.state
        )
        
    def request_task(self):
        """Request a new task from the task pool"""
        from agent_stack.core.task_pool import TaskPool
        if self.state.current_task_count >= self.state.max_concurrent_tasks:
            return None
        
        task = TaskPool.get_task(
            agent_id=self.agent_id,
            capabilities=self.state.capability_tags
        )
        
        if task:
            self.state.current_task = task.task_id
            self.state.current_task_count += 1
            self.state.status = "WORKING"
        
        return task
        
    def update_status(self, status: str, progress: int, current_task: Optional[str] = None):
        """Update agent status"""
        self.state.status = status
        self.state.progress = progress
        if current_task:
            self.state.current_task = current_task
        self.send_heartbeat()
        
    def complete_task(self, task_id: str):
        """Mark a task as completed"""
        from agent_stack.core.task_pool import TaskPool
        if task_id == self.state.current_task:
            TaskPool.complete_task(task_id, self.agent_id)
            self.state.current_task = None
            self.state.current_task_count -= 1
            self.state.progress = 0
            if self.state.current_task_count == 0:
                self.state.status = "IDLE"
            self.send_heartbeat()
            
    def shutdown(self):
        """Shutdown the agent"""
        from agent_stack.core.registry import AgentRegistry
        self.state.status = "SHUTTING_DOWN"
        self.send_heartbeat()
        
        # Handle any incomplete tasks
        if self.state.current_task:
            from agent_stack.core.task_pool import TaskPool
            TaskPool.reassign_task(self.state.current_task)
            
        AgentRegistry.deregister_agent(self.agent_id)
        self.state.status = "SHUTDOWN"
        self.send_heartbeat()
