#!/bin/bash

start_system() {
    log_info "Starting WARP Multi-Agent AI System..."
    log_info "System Directory: $SYSTEM_DIR"
    log_info "Host Directory: $WARP_HOST_DIR"
    
    # Initialize system
    initialize_directory_structure
    initialize_system_files
    
    # Register supervisor agent
    register_agent "supervisor" "active" "system_oversight"
    
    # Perform initial health check
    system_health_check
    
    # Create initial backup
    create_system_backup "initial_backup"
    
    update_system_status "System Startup" "COMPLETE"
    log_success "WARP system started successfully!"
}

stop_system() {
    log_info "Stopping WARP system..."
    
    # Create final backup
    create_system_backup "shutdown_backup"
    
    # Update all agents to inactive
    if [[ -f "$AGENT_REGISTRY" ]]; then
        sed -i 's/,active,/,inactive,/g' "$AGENT_REGISTRY"
    fi
    
    update_system_status "System Shutdown" "COMPLETE"
    log_success "WARP system stopped successfully"
}

