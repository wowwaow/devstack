#!/usr/bin/env python3

from . import get_agent_context, AgentCLI

def example_usage():
    # Initialize the CLI
    cli = AgentCLI()
    
    # Register a new agent
    result = cli.register('example_agent', 'active')
    print(f"Agent registration: {result}")
    
    # Create a task
    result = cli.create_task('task_001', 'Example task description', 'example_agent')
    print(f"Task creation: {result}")
    
    # Get agent status
    result = cli.get_status('example_agent')
    print(f"Agent status: {result}")
    
    # Using agent context
    agent = get_agent_context('example_agent')
    
    # Create task through agent context
    result = agent.create_task('task_002', 'Another example task')
    print(f"Task creation through context: {result}")
    
    # Send heartbeat
    result = agent.heartbeat()
    print(f"Heartbeat: {result}")

if __name__ == '__main__':
    example_usage()

