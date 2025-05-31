"""Core type definitions for the AI Agent Stack.

This module provides shared type definitions and base classes used throughout
the agent system. It ensures type safety and consistent interfaces across
different components.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, TypeVar, Union
from uuid import UUID

# Type variables for generic type hints
T = TypeVar('T')
AgentID = str
TaskID = UUID

class TaskStatus(Enum):
    """Enumeration of possible task states in the system."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskPriority(Enum):
    """Enumeration of task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class TaskMetadata:
    """Metadata associated with a task."""
    created_at: datetime
    updated_at: datetime
    agent_id: Optional[AgentID] = None
    retries: int = 0
    timeout_seconds: int = 3600

@dataclass
class Task:
    """Represents a task in the agent system."""
    id: TaskID
    type: str
    priority: TaskPriority
    status: TaskStatus
    metadata: TaskMetadata
    parameters: Dict[str, any]
    result: Optional[Dict[str, any]] = None
    error: Optional[str] = None

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

class AgentComment:
    """Represents a comment made by an agent on a file or code block."""
    
    def __init__(
        self,
        agent_id: AgentID,
        file_path: str,
        comment: str,
        line_number: Optional[int] = None,
        timestamp: Optional[datetime] = None
    ) -> None:
        """Initialize an agent comment.
        
        Args:
            agent_id: ID of the agent making the comment
            file_path: Path to the file being commented on
            comment: The comment text
            line_number: Optional line number the comment refers to
            timestamp: Optional timestamp for when the comment was made
        """
        self.agent_id = agent_id
        self.file_path = file_path
        self.comment = comment
        self.line_number = line_number
        self.timestamp = timestamp or datetime.utcnow()

    def to_dict(self) -> Dict[str, Union[str, int, None]]:
        """Convert the comment to a dictionary representation.
        
        Returns:
            Dictionary containing the comment data
        """
        return {
            "agent_id": self.agent_id,
            "file_path": self.file_path,
            "comment": self.comment,
            "line_number": self.line_number,
            "timestamp": self.timestamp.isoformat()
        }

