#!/bin/bash

create_task() {
    local task_id="$1"
    local task_description="$2"
    local assigned_agent="${3:-unassigned}"
    local priority="${4:-medium}"
    local dependencies="${5:-none}"
    
    local task_file="$TASK_POOL_DIR/${task_id}.md"
    
    ensure_directory_permissions "$TASK_POOL_DIR"
    
    cat > "$task_file" << EOF
# Task: $task_id

## Description
$task_description

## Assignment
- **Assigned Agent**: $assigned_agent
- **Priority**: $priority
- **Status**: pending
- **Created**: $(date)

## Dependencies
$dependencies

## Progress Log
- Created: $(date)

## Notes
Task created via WARP system
EOF

    ensure_file_permissions "$task_file"
    log_info "Created task: $task_id"
    
    # Update agent registry if assigned
    if [[ "$assigned_agent" != "unassigned" ]]; then
        assign_task_to_agent "$assigned_agent" "$task_id"
    fi
}

assign_task_to_agent() {
    local agent_id="$1"
    local task_id="$2"
    
    ensure_file_exists "$AGENT_REGISTRY"
    
    # Update agent's current task
    sed -i "s/^$agent_id,\([^,]*\),\([^,]*\),[^,]*,\(.*\)/$agent_id,\1,\2,$task_id,\3/" "$AGENT_REGISTRY"
    
    log_info "Assigned task $task_id to agent $agent_id"
}

