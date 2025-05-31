from typing import Dict, List, Optional, Any
import subprocess
import json
import os
from datetime import datetime

class AgentCLI:
    def __init__(self):
        self.home = os.environ.get('HOME', os.path.expanduser('~'))
        self.devstack_dir = os.path.join(self.home, 'devstack')
        self.warp_system = os.path.join(self.devstack_dir, 'agent_stack', 'core', 'warp_system.sh')
        self._ensure_executable()

    def _ensure_executable(self):
        """Ensure the warp_system.sh script is executable."""
        if os.path.exists(self.warp_system):
            os.chmod(self.warp_system, 0o755)

    def _run_command(self, *args) -> Dict[str, Any]:
        """Run a warp system command and return structured output."""
        try:
            cmd = [self.warp_system] + list(args)
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            return {
                'success': result.returncode == 0,
                'output': result.stdout.strip(),
                'error': result.stderr.strip() if result.returncode != 0 else None,
                'code': result.returncode
            }
        except Exception as e:
            return {
                'success': False,
                'output': None,
                'error': str(e),
                'code': -1
            }

    def register(self, agent_id: str, status: str = 'active') -> Dict[str, Any]:
        """Register an agent with the system."""
        return self._run_command('register_agent', agent_id, status)

    def create_task(self, task_id: str, description: str, 
                   agent: Optional[str] = None, 
                   priority: str = 'medium') -> Dict[str, Any]:
        """Create a new task."""
        args = ['create_task', task_id, description]
        if agent:
            args.append(agent)
        if priority:
            args.append(priority)
        return self._run_command(*args)

    def assign_task(self, agent_id: str, task_id: str) -> Dict[str, Any]:
        """Assign a task to an agent."""
        return self._run_command('assign_task', agent_id, task_id)

    def get_status(self, agent_id: str) -> Dict[str, Any]:
        """Get an agent's status."""
        return self._run_command('agent_status', agent_id)

    def heartbeat(self, agent_id: str) -> Dict[str, Any]:
        """Send a heartbeat for an agent."""
        return self._run_command('heartbeat', agent_id)

    def system_health(self) -> Dict[str, Any]:
        """Check system health."""
        return self._run_command('health')

    def create_backup(self, name: Optional[str] = None) -> Dict[str, Any]:
        """Create a system backup."""
        args = ['backup']
        if name:
            args.append(name)
        return self._run_command(*args)

    def install_tool(self, tool_name: str, method: str = 'auto') -> Dict[str, Any]:
        """Install a tool."""
        return self._run_command('install_tool', tool_name, method)

class AgentContext:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.cli = AgentCLI()
        self._register()

    def _register(self):
        """Register the agent if not already registered."""
        self.cli.register(self.agent_id)

    def create_task(self, task_id: str, description: str, 
                    priority: str = 'medium') -> Dict[str, Any]:
        """Create a task assigned to this agent."""
        return self.cli.create_task(task_id, description, self.agent_id, priority)

    def heartbeat(self) -> Dict[str, Any]:
        """Send agent heartbeat."""
        return self.cli.heartbeat(self.agent_id)

    def get_status(self) -> Dict[str, Any]:
        """Get this agent's status."""
        return self.cli.get_status(self.agent_id)

    def install_tool(self, tool_name: str, method: str = 'auto') -> Dict[str, Any]:
        """Install a required tool."""
        return self.cli.install_tool(tool_name, method)

def get_agent_context(agent_id: str) -> AgentContext:
    """Get an agent context for the specified agent ID."""
    return AgentContext(agent_id)

