"""Core type definitions for the AI Agent Stack.

This module provides shared type definitions and base classes used throughout
the agent system. It ensures type safety and consistent interfaces across
different components.
"""

from agent_stack.core.types.base import T, AgentID, TaskID
from agent_stack.core.types.agent import (
    AgentCapability,
    AgentMetadata,
    BaseAgent,
)
from agent_stack.core.types.task import (
    Task,
    TaskMetadata,
    TaskPriority,
    TaskStatus,
)
from agent_stack.core.types.comment import AgentComment

__all__ = [
    'T',
    'AgentID',
    'TaskID',
    'AgentCapability',
    'AgentMetadata',
    'BaseAgent',
    'Task',
    'TaskMetadata',
    'TaskPriority',
    'TaskStatus',
    'AgentComment',
]

