# Warp Agent Rules

This directory contains the core rules and protocols for the Warp Agent system. All agents must follow these rules exactly for proper system operation.

## 🌍 Environment Configuration

The system uses environment-based configuration for flexibility and portability:

```bash
# Base configuration
export WARP_HOST_DIR="${WARP_HOST_DIR:-/mnt/host}"
export WARP_SYSTEM_DIR="${WARP_SYSTEM_DIR:-$WARP_HOST_DIR/WARP_CURRENT}"

# Legacy compatibility
export SYSTEM_DIR="$WARP_SYSTEM_DIR"
```

## 📁 Directory Structure

### Primary System Directories
- **Core system** → `$SYSTEM_DIR/`
  - `System Commands/` → Command definitions and executables
  - `Work Logs/` → Active session logs and archives
  - `System Logs/` → System maintenance and operational logs
  - `Warp Rules/` → Governance and operational procedures
  - `Current Objective/` → Active project phase data
  - `Future Objectives/` → Queued project phases
  - `Past Objectives/` → Completed project archives
  - `Agent Status/` → Per-agent heartbeat and status files
  - `Task Pool/` → Active and pending task definitions
  - `Dependencies/` → Cross-task and cross-objective dependency mapping
  - `Missing Tasks/` → **Detected missing tasks awaiting addition**
  - `Promotion Queue/` → **Objectives ready for promotion tracking**

### Secondary Directories
- **Templates** → `$TEMPLATES_DIR/`
- **Archived files** → `$ARCHIVE_DIR/`
- **Masterlog archive** → `$MASTERLOG_ARCHIVE_DIR/`
- **Emergency backups** → `$EMERGENCY_BACKUP_DIR/`
- **Cloud sync staging** → `$CLOUD_SYNC_DIR/`
- **Simulation workspace** → `$SIMULATION_DIR/`
- **Remote backup cache** → `$REMOTE_CACHE_DIR/`

## 📝 Critical System Files

### Configuration Files
- **Main ruleset** → `$MAIN_RULESET`
- **System documentation** → `$SYSTEM_DOCUMENTATION`
- **Path registry** → `$PATH_REGISTRY`

### Log Files
- **Tidy log** → `$TIDY_LOG`
- **Organize log** → `$ORGANIZE_LOG`
- **System status** → `$SYSTEM_STATUS`
- **Anomaly detection log** → `$ANOMALY_LOG`
- **Supervisor alerts** → `$SUPERVISOR_ALERTS`

### Agent Management
- **Agent registry** → `$AGENT_REGISTRY`
- **🆕 Missing task log** → `$MISSING_TASKS_LOG`
- **🆕 Objective promotion log** → `$OBJECTIVE_PROMOTION_LOG`
- **🆕 Agent timeout log** → `$AGENT_TIMEOUT_LOG`
- **🆕 Task reassignment log** → `$TASK_REASSIGNMENT_LOG`
- **🆕 Agent heartbeat monitor** → `$HEARTBEAT_MONITOR`

## 🔄 Instance Management

The system supports multiple instances through environment configuration:

```bash
# Development instance
export WARP_SYSTEM_DIR=/path/to/dev/instance
source core/config/environment.sh

# Production instance
export WARP_SYSTEM_DIR=/path/to/prod/instance
source core/config/environment.sh
```

Use the instance management utility for operations:
```bash
# Create new instance
./core/config/manage_instances.sh create dev_instance

# List instances
./core/config/manage_instances.sh list

# Switch instance
./core/config/manage_instances.sh switch prod_instance
```

## 🔐 Security Rules

1. Never expose sensitive data in environment variables
2. Maintain proper file permissions:
   - Directories: 755 (drwxr-xr-x)
   - Files: 644 (rw-r--r--)
3. Validate environment before operations
4. Log all security-relevant actions

## 🚀 System Operations

1. Initialize environment before operations
2. Validate configuration regularly
3. Monitor agent health
4. Track task dependencies
5. Handle missing tasks
6. Manage objective promotion
7. Maintain system logs

## ⚠️ Error Handling

1. Validate environment variables
2. Check file permissions
3. Verify directory structure
4. Log all errors
5. Alert on anomalies

## 📊 Monitoring

1. Track agent heartbeats
2. Monitor system health
3. Log performance metrics
4. Track resource usage
5. Monitor task progress


## 🔄 Automatic Git Sync and Rebuild

The system automatically synchronizes with the devstack repository and rebuilds itself:

### Auto-Sync Features
- Hourly automatic sync with devstack repository
- Automatic system rebuild on updates
- Configuration preservation across updates
- Seamless multi-machine deployment

### Manual Sync
```bash
# Trigger manual sync
$SYSTEM_DIR/core/sync_rules.sh
```

### Initial Setup
The system automatically:
1. Clones devstack repository
2. Syncs rules and configuration
3. Sets up automatic updates
4. Configures environment
5. Rebuilds system structure

### Cross-Machine Deployment
To deploy on a new machine:
1. Set environment variables:
   ```bash
   export WARP_HOST_DIR="/desired/host/path"
   export WARP_SYSTEM_DIR="/desired/system/path"
   ```

2. Run initial setup:
   ```bash
   ./core/initialize.sh
   ```

The system will:
- Clone devstack repository
- Configure automatic updates
- Create directory structure
- Set up monitoring
- Enable automatic sync

### Sync Configuration
- Default sync: Hourly
- Source: github.com/wowwaow/devstack
- Target: $WARP_RULES_DIR
- Backup: Automatic before sync
- Rebuild: Automatic after sync

