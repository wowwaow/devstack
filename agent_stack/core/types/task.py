"""Task-related type definitions."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Optional

from agent_stack.core.types.base import AgentID, TaskID

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

