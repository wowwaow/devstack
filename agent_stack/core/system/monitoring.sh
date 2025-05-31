#!/bin/bash

system_health_check() {
    local issues=0
    
    log_info "Performing system health check..."
    
    # Check directory permissions
    local critical_dirs=("$SYSTEM_DIR" "$SYSTEM_LOGS_DIR" "$AGENT_STATUS_DIR")
    for dir in "${critical_dirs[@]}"; do
        if ! verify_directory_access "$dir"; then
            log_error "Directory access issue: $dir"
            ((issues++))
        fi
    done
    
    # Check critical files
    local critical_files=("$AGENT_REGISTRY" "$SYSTEM_STATUS" "$HEARTBEAT_MONITOR")
    for file in "${critical_files[@]}"; do
        if [[ -f "$file" ]] && ! verify_file_access "$file"; then
            log_error "File access issue: $file"
            ((issues++))
        fi
    done
    
    # Check disk space
    local disk_usage=$(df "$WARP_HOST_DIR" | tail -1 | awk '{print $5}' | sed 's/%//')
    if [[ $disk_usage -gt 90 ]]; then
        log_warn "Disk usage high: ${disk_usage}%"
        ((issues++))
    fi
    
    # Update system status
    local health_status="HEALTHY"
    if [[ $issues -gt 0 ]]; then
        health_status="ISSUES_DETECTED"
    fi
    
    update_system_status "Health Check" "$health_status - $issues issues found"
    
    log_info "Health check completed: $issues issues found"
    return $issues
}

update_system_status() {
    local operation="$1"
    local status="$2"
    local timestamp=$(date)
    
    ensure_file_exists "$SYSTEM_STATUS"
    
    # Append status update
    cat >> "$SYSTEM_STATUS" << EOF

## Status Update - $timestamp
- **Operation**: $operation
- **Status**: $status
- **System Directory**: $SYSTEM_DIR
- **Active Agents**: $(wc -l < "$AGENT_REGISTRY" 2>/dev/null || echo "0")

EOF

    log_info "System status updated: $operation - $status"
}

