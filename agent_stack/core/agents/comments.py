#!/usr/bin/env python3

import os
import json
import datetime
from pathlib import Path
from typing import Dict, List, Optional

class AgentCommentSystem:
    def __init__(self):
        self.home = os.environ.get('HOME', os.path.expanduser('~'))
        self.devstack_dir = os.path.join(self.home, 'devstack')
        self.comments_dir = os.path.join(self.devstack_dir, 'agent_stack', 'core', 'comments')
        self.index_file = os.path.join(self.comments_dir, 'comment_index.json')
        self._ensure_structure()

    def _ensure_structure(self):
        """Ensure the comments directory structure exists."""
        os.makedirs(self.comments_dir, exist_ok=True)
        if not os.path.exists(self.index_file):
            self._save_index({})

    def _load_index(self) -> Dict:
        """Load the comment index."""
        try:
            with open(self.index_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_index(self, index: Dict):
        """Save the comment index."""
        with open(self.index_file, 'w') as f:
            json.dump(index, f, indent=2)

    def add_comment(self, agent_id: str, file_path: str, comment: str, line_number: Optional[int] = None):
        """Add a new comment from an agent."""
        index = self._load_index()
        
        # Make file path relative to devstack
        rel_path = os.path.relpath(file_path, self.devstack_dir)
        
        if rel_path not in index:
            index[rel_path] = []

        comment_entry = {
            'agent_id': agent_id,
            'comment': comment,
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'line_number': line_number
        }

        index[rel_path].append(comment_entry)
        self._save_index(index)

        # If line number is provided, add inline comment to file
        if line_number is not None:
            self._add_inline_comment(file_path, line_number, comment, agent_id)

    def _add_inline_comment(self, file_path: str, line_number: int, comment: str, agent_id: str):
        """Add an inline comment to a file."""
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # Format the comment
        comment_lines = [f"# AGENT[{agent_id}]: {line}" for line in comment.split('\n')]
        
        # Insert comments before the specified line
        for i, comment_line in enumerate(comment_lines):
            lines.insert(line_number + i - 1, comment_line + '\n')

        with open(file_path, 'w') as f:
            f.writelines(lines)

    def get_file_comments(self, file_path: str) -> List[Dict]:
        """Get all comments for a specific file."""
        index = self._load_index()
        rel_path = os.path.relpath(file_path, self.devstack_dir)
        return index.get(rel_path, [])

    def get_agent_comments(self, agent_id: str) -> Dict[str, List[Dict]]:
        """Get all comments from a specific agent."""
        index = self._load_index()
        agent_comments = {}
        
        for file_path, comments in index.items():
            agent_file_comments = [c for c in comments if c['agent_id'] == agent_id]
            if agent_file_comments:
                agent_comments[file_path] = agent_file_comments
                
        return agent_comments

