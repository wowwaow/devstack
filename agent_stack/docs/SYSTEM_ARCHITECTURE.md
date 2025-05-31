# AI Agent Stack System Architecture

## System Overview
The AI Agent Stack uses a **single consolidated rule set**, a shared template library, and a series of persistent local files + system commands to coordinate multi-agent operations with intelligent task detection and automatic objective promotion.

## Directory Structure & File Hierarchy

### Core System Components
- `agent_stack/core/`
  - `rules/` → Governance and operational procedures
  - `objectives/` → Active, future, and past project phases
  - `agent_status/` → Per-agent heartbeat and status files
  - `task_pool/` → Active and pending task definitions
  - `dependencies/` → Cross-task and cross-objective dependency mapping
  - `missing_tasks/` → Detected missing tasks awaiting addition
  - `promotion_queue/` → Objectives ready for promotion tracking

### Critical System Files
- **Main ruleset** → `core/rules/README.md`
- **System documentation** → `docs/SYSTEM_ARCHITECTURE.md`
- **Path registry** → `core/rules/PATHS.md`
- **Agent registry** → `core/agent_status/AGENT_REGISTRY.csv`
- **Missing task log** → `logs/system_logs/MISSING_TASKS_LOG.md`
- **Objective promotion log** → `logs/system_logs/OBJECTIVE_PROMOTION_LOG.md`
- **Agent timeout log** → `logs/system_logs/AGENT_TIMEOUT_LOG.md`
- **Task reassignment log** → `logs/system_logs/TASK_REASSIGNMENT_LOG.md`
- **Agent heartbeat monitor** → `core/agent_status/HEARTBEAT_MONITOR.json`

## Agent Session Protocol

### Session Startup Sequence
1. **Identity Verification**
   - Confirm agent identity and session timestamp
   - Log session start in AGENT_REGISTRY.csv
   - Check for existing agent conflicts

2. **Rule Set Validation**
   - Read primary ruleset
   - Verify rule version compatibility
   - Cross-reference system architecture

3. **System Health Check**
   - Validate directory structure
   - Check file permissions
   - Verify template availability

4. **Missing Task Detection**
   - Scan current objective for gaps
   - Analyze dependencies
   - Auto-generate missing tasks
   - Update task pool

5. **Objective Completion Check**
   - Evaluate objective status
   - Execute promotion if complete
   - Archive completed objectives
   - Initialize new objectives

## Core Commands

### DETECT_MISSING_TASKS
- **Purpose:** AI-driven task detection and addition
- **Syntax:** `DETECT_MISSING_TASKS [objective_name] [scan_depth] [auto_add]`
- **Features:**
  - Pattern analysis
  - Dependency gap detection
  - Best practice scanning
  - Quality assurance verification
  - Auto-addition capability

### MONITOR_AGENTS
- **Purpose:** Agent heartbeat monitoring
- **Syntax:** `MONITOR_AGENTS [scan_interval] [timeout_threshold] [auto_reassign]`
- **Features:**
  - Continuous heartbeat tracking
  - Automatic timeout detection
  - Task state preservation
  - Intelligent reassignment

### HEARTBEAT
- **Purpose:** Agent lifecycle management
- **Syntax:** `HEARTBEAT [agent_id] [status] [current_task] [progress]`
- **Intervals:**
  - Soft Timeout: 5 minutes
  - Hard Timeout: 10 minutes
  - Critical Timeout: 15 minutes

## Agent Coordination Protocols

### Task Distribution Protocol
1. Analyze requirements
2. Evaluate agent capabilities
3. Calculate optimal distribution
4. Assign tasks
5. Monitor progress
6. Handle completion

### Resource Sharing Protocol
1. Register requirements
2. Check availability
3. Allocate resources
4. Monitor usage
5. Handle conflicts
6. Release resources

### State Synchronization Protocol
1. Collect agent states
2. Identify inconsistencies
3. Calculate updates
4. Distribute changes
5. Verify consistency
6. Log results

### Performance Monitoring
- Communication latency tracking
- Resource utilization metrics
- Task completion analysis
- Collaboration efficiency
- System synchronization overhead

[Additional protocol documentation continues...]
