#!/bin/bash

register_agent() {
    local agent_id="$1"
    local initial_status="${2:-inactive}"
    local assigned_objectives="${3:-none}"
    
    ensure_file_exists "$AGENT_REGISTRY"
    
    # Check if agent already exists
    if grep -q "^$agent_id," "$AGENT_REGISTRY"; then
        log_warn "Agent $agent_id already registered, updating status"
        # Update existing agent
        sed -i "s/^$agent_id,.*/$agent_id,$initial_status,$(date -Iseconds),none,$assigned_objectives/" "$AGENT_REGISTRY"
    else
        # Add new agent
        echo "$agent_id,$initial_status,$(date -Iseconds),none,$assigned_objectives" >> "$AGENT_REGISTRY"
        log_info "Registered new agent: $agent_id"
    fi
    
    # Update heartbeat monitor
    update_agent_heartbeat "$agent_id" "$initial_status"
}

update_agent_heartbeat() {
    local agent_id="$1"
    local status="${2:-active}"
    local current_time=$(date -Iseconds)
    
    ensure_file_exists "$HEARTBEAT_MONITOR"
    
    # Update JSON using jq if available, otherwise use sed
    if command -v jq &> /dev/null; then
        jq --arg agent "$agent_id" --arg status "$status" --arg time "$current_time" \
           '.last_updated = $time | .agents[$agent] = {
               "status": $status,
               "last_heartbeat": $time,
               "health": "healthy"
           }' "$HEARTBEAT_MONITOR" > "${HEARTBEAT_MONITOR}.tmp" && \
           mv "${HEARTBEAT_MONITOR}.tmp" "$HEARTBEAT_MONITOR"
    else
        log_warn "jq not available, using basic heartbeat update"
        echo "Agent $agent_id heartbeat: $current_time" >> "$SYSTEM_LOGS_DIR/heartbeat_simple.log"
    fi
    
    log_info "Updated heartbeat for agent: $agent_id"
}

get_agent_status() {
    local agent_id="$1"
    ensure_file_exists "$AGENT_REGISTRY"
    
    grep "^$agent_id," "$AGENT_REGISTRY" | cut -d',' -f2
}

