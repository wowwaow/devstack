# Warp Agent System Protocols

## Environment Configuration Protocols

### 1. Environment Initialization
```bash
# Required initialization sequence for all agents
source "$(dirname "$0")/../../core/config/environment.sh"

# Verify environment
if [[ -z "$WARP_SYSTEM_DIR" ]]; then
    echo "Error: Environment not properly initialized"
    exit 1
fi
```

### 2. Path Resolution
- Always use environment variables for path resolution
- Never hardcode system paths
- Use path joining for subdirectories
```python
import os

class AgentPathResolver:
    @staticmethod
    def get_log_path(log_name):
        return os.path.join(os.environ['SYSTEM_LOGS_DIR'], log_name)
    
    @staticmethod
    def get_agent_status_path(agent_id):
        return os.path.join(os.environ['AGENT_STATUS_DIR'], f"{agent_id}.json")
```

## Agent Protocols

### 1. Agent Registration
```python
def register_agent(agent_id):
    registry_path = os.environ['AGENT_REGISTRY']
    with open(registry_path, 'a') as f:
        f.write(f"{agent_id},{time.time()},ACTIVE\n")
```

### 2. Heartbeat Protocol
- Frequency: Every 2 minutes
- Location: $HEARTBEAT_MONITOR
```json
{
    "agent_id": "agent_001",
    "timestamp": "2025-05-31T18:30:00Z",
    "status": "ACTIVE",
    "current_task": "task_123",
    "progress": 65,
    "next_heartbeat": "2025-05-31T18:32:00Z"
}
```

### 3. Task Management
- Check task pool: $TASK_POOL_DIR
- Update task status: $CURRENT_OBJECTIVE_DIR
- Log missing tasks: $MISSING_TASKS_DIR
- Monitor dependencies: $DEPENDENCIES_DIR

## File Access Protocols

### 1. Log File Access
```python
def write_log(log_type, message):
    log_path = os.path.join(os.environ['SYSTEM_LOGS_DIR'], f"{log_type}.md")
    with open(log_path, 'a') as f:
        f.write(f"[{time.isoformat()}] {message}\n")
```

### 2. Status Updates
```python
def update_status(status_type, data):
    status_file = os.path.join(os.environ['AGENT_STATUS_DIR'], f"{status_type}.json")
    with open(status_file, 'w') as f:
        json.dump(data, f, indent=2)
```

## Event Handling Protocols

### 1. Task Detection Events
```python
def handle_missing_task(task_data):
    missing_tasks_dir = os.environ['MISSING_TASKS_DIR']
    task_file = os.path.join(missing_tasks_dir, f"task_{int(time.time())}.json")
    with open(task_file, 'w') as f:
        json.dump(task_data, f, indent=2)
```

### 2. Objective Promotion Events
```python
def handle_promotion(objective_id):
    source = os.path.join(os.environ['CURRENT_OBJECTIVE_DIR'], objective_id)
    target = os.path.join(os.environ['PAST_OBJECTIVES_DIR'], objective_id)
    shutil.move(source, target)
```

## Directory Management Protocols

### 1. Directory Creation
```python
def ensure_directory(dir_path):
    os.makedirs(dir_path, exist_ok=True)
    os.chmod(dir_path, 0o755)
```

### 2. File Management
```python
def create_system_file(file_path):
    with open(file_path, 'w') as f:
        pass
    os.chmod(file_path, 0o644)
```

## Security Protocols

### 1. Permission Management
```python
def set_secure_permissions():
    for dir_var in ['SYSTEM_LOGS_DIR', 'AGENT_STATUS_DIR']:
        dir_path = os.environ[dir_var]
        os.chmod(dir_path, 0o755)
        for root, dirs, files in os.walk(dir_path):
            for d in dirs:
                os.chmod(os.path.join(root, d), 0o755)
            for f in files:
                os.chmod(os.path.join(root, f), 0o644)
```

### 2. Access Control
- Use environment variables for all path access
- Validate file permissions before access
- Log all permission changes

## Error Handling Protocols

### 1. Environment Errors
```python
def verify_environment():
    required_vars = [
        'WARP_SYSTEM_DIR',
        'SYSTEM_LOGS_DIR',
        'AGENT_STATUS_DIR'
    ]
    missing = [var for var in required_vars if not os.environ.get(var)]
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {missing}")
```

### 2. File Access Errors
```python
def safe_file_access(file_path, mode='r'):
    try:
        with open(file_path, mode) as f:
            return f.read()
    except Exception as e:
        log_error(f"File access error: {e}")
        raise
```

## Monitoring Protocols

### 1. System Health Checks
```python
def check_system_health():
    status = {
        'timestamp': time.time(),
        'directory_status': check_directories(),
        'agent_status': check_agents(),
        'task_status': check_tasks()
    }
    update_status('system_health', status)
```

### 2. Performance Monitoring
```python
def monitor_performance():
    metrics = {
        'cpu_usage': get_cpu_usage(),
        'memory_usage': get_memory_usage(),
        'active_agents': count_active_agents(),
        'pending_tasks': count_pending_tasks()
    }
    log_metrics(metrics)
```

## Backup Protocols

### 1. System Backup
```python
def create_backup():
    backup_dir = os.environ['EMERGENCY_BACKUP_DIR']
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(backup_dir, f"backup_{timestamp}")
    shutil.copytree(os.environ['WARP_SYSTEM_DIR'], backup_path)
```

### 2. Log Rotation
```python
def rotate_logs():
    log_dir = os.environ['SYSTEM_LOGS_DIR']
    archive_dir = os.environ['MASTERLOG_ARCHIVE_DIR']
    # Implement log rotation logic
```
