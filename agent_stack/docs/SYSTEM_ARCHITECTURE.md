# Warp Agent System Architecture

## System Overview

The Warp Agent system is designed as a flexible, portable AI agent coordination framework built around environment-based configuration and clear separation of concerns.

## Core Architecture Components

### 1. Environment Configuration Layer
```
core/config/environment.sh
```
- Defines all system paths and directories
- Enables system portability through environment variables
- Provides backward compatibility with legacy configurations
- Supports multiple instance deployment

### 2. Directory Structure
The system uses a hierarchical directory structure defined by environment variables:

```
$WARP_HOST_DIR/               # Base host directory
└── $WARP_SYSTEM_DIR/        # System directory (WARP_CURRENT)
    ├── System Commands/     # Command definitions
    ├── Work Logs/          # Session logs
    ├── System Logs/        # Operational logs
    ├── Warp Rules/         # System rules
    ├── Current Objective/  # Active tasks
    ├── Future Objectives/  # Queued objectives
    ├── Past Objectives/    # Completed work
    ├── Agent Status/       # Agent monitoring
    ├── Task Pool/          # Task definitions
    ├── Dependencies/       # Task dependencies
    ├── Missing Tasks/      # Task detection
    └── Promotion Queue/    # Objective promotion
```

### 3. Core Subsystems

#### Agent Management (`core/agents/`)
- Agent lifecycle management
- Task assignment and coordination
- Agent status monitoring
- Heartbeat tracking

#### Event System (`core/events/`)
- System event processing
- Inter-agent communication
- Event logging and tracking
- State change notifications

#### Logging Infrastructure (`core/logging/`)
- Centralized logging
- Log rotation and archival
- Activity tracking
- System diagnostics

#### Monitoring System (`core/monitoring/`)
- Agent health monitoring
- System performance tracking
- Resource utilization
- Anomaly detection

#### Task Management (`core/tasks/`)
- Task definition and tracking
- Dependency management
- Missing task detection
- Task state management

## System Integration

### Environment Variable Integration
The system uses environment variables for configuration, enabling:
- Portable deployments
- Multiple instance support
- Custom path configurations
- Development/production environment separation

Example:
```bash
# Custom deployment
export WARP_HOST_DIR=/custom/path
export WARP_SYSTEM_DIR=/custom/path/instance1
source core/config/environment.sh

# All subsystems automatically use updated paths
agent_status_file="$AGENT_STATUS_DIR/status.json"
log_file="$SYSTEM_LOGS_DIR/system.log"
```

### Directory Structure Integration
```python
# Python example of system integration
class WarpSystem:
    def __init__(self):
        self.system_dir = os.environ['SYSTEM_DIR']
        self.logs_dir = os.environ['SYSTEM_LOGS_DIR']
        self.agent_dir = os.environ['AGENT_STATUS_DIR']
        
    def initialize_directories(self):
        """Create required system directories"""
        os.makedirs(self.logs_dir, exist_ok=True)
        os.makedirs(self.agent_dir, exist_ok=True)
        
    def get_log_path(self, log_name):
        """Get absolute path for a log file"""
        return os.path.join(self.logs_dir, log_name)
```

## Deployment Configurations

### Single Instance
```bash
export WARP_HOST_DIR=/mnt/host
export WARP_SYSTEM_DIR=$WARP_HOST_DIR/WARP_CURRENT
source core/config/environment.sh
```

### Multiple Instances
```bash
# Development instance
export WARP_SYSTEM_DIR=/mnt/host/warp_dev
source core/config/environment.sh

# Production instance
export WARP_SYSTEM_DIR=/mnt/host/warp_prod
source core/config/environment.sh
```

### Cloud Deployment
```bash
# AWS deployment example
export WARP_HOST_DIR=/mnt/efs/warp
export WARP_SYSTEM_DIR=/mnt/efs/warp/production
source core/config/environment.sh
```

## Security Considerations

### File Permissions
- System directories: 755 (drwxr-xr-x)
- Configuration files: 644 (rw-r--r--)
- Executable scripts: 755 (rwxr-xr-x)

### Environment Security
- Environment variables are local to each process
- No sensitive data in environment variables
- Separate configuration for sensitive data

## System Requirements

### Minimum Requirements
- Linux/Unix environment
- Bash shell
- Python 3.8+
- 1GB RAM
- 10GB storage

### Recommended Requirements
- 4GB+ RAM
- 50GB+ storage
- SSD storage for logs
- Multi-core processor

## Future Considerations

### Scalability
- Container support
- Distributed system support
- Cloud-native deployment
- Kubernetes integration

### Monitoring
- Enhanced metrics collection
- Performance monitoring
- Resource utilization tracking
- Alert system integration

