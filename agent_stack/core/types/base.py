"""Base type definitions and type variables."""

from typing import TypeVar
from uuid import UUID

# Type variables for generic type hints
T = TypeVar('T')
AgentID = str
TaskID = UUID

