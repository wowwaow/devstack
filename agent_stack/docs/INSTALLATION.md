# Warp Agent Stack Installation

## Prerequisites
- Linux/Unix environment
- Bash shell
- Git

## Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/wowwaow/devstack.git
cd devstack/agent_stack
```

2. Configure Environment:
```bash
# Optional: Set custom base directories
export WARP_HOST_DIR=/path/to/host/directory     # Default: /mnt/host
export WARP_SYSTEM_DIR=/path/to/system/directory # Default: $WARP_HOST_DIR/WARP_CURRENT

# Source the environment configuration
source core/config/environment.sh
```

3. Initialize Directory Structure:
```bash
# Create required directories
mkdir -p \
  "$SYSTEM_COMMANDS_DIR" \
  "$WORK_LOGS_DIR" \
  "$SYSTEM_LOGS_DIR" \
  "$WARP_RULES_DIR" \
  "$CURRENT_OBJECTIVE_DIR" \
  "$FUTURE_OBJECTIVES_DIR" \
  "$PAST_OBJECTIVES_DIR" \
  "$AGENT_STATUS_DIR" \
  "$TASK_POOL_DIR" \
  "$DEPENDENCIES_DIR" \
  "$MISSING_TASKS_DIR" \
  "$PROMOTION_QUEUE_DIR" \
  "$TEMPLATES_DIR" \
  "$ARCHIVE_DIR"
```

4. Initialize System Files:
```bash
# Create necessary system files
touch \
  "$MAIN_RULESET" \
  "$SYSTEM_DOCUMENTATION" \
  "$PATH_REGISTRY" \
  "$TIDY_LOG" \
  "$ORGANIZE_LOG" \
  "$SYSTEM_STATUS" \
  "$ANOMALY_LOG" \
  "$SUPERVISOR_ALERTS" \
  "$AGENT_REGISTRY" \
  "$MISSING_TASKS_LOG" \
  "$OBJECTIVE_PROMOTION_LOG" \
  "$AGENT_TIMEOUT_LOG" \
  "$TASK_REASSIGNMENT_LOG" \
  "$HEARTBEAT_MONITOR"
```

## Configuration Options

### Custom Installation Paths
You can customize the installation location by setting environment variables before sourcing the configuration:

```bash
# Example: Custom host directory
export WARP_HOST_DIR=/custom/host/path
source core/config/environment.sh

# Example: Custom system directory
export WARP_SYSTEM_DIR=/custom/system/path
source core/config/environment.sh
```

### Multiple Instance Setup
You can run multiple instances by using different system directories:

```bash
# Instance A
export WARP_SYSTEM_DIR=/mnt/host/WARP_PROJECT_A
source core/config/environment.sh

# Instance B
export WARP_SYSTEM_DIR=/mnt/host/WARP_PROJECT_B
source core/config/environment.sh
```

## Directory Structure

### Primary System Directories
- `$SYSTEM_DIR/` - Core system
  - `System Commands/` - Command definitions and executables
  - `Work Logs/` - Active session logs and archives
  - `System Logs/` - System maintenance and operational logs
  - `Warp Rules/` - Governance and operational procedures
  - `Current Objective/` - Active project phase data
  - `Future Objectives/` - Queued project phases
  - `Past Objectives/` - Completed project archives
  - `Agent Status/` - Per-agent heartbeat and status files
  - `Task Pool/` - Active and pending task definitions
  - `Dependencies/` - Cross-task dependency mapping
  - `Missing Tasks/` - Detected missing tasks awaiting addition
  - `Promotion Queue/` - Objectives ready for promotion tracking

### Secondary Directories
- `$TEMPLATES_DIR/` - Template files
- `$ARCHIVE_DIR/` - Archived files
- `$MASTERLOG_ARCHIVE_DIR/` - Log archives
- `$EMERGENCY_BACKUP_DIR/` - System backups
- `$CLOUD_SYNC_DIR/` - Cloud sync staging
- `$SIMULATION_DIR/` - Simulation workspace
- `$REMOTE_CACHE_DIR/` - Remote backup cache

## Verification
After installation, verify the setup by running:
```bash
# Check directory structure
ls -la "$SYSTEM_DIR"

# Verify file permissions
ls -la "$SYSTEM_LOGS_DIR"
ls -la "$AGENT_STATUS_DIR"

# Test environment configuration
echo $SYSTEM_DIR
echo $WARP_RULES_DIR
```

## Troubleshooting

### Common Issues

1. Permission Denied
```bash
# Fix directory permissions
sudo chown -R $USER:$USER "$SYSTEM_DIR"
sudo chmod -R 755 "$SYSTEM_DIR"
```

2. Environment Variables Not Set
```bash
# Verify environment setup
env | grep WARP
env | grep SYSTEM
```

3. Missing Directories
```bash
# Recreate directory structure
source core/config/environment.sh
./scripts/setup_directories.sh
```
