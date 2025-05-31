"""Base configuration management for the AI Agent Stack.

This module implements a robust configuration system using pydantic for
validation and type safety. It supports multiple environments and provides
a clean interface for accessing configuration values.
"""

from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, validator
from pydantic_settings import BaseSettings

class Environment(str, Enum):
    """Supported environment types."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class LogConfig(BaseModel):
    """Logging configuration settings."""
    level: str = Field(default="INFO", description="Logging level")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format string"
    )
    file_path: Optional[Path] = Field(
        default=None,
        description="Path to log file. If None, logs to stdout"
    )
    rotate_size: str = Field(
        default="10MB",
        description="Size at which to rotate log files"
    )
    rotate_count: int = Field(
        default=5,
        description="Number of rotated log files to keep"
    )

class DatabaseConfig(BaseModel):
    """Database configuration settings."""
    url: str = Field(..., description="Database connection URL")
    pool_size: int = Field(default=5, description="Connection pool size")
    max_overflow: int = Field(default=10, description="Maximum connection overflow")
    echo: bool = Field(default=False, description="Echo SQL statements")

class AgentConfig(BaseModel):
    """Agent-specific configuration settings."""
    heartbeat_interval: int = Field(
        default=60,
        description="Interval between agent heartbeats in seconds"
    )
    task_poll_interval: int = Field(
        default=5,
        description="Interval between task polling in seconds"
    )
    max_retries: int = Field(
        default=3,
        description="Maximum number of task retries"
    )
    timeout: int = Field(
        default=3600,
        description="Default task timeout in seconds"
    )

class Settings(BaseSettings):
    """Main configuration settings for the AI Agent Stack."""
    
    environment: Environment = Field(
        default=Environment.DEVELOPMENT,
        description="Current environment"
    )
    debug: bool = Field(
        default=False,
        description="Enable debug mode"
    )
    secret_key: str = Field(
        ...,
        description="Secret key for secure operations"
    )
    
    # Component configurations
    logging: LogConfig = Field(
        default_factory=LogConfig,
        description="Logging configuration"
    )
    database: DatabaseConfig = Field(
        ...,
        description="Database configuration"
    )
    agent: AgentConfig = Field(
        default_factory=AgentConfig,
        description="Agent configuration"
    )
    
    # Directory paths
    base_dir: Path = Field(
        default=Path.home() / "devstack",
        description="Base directory for the system"
    )
    data_dir: Path = Field(
        default=Path.home() / "devstack/data",
        description="Data directory"
    )
    
    @validator("data_dir", "base_dir")
    def create_directories(cls, v: Path) -> Path:
        """Ensure directories exist.
        
        Args:
            v: Directory path to validate
            
        Returns:
            Validated directory path
        """
        v.mkdir(parents=True, exist_ok=True)
        return v
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

def load_settings(env_file: Optional[str] = None) -> Settings:
    """Load settings from environment and files.
    
    Args:
        env_file: Optional path to environment file
        
    Returns:
        Loaded and validated settings
    """
    return Settings(_env_file=env_file)

