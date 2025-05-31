"""Test configuration and fixtures for the AI Agent Stack."""

import asyncio
from pathlib import Path
from typing import AsyncGenerator, Generator

import pytest
from _pytest.fixtures import SubRequest

from agent_stack.core.config.base import Environment, Settings, load_settings
from agent_stack.core.types import AgentCapability, AgentID, AgentMetadata, BaseAgent, Task

@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """Create test settings with a temporary directory structure."""
    temp_dir = Path("/tmp/devstack_test")
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    return Settings(
        environment=Environment.DEVELOPMENT,
        debug=True,
        secret_key="test_secret_key",
        base_dir=temp_dir,
        data_dir=temp_dir / "data",
        database={
            "url": "sqlite:///:memory:",
            "echo": True
        }
    )

@pytest.fixture
async def mock_agent(request: SubRequest) -> AsyncGenerator[BaseAgent, None]:
    """Create a mock agent for testing.
    
    Args:
        request: Pytest request object containing markers
        
    Yields:
        A configured mock agent
    """
    # Allow tests to customize agent capabilities via markers
    marker = request.node.get_closest_marker("agent_capabilities")
    capabilities = marker.args[0] if marker else [AgentCapability.TASK_PROCESSING]
    
    # Create mock agent class
    class MockAgent(BaseAgent):
        async def process_task(self, task: Task) -> Task:
            task.status = "completed"
            task.result = {"mock": "result"}
            return task
        
        async def heartbeat(self) -> bool:
            return True
    
    # Create agent instance
    agent_id = AgentID("mock_agent_1")
    metadata = AgentMetadata(
        capabilities=capabilities,
        status="active",
        version="1.0.0"
    )
    
    agent = MockAgent(agent_id, metadata)
    yield agent

@pytest.fixture
def temp_file(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a temporary file for testing.
    
    Args:
        tmp_path: Pytest temporary directory fixture
        
    Yields:
        Path to temporary file
    """
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("Test content")
    yield test_file

