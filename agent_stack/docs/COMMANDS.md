# AI Agent Stack Command Reference

## Core System Commands

### DETECT_MISSING_TASKS
**Purpose:** AI-driven detection and addition of missing tasks to current objective

**Syntax:**
```bash
DETECT_MISSING_TASKS [objective_name] [scan_depth] [auto_add]
```

**Parameters:**
- `objective_name`: Name of the objective to scan
- `scan_depth`: Depth of analysis ("quick", "normal", "deep")
- `auto_add`: Boolean flag for automatic task addition

**Behavior:**
- Pattern Analysis
- Dependency Gap Detection
- Best Practice Scanning
- Stakeholder Review Tasks
- Quality Assurance Tasks
- Documentation Tasks
- Auto-Addition
- Priority Assignment

**Example:**
```python
system.detect_missing_tasks(
    objective_name="project_alpha",
    scan_depth="deep",
    auto_add=True
)
```

### MONITOR_AGENTS
**Purpose:** Continuous agent heartbeat monitoring with automatic timeout detection

**Syntax:**
```bash
MONITOR_AGENTS [scan_interval] [timeout_threshold] [auto_reassign]
```

**Parameters:**
- `scan_interval`: Seconds between scans (default: 30)
- `timeout_threshold`: Minutes before timeout (default: 5)
- `auto_reassign`: Enable automatic task reassignment

**Features:**
- Heartbeat Scanning
- Timeout Detection
- Task State Analysis
- Automatic Reassignment
- Progress Preservation
- Agent Notification
- Detailed Logging

**Example:**
```python
system.monitor_agents(
    scan_interval=30,
    timeout_threshold=5,
    auto_reassign=True
)
```

### REASSIGN_TASK
**Purpose:** Intelligent task reassignment with state preservation

**Syntax:**
```bash
REASSIGN_TASK [task_id] [from_agent] [to_agent] [preserve_state]
```

**Parameters:**
- `task_id`: Unique task identifier
- `from_agent`: Original agent ID
- `to_agent`: Target agent ID
- `preserve_state`: Boolean for state preservation

**Features:**
- Agent Capability Matching
- State Transfer
- Dependency Validation
- Priority Adjustment
- Handoff Documentation
- Timeline Recalculation

**Example:**
```python
system.reassign_task(
    task_id="task_123",
    from_agent="agent_001",
    to_agent="agent_002",
    preserve_state=True
)
```

### HEARTBEAT
**Purpose:** Agent lifecycle and health monitoring

**Syntax:**
```bash
HEARTBEAT [agent_id] [status] [current_task] [progress]
```

**Parameters:**
- `agent_id`: Unique agent identifier
- `status`: Current agent status
- `current_task`: Active task ID
- `progress`: Task completion percentage

**Features:**
- Health Status Update
- Task Progress Reporting
- Capability Advertisement
- Resource Usage Tracking
- Error State Reporting
- Next Heartbeat Scheduling

**Timeouts:**
- Soft: 5 minutes
- Hard: 10 minutes
- Critical: 15 minutes

**Example:**
```python
agent.send_heartbeat(
    status="ACTIVE",
    current_task="task_456",
    progress=75
)
```

### WORK
**Purpose:** Intelligent task allocation with missing task detection

**Syntax:**
```bash
WORK [agent_id] [task_filter] [parallel_mode]
```

**Parameters:**
- `agent_id`: Agent requesting work
- `task_filter`: Filter criteria for tasks
- `parallel_mode`: Enable parallel execution

**Enhanced Features:**
- Pre-work missing task detection
- Objective completion check
- Cross-phase parallel task identification
- Agent capacity matching
- Dependency resolution
- Conflict detection

**Example:**
```python
agent.request_work(
    task_filter={"priority": "high"},
    parallel_mode=True
)
```

### STATUS
**Purpose:** Comprehensive system state reporting

**Syntax:**
```bash
STATUS [detail_level] [scope] [format]
```

**Parameters:**
- `detail_level`: Depth of status report
- `scope`: System areas to include
- `format`: Output format

**Enhanced Reporting:**
- Current objective progress
- Missing task analysis
- Promotion history
- Task completion velocity
- Auto-promotion readiness
- Detection patterns
- Future objective status

**Example:**
```python
system.get_status(
    detail_level="full",
    scope=["agents", "tasks", "resources"],
    format="json"
)
```

## Protocol Commands

### COORDINATE_AGENTS
**Purpose:** Multi-agent task coordination

**Syntax:**
```bash
COORDINATE_AGENTS [task_id] [agent_ids] [resource_list] [coordination_type]
```

**Features:**
- Task Distribution
- Resource Allocation
- Progress Tracking
- State Management
- Conflict Prevention
- Performance Optimization

### RESOLVE_CONFLICTS
**Purpose:** Resource and task conflict resolution

**Syntax:**
```bash
RESOLVE_CONFLICTS [conflict_id] [resolution_strategy] [priority_override]
```

**Features:**
- Conflict Analysis
- Strategy Selection
- Resource Reallocation
- State Recovery
- Impact Mitigation
- Resolution Verification

### SYNC_AGENTS
**Purpose:** State and resource synchronization

**Syntax:**
```bash
SYNC_AGENTS [agent_ids] [sync_scope] [force_level]
```

**Features:**
- State Verification
- Delta Identification
- Update Propagation
- Resource Alignment
- Version Control
- Conflict Resolution

## System Management Commands

### SYSTEM_HEALTH
**Purpose:** System health monitoring and maintenance

**Syntax:**
```bash
SYSTEM_HEALTH [check_level] [components] [repair]
```

**Features:**
- Component Status
- Resource Usage
- Error Detection
- Performance Metrics
- Auto-repair Options

### BACKUP_SYSTEM
**Purpose:** System state backup and recovery

**Syntax:**
```bash
BACKUP_SYSTEM [backup_type] [destination] [compression]
```

**Features:**
- State Preservation
- Configuration Backup
- Log Archive
- Recovery Points
- Verification Checks

## Best Practices

### Command Usage
1. Always check command prerequisites
2. Verify parameter values
3. Handle command output appropriately
4. Log command execution
5. Monitor command performance

### Error Handling
1. Implement proper error catching
2. Provide meaningful error messages
3. Handle timeout conditions
4. Maintain system stability
5. Log error details

### Performance
1. Use appropriate scan depths
2. Set reasonable timeouts
3. Optimize resource usage
4. Monitor system impact
5. Balance automation levels

## Command Development

### Creating Custom Commands
```python
class CustomCommand(BaseCommand):
    def execute(self, params):
        # Command implementation
        pass
```

### Command Integration
```python
system.register_command(
    command_name="CUSTOM_COMMAND",
    command_class=CustomCommand
)
```

### Command Testing
```python
def test_command():
    # Command test implementation
    pass
```

## Additional Resources
- [System Architecture](SYSTEM_ARCHITECTURE.md)
- [Protocol Reference](PROTOCOLS.md)
- [API Documentation](API.md)
- [Usage Examples](EXAMPLES.md)
