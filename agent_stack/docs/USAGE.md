# AI Agent Stack Usage Guide

## Getting Started

### Basic Concepts
- **Agents**: Autonomous AI entities that perform tasks
- **Tasks**: Units of work to be completed
- **Objectives**: Groups of related tasks
- **Protocols**: Rules governing agent interaction
- **Commands**: System operations and controls

### System Structure
```
agent_stack/
├── core/               # System core
├── protocols/         # Agent protocols
├── commands/          # Available commands
├── docs/             # Documentation
└── logs/             # System logs
```

## Working with Agents

### Agent Lifecycle

1. **Initialization**
```python
from agent_stack.core import Agent

agent = Agent(agent_id="agent_001")
agent.initialize()
```

2. **Registration**
```python
agent.register()
# Automatically logs to AGENT_REGISTRY.csv
```

3. **Heartbeat Management**
```python
agent.start_heartbeat()
# Sends heartbeats every 2 minutes
```

4. **Task Assignment**
```python
task = agent.request_task()
agent.start_task(task)
```

5. **Status Updates**
```python
agent.update_status(
    status="WORKING",
    progress=75,
    current_task="task_123"
)
```

### Agent Commands

#### DETECT_MISSING_TASKS
```python
# Automatic task detection
agent.detect_missing_tasks(
    objective_name="current_objective",
    scan_depth="full",
    auto_add=True
)
```

#### MONITOR_AGENTS
```python
# Start agent monitoring
agent.monitor_agents(
    scan_interval=30,
    timeout_threshold=300,
    auto_reassign=True
)
```

## Task Management

### Creating Tasks
```python
from agent_stack.core import Task

task = Task(
    name="process_data",
    priority=1,
    dependencies=["fetch_data"],
    required_skills=["data_processing"]
)
```

### Task Assignment
```python
# Automatic assignment
task_pool.assign_task(agent_id)

# Manual assignment
task_pool.assign_specific_task(task_id, agent_id)
```

### Task Status Updates
```python
task.update_progress(
    progress=50,
    status="IN_PROGRESS",
    notes="Processing batch 2/4"
)
```

## Objective Management

### Creating Objectives
```python
from agent_stack.core import Objective

objective = Objective(
    name="data_analysis_project",
    priority=1,
    deadline="2025-06-30"
)
```

### Adding Tasks to Objectives
```python
objective.add_task(task)
objective.add_tasks([task1, task2, task3])
```

### Promoting Objectives
```python
# Automatic promotion
system.check_and_promote_objectives()

# Manual promotion
system.promote_objective(objective_id)
```

## Resource Management

### Allocating Resources
```python
resource_manager.allocate(
    agent_id="agent_001",
    resource_type="CPU",
    amount=2
)
```

### Resource Monitoring
```python
usage = resource_manager.get_usage(agent_id)
resource_manager.check_availability()
```

## System Monitoring

### Health Checks
```python
# Run system health check
system.check_health()

# Get agent status
system.get_agent_status(agent_id)

# Monitor resource usage
system.monitor_resources()
```

### Log Management
```python
# Access logs
system_logs = LogManager.get_system_logs()
work_logs = LogManager.get_work_logs()

# Search logs
results = LogManager.search_logs(
    query="error",
    start_time="2025-05-31T00:00:00Z",
    end_time="2025-05-31T23:59:59Z"
)
```

## Error Handling

### Common Error Patterns
```python
try:
    agent.execute_task(task)
except AgentTimeoutError:
    system.handle_timeout(agent_id)
except TaskFailureError:
    system.handle_task_failure(task_id)
```

### Recovery Procedures
```python
# Agent recovery
system.recover_agent(agent_id)

# Task recovery
system.recover_task(task_id)

# System state recovery
system.recover_state()
```

## Best Practices

### Agent Operation
1. Always initialize agents properly
2. Maintain regular heartbeats
3. Update task progress frequently
4. Handle errors gracefully
5. Clean up resources after completion

### Task Management
1. Define clear task requirements
2. Set appropriate priorities
3. Document dependencies
4. Monitor progress
5. Validate completion

### Resource Utilization
1. Request resources efficiently
2. Release unused resources
3. Monitor resource usage
4. Handle resource conflicts
5. Optimize resource allocation

## Advanced Features

### Custom Agent Behaviors
```python
class CustomAgent(Agent):
    def custom_behavior(self):
        # Implement custom logic
        pass
```

### Protocol Extensions
```python
class CustomProtocol(BaseProtocol):
    def custom_protocol_logic(self):
        # Implement custom protocol
        pass
```

### System Integration
```python
# Integrate with external systems
system.integrate_external(
    system_type="external_db",
    connection_params={...}
)
```

## Troubleshooting

### Common Issues
1. Agent timeout resolution
2. Task assignment conflicts
3. Resource allocation issues
4. Protocol synchronization
5. System state inconsistencies

### Debugging Tools
```python
# Debug mode
system.enable_debug()

# Trace operations
system.trace_operation(operation_id)

# Analyze system state
system.analyze_state()
```

## Performance Optimization

### System Tuning
1. Adjust heartbeat intervals
2. Optimize resource allocation
3. Fine-tune task distribution
4. Configure monitoring thresholds
5. Optimize log rotation

### Scaling Guidelines
1. Monitor system metrics
2. Adjust resource limits
3. Balance agent workload
4. Optimize task distribution
5. Manage system overhead

## Additional Resources
- [System Architecture](SYSTEM_ARCHITECTURE.md)
- [Protocol Reference](PROTOCOLS.md)
- [Command Reference](COMMANDS.md)
- [API Documentation](API.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)
