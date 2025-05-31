# Initialize agents package

"""
AI Agent Stack - Core Agent System
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Union
import json
import logging
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@dataclass
class AgentComment:
    """Represents a structured agent progress comment"""
    timestamp: datetime
    action: str
    details: str
    status: str
    metadata: Optional[Dict] = None

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
    comments: List[AgentComment]  # Track progress comments

class Agent:
    """Base Agent class for AI Agent Stack"""
    
    def __init__(self, agent_id: Optional[str] = None):
        self.agent_id = agent_id or f"agent_{uuid.uuid4().hex[:8]}"
        self.logger = logging.getLogger(f"agent.{self.agent_id}")
        self.state = AgentState(
            status="INITIALIZING",
            current_task=None,
            progress=0,
            last_heartbeat=datetime.utcnow(),
            health_status="UNKNOWN",
            resource_usage={},
            capability_tags=[],
            max_concurrent_tasks=1,
            current_task_count=0,
            comments=[]  # Initialize empty comments list
        )

    def add_comment(self, action: str, details: str, status: str, metadata: Optional[Dict] = None) -> AgentComment:
        """
        Add a progress comment with consistent formatting.
        
        Args:
            action: The action being performed
            details: Detailed description of the progress
            status: Current status (e.g., "started", "completed", "failed")
            metadata: Optional additional structured data
        
        Returns:
            The created AgentComment object
        """
        comment = AgentComment(
            timestamp=datetime.utcnow(),
            action=action,
            details=details,
            status=status,
            metadata=metadata
        )
        self.state.comments.append(comment)
        
        # Log the comment
        self.logger.info(
            f"AGENT[{self.agent_id}] {action}: {details} (Status: {status})"
        )
        
        # Store in version control compatible format
        with open(f"agent_stack/logs/work_logs/{self.agent_id}_progress.log", "a") as f:
            json.dump({
                "timestamp": comment.timestamp.isoformat(),
                "agent_id": self.agent_id,
                "action": action,
                "details": details,
                "status": status,
                "metadata": metadata
            }, f)
            f.write("\n")
            
        return comment
        
    def initialize(self):
        """Initialize the agent"""
        self.add_comment("initialization", "Starting agent initialization", "started")
        
        self._register_agent()
        self.add_comment("registration", "Agent registered with system", "completed")
        
        self._setup_heartbeat()
        self.add_comment("heartbeat", "Heartbeat monitoring established", "completed")
        
        self._load_capabilities()
        self.add_comment("capabilities", f"Loaded capabilities: {', '.join(self.state.capability_tags)}", "completed")
        
        self.state.status = "IDLE"
        self.state.health_status = "HEALTHY"
        
        self.add_comment("initialization", "Agent initialization completed successfully", "completed", {
            "status": self.state.status,
            "health": self.state.health_status,
            "capabilities": self.state.capability_tags
        })
        
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
        self.add_comment("task_request", "Requesting new task from pool", "started")
        
        from agent_stack.core.task_pool import TaskPool
        if self.state.current_task_count >= self.state.max_concurrent_tasks:
            self.add_comment("task_request", 
                           f"Task request denied - at maximum capacity ({self.state.current_task_count}/{self.state.max_concurrent_tasks})", 
                           "failed")
            return None
        
        self.add_comment("task_request", "Searching for compatible task", "in_progress", {
            "capabilities": self.state.capability_tags
        })
        
        task = TaskPool.get_task(
            agent_id=self.agent_id,
            capabilities=self.state.capability_tags
        )
        
        if task:
            self.state.current_task = task.task_id
            self.state.current_task_count += 1
            self.state.status = "WORKING"
            self.add_comment("task_request", f"Task {task.task_id} assigned successfully", "completed", {
                "task_id": task.task_id,
                "task_type": task.type if hasattr(task, 'type') else None
            })
        else:
            self.add_comment("task_request", "No compatible tasks found in pool", "completed")
        
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
        self.add_comment("task_completion", f"Starting completion process for task {task_id}", "started")
        
        from agent_stack.core.task_pool import TaskPool
        if task_id == self.state.current_task:
            self.add_comment("task_completion", "Finalizing task results", "in_progress")
            TaskPool.complete_task(task_id, self.agent_id)
            
            self.state.current_task = None
            self.state.current_task_count -= 1
            self.state.progress = 0
            
            if self.state.current_task_count == 0:
                self.state.status = "IDLE"
                self.add_comment("status_update", "Agent returned to IDLE state", "completed")
            
            self.send_heartbeat()
            self.add_comment("task_completion", f"Task {task_id} completed successfully", "completed", {
                "remaining_tasks": self.state.current_task_count,
                "status": self.state.status
            })
        else:
            self.add_comment("task_completion", 
                           f"Failed to complete task {task_id} - not currently assigned", 
                           "failed")
            
    def shutdown(self):
        """Shutdown the agent"""
        self.add_comment("shutdown", "Initiating agent shutdown sequence", "started")
        
        from agent_stack.core.registry import AgentRegistry
        self.state.status = "SHUTTING_DOWN"
        self.send_heartbeat()
        
        # Handle any incomplete tasks
        if self.state.current_task:
            self.add_comment("shutdown", 
                           f"Reassigning active task {self.state.current_task}", 
                           "in_progress")
            from agent_stack.core.task_pool import TaskPool
            TaskPool.reassign_task(self.state.current_task)
            self.add_comment("task_handoff", 
                           f"Task {self.state.current_task} reassigned to task pool", 
                           "completed")
            
        self.add_comment("shutdown", "Deregistering agent from system", "in_progress")
        AgentRegistry.deregister_agent(self.agent_id)
        
        self.state.status = "SHUTDOWN"
        self.send_heartbeat()
        
        self.add_comment("shutdown", "Agent shutdown completed successfully", "completed", {
            "final_status": self.state.status,
            "tasks_reassigned": 1 if self.state.current_task else 0
        })
