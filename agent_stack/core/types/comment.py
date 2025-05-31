"""Comment-related type definitions."""

from datetime import datetime
from typing import Dict, Optional, Union

from agent_stack.core.types.base import AgentID

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

