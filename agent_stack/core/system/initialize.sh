#!/bin/bash

initialize_directory_structure() {
    log_info "Initializing WARP system directory structure..."
    
    # Create all primary directories
    local directories=(
        "$SYSTEM_DIR"
        "$TEMPLATES_DIR"
        "$ARCHIVE_DIR"
        "$BACKUP_DIR"
        "$SYSTEM_COMMANDS_DIR"
        "$WORK_LOGS_DIR"
        "$SYSTEM_LOGS_DIR"
        "$WARP_RULES_DIR"
        "$CURRENT_OBJECTIVE_DIR"
        "$FUTURE_OBJECTIVES_DIR"
        "$PAST_OBJECTIVES_DIR"
        "$AGENT_STATUS_DIR"
        "$TASK_POOL_DIR"
        "$DEPENDENCIES_DIR"
        "$MISSING_TASKS_DIR"
        "$PROMOTION_QUEUE_DIR"
        "$INSTALLED_TOOLS_DIR"
    )
    
    for dir in "${directories[@]}"; do
        ensure_directory_permissions "$dir"
    done
    
    log_success "Directory structure initialized successfully"
}

initialize_system_files() {
    log_info "Initializing critical system files..."
    
    # Initialize permission audit log with header
    ensure_file_exists "$PERMISSION_AUDIT_LOG" "# Permission Audit Log
| Timestamp | Type | Path | Action |
|-----------|------|------|--------|"

    # Initialize agent registry
    ensure_file_exists "$AGENT_REGISTRY" "agent_id,status,last_heartbeat,current_task,assigned_objectives
supervisor,active,$(date -Iseconds),system_monitoring,system_oversight"

    # Initialize heartbeat monitor
    ensure_file_exists "$HEARTBEAT_MONITOR" '{
  "last_updated": "'$(date -Iseconds)'",
  "agents": {
    "supervisor": {
      "status": "active",
      "last_heartbeat": "'$(date -Iseconds)'",
      "health": "healthy"
    }
  }
}'

    # Initialize tools registry
    ensure_file_exists "$TOOLS_REGISTRY" '{
  "installed_tools": {},
  "last_updated": "'$(date -Iseconds)'",
  "installation_count": 0
}'

    # Initialize main ruleset if not using devstack rules
    if [[ ! -f "$WARP_RULES_SOURCE/README.md" ]]; then
        ensure_file_exists "$MAIN_RULESET" "# WARP System Rules

## Core Principles
1. All operations must maintain system integrity
2. Agent communication follows defined protocols
3. Task dependencies must be resolved before execution
4. System logs must be maintained for all operations

## Directory Structure
- System Directory: $SYSTEM_DIR
- Templates: $TEMPLATES_DIR
- Archive: $ARCHIVE_DIR

## Agent Responsibilities
- Each agent must maintain heartbeat
- Task completion must be logged
- Anomalies must be reported to supervisor

## Last Updated
$(date)"
    fi

    log_success "System files initialized successfully"
}

