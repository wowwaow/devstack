# Agent CLI Interface

This module provides a Python interface for agents to interact with the WARP system. It offers both a low-level CLI interface and a higher-level agent context system.

## Usage

### Basic CLI Usage
```python
from agents.cli import AgentCLI

# Initialize the CLI
cli = AgentCLI()

# Register an agent
cli.register('my_agent', 'active')

# Create a task
cli.create_task('task_001', 'Process data files', 'my_agent')

# Check agent status
status = cli.get_status('my_agent')
```

### Using Agent Context
```python
from agents.cli import get_agent_context

# Get an agent context (automatically registers the agent)
agent = get_agent_context('my_agent')

# Create a task (automatically assigned to this agent)
agent.create_task('task_002', 'Analyze results')

# Send heartbeat
agent.heartbeat()
```

## Features
- Automatic agent registration
- Task creation and assignment
- System health monitoring
- Tool installation
- Backup management
- Error handling and structured output

## Installation
The CLI interface is automatically available to all agents in the devstack environment. No additional installation is required.

## Examples
See `examples.py` for detailed usage examples.

