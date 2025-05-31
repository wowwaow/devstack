"""Agent-related type definitions."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List

from agent_stack.core.types.base import AgentID
from agent_stack.core.types.task import Task

class AgentCapability(Enum):
    """Enumeration of possible agent capabilities."""
    TASK_PROCESSING = "task_processing"
    RESOURCE_MANAGEMENT = "resource_management"
    HEALTH_MONITORING = "health_monitoring"
    OBJECTIVE_PROMOTION = "objective_promotion"

@dataclass
class AgentMetadata:
    """Metadata associated with an agent."""
    created_at: datetime
    last_heartbeat: datetime
    capabilities: List[AgentCapability]
    status: str
    version: str

class BaseAgent(ABC):
    """Abstract base class for all agents in the system.
    
    Provides common interface and functionality that all agents must implement.
    """
    
    def __init__(self, agent_id: AgentID, metadata: AgentMetadata) -> None:
        """Initialize the base agent.
        
        Args:
            agent_id: Unique identifier for the agent
            metadata: Agent metadata containing capabilities and status
        """
        self.agent_id = agent_id
        self.metadata = metadata
    
    @abstractmethod
    async def process_task(self, task: Task) -> Task:
        """Process a task assigned to this agent.
        
        Args:
            task: The task to be processed
            
        Returns:
            The processed task with updated status and results
        """
        pass
    
    @abstractmethod
    async def heartbeat(self) -> bool:
        """Send a heartbeat signal to indicate agent health.
        
        Returns:
            True if heartbeat was successful, False otherwise
        """
        pass

