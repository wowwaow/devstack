#!/bin/bash

create_system_backup() {
    local backup_name="${1:-backup_$(date +%Y%m%d_%H%M%S)}"
    local backup_path="$BACKUP_DIR/$backup_name"
    
    ensure_directory_permissions "$BACKUP_DIR"
    
    log_info "Creating system backup: $backup_name"
    
    # Create backup directory
    mkdir -p "$backup_path"
    
    # Copy critical system files
    cp -r "$SYSTEM_LOGS_DIR" "$backup_path/" 2>/dev/null || true
    cp -r "$AGENT_STATUS_DIR" "$backup_path/" 2>/dev/null || true
    cp -r "$WARP_RULES_DIR" "$backup_path/" 2>/dev/null || true
    cp -r "$CURRENT_OBJECTIVE_DIR" "$backup_path/" 2>/dev/null || true
    
    # Create backup manifest
    cat > "$backup_path/MANIFEST.md" << EOF
# Backup Manifest

## Backup Information
- **Name**: $backup_name
- **Created**: $(date)
- **System Directory**: $SYSTEM_DIR
- **Host Directory**: $WARP_HOST_DIR

## Contents
- System Logs
- Agent Status
- Warp Rules
- Current Objectives

## System State
- Active Agents: $(wc -l < "$AGENT_REGISTRY" 2>/dev/null || echo "0")
- Total Tasks: $(find "$TASK_POOL_DIR" -name "*.md" -type f 2>/dev/null | wc -l || echo "0")
EOF

    ensure_directory_permissions "$backup_path"
    log_success "Backup created: $backup_path"
}

