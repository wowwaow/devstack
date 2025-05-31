"""
AI Agent Stack - Task Management System
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Set
import uuid

@dataclass
class Task:
    """Task definition and state"""
    task_id: str = field(default_factory=lambda: f"task_{uuid.uuid4().hex[:8]}")
    name: str = ""
    description: str = ""
    priority: int = 1
    status: str = "PENDING"
    progress: int = 0
    assigned_agent: Optional[str] = None
    dependencies: Set[str] = field(default_factory=set)
    required_skills: Set[str] = field(default_factory=set)
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    estimated_duration: Optional[int] = None
    actual_duration: Optional[int] = None
    metadata: Dict = field(default_factory=dict)

class TaskPool:
    """System-wide task management"""
    
    _tasks: Dict[str, Task] = {}
    _agent_tasks: Dict[str, Set[str]] = {}
    _dependency_graph: Dict[str, Set[str]] = {}
    
    @classmethod
    def create_task(cls, 
                   name: str,
                   description: str = "",
                   priority: int = 1,
                   dependencies: Set[str] = None,
                   required_skills: Set[str] = None,
                   estimated_duration: Optional[int] = None) -> Task:
        """Create a new task"""
        task = Task(
            name=name,
            description=description,
            priority=priority,
            dependencies=dependencies or set(),
            required_skills=required_skills or set(),
            estimated_duration=estimated_duration
        )
        
        cls._tasks[task.task_id] = task
        cls._update_dependency_graph(task)
        
        return task
    
    @classmethod
    def _update_dependency_graph(cls, task: Task):
        """Update the dependency graph with a new task"""
        cls._dependency_graph[task.task_id] = task.dependencies
        
        # Verify no cycles are created
        if cls._has_dependency_cycle(task.task_id):
            raise ValueError("Task dependencies would create a cycle")
            
    @classmethod
    def _has_dependency_cycle(cls, task_id: str, visited: Set[str] = None) -> bool:
        """Check for dependency cycles"""
        if visited is None:
            visited = set()
            
        if task_id in visited:
            return True
            
        visited.add(task_id)
        
        for dep_id in cls._dependency_graph.get(task_id, set()):
            if cls._has_dependency_cycle(dep_id, visited):
                return True
                
        visited.remove(task_id)
        return False
    
    @classmethod
    def get_task(cls, agent_id: str, capabilities: List[str]) -> Optional[Task]:
        """Get next available task for an agent"""
        available_tasks = []
        
        for task in cls._tasks.values():
            if cls._can_assign_task(task, agent_id, capabilities):
                available_tasks.append(task)
                
        if not available_tasks:
            return None
            
        # Sort by priority and select highest
        task = max(available_tasks, key=lambda t: t.priority)
        cls._assign_task(task, agent_id)
        
        return task
    
    @classmethod
    def _can_assign_task(cls, task: Task, agent_id: str, capabilities: List[str]) -> bool:
        """Check if a task can be assigned to an agent"""
        if task.status != "PENDING":
            return False
            
        if task.assigned_agent is not None:
            return False
            
        # Check capabilities
        if not task.required_skills.issubset(set(capabilities)):
            return False
            
        # Check dependencies
        for dep_id in task.dependencies:
            dep_task = cls._tasks.get(dep_id)
            if not dep_task or dep_task.status != "COMPLETED":
                return False
                
        return True
    
    @classmethod
    def _assign_task(cls, task: Task, agent_id: str):
        """Assign a task to an agent"""
        task.status = "ASSIGNED"
        task.assigned_agent = agent_id
        task.started_at = datetime.utcnow()
        
        if agent_id not in cls._agent_tasks:
            cls._agent_tasks[agent_id] = set()
        cls._agent_tasks[agent_id].add(task.task_id)
    
    @classmethod
    def complete_task(cls, task_id: str, agent_id: str):
        """Mark a task as completed"""
        task = cls._tasks.get(task_id)
        if not task:
            raise ValueError(f"Task not found: {task_id}")
            
        if task.assigned_agent != agent_id:
            raise ValueError(f"Task not assigned to agent: {agent_id}")
            
        task.status = "COMPLETED"
        task.completed_at = datetime.utcnow()
        task.actual_duration = (task.completed_at - task.started_at).total_seconds()
        
        cls._agent_tasks[agent_id].remove(task_id)
        
        # Notify waiting tasks
        cls._notify_dependent_tasks(task_id)
    
    @classmethod
    def _notify_dependent_tasks(cls, completed_task_id: str):
        """Notify tasks that were waiting on this completion"""
        for task_id, deps in cls._dependency_graph.items():
            if completed_task_id in deps:
                task = cls._tasks.get(task_id)
                if task and task.status == "PENDING":
                    # Check if all dependencies are now complete
                    all_deps_complete = all(
                        cls._tasks.get(dep_id).status == "COMPLETED"
                        for dep_id in task.dependencies
                    )
                    if all_deps_complete:
                        cls._notify_task_ready(task)
    
    @classmethod
    def _notify_task_ready(cls, task: Task):
        """Notify system that a task is ready for assignment"""
        from agent_stack.core.events import SystemEventBus
        
        SystemEventBus.emit(
            "task_ready",
            {
                "task_id": task.task_id,
                "name": task.name,
                "priority": task.priority
            }
        )
    
    @classmethod
    def get_agent_tasks(cls, agent_id: str) -> List[Task]:
        """Get all tasks assigned to an agent"""
        task_ids = cls._agent_tasks.get(agent_id, set())
        return [cls._tasks[task_id] for task_id in task_ids]
    
    @classmethod
    def reassign_task(cls, task_id: str, new_agent_id: Optional[str] = None):
        """Reassign a task to a new agent or back to the pool"""
        task = cls._tasks.get(task_id)
        if not task:
            raise ValueError(f"Task not found: {task_id}")
            
        old_agent_id = task.assigned_agent
        if old_agent_id:
            cls._agent_tasks[old_agent_id].remove(task_id)
            
        if new_agent_id:
            cls._assign_task(task, new_agent_id)
        else:
            task.status = "PENDING"
            task.assigned_agent = None
            
        # Log reassignment
        from agent_stack.core.logging import SystemLogger
        
        SystemLogger.info(
            f"Task reassigned: {task_id}",
            extra={
                "task_id": task_id,
                "old_agent": old_agent_id,
                "new_agent": new_agent_id,
                "reason": "manual_reassignment"
            }
        )
