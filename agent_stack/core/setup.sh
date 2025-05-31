#!/bin/bash

# Source environment configuration
source "$(dirname "$0")/config/environment.sh"

# Function to create directory with proper permissions
create_directory() {
    local dir_path="$1"
    local dir_name="$2"
    
    echo "Creating $dir_name..."
    mkdir -p "$dir_path"
    chmod 755 "$dir_path"
    echo "✓ Created $dir_name at $dir_path"
}

# Function to create file with proper permissions
create_file() {
    local file_path="$1"
    local file_name="$2"
    
    echo "Creating $file_name..."
    touch "$file_path"
    chmod 644 "$file_path"
    echo "✓ Created $file_name at $file_path"
}

echo "=== Warp Agent System Setup ==="
echo "Using configuration:"
echo "WARP_HOST_DIR: $WARP_HOST_DIR"
echo "WARP_SYSTEM_DIR: $WARP_SYSTEM_DIR"
echo

# Create primary system directories
echo "Creating primary system directories..."
create_directory "$SYSTEM_COMMANDS_DIR" "System Commands"
create_directory "$WORK_LOGS_DIR" "Work Logs"
create_directory "$SYSTEM_LOGS_DIR" "System Logs"
create_directory "$WARP_RULES_DIR" "Warp Rules"
create_directory "$CURRENT_OBJECTIVE_DIR" "Current Objective"
create_directory "$FUTURE_OBJECTIVES_DIR" "Future Objectives"
create_directory "$PAST_OBJECTIVES_DIR" "Past Objectives"
create_directory "$AGENT_STATUS_DIR" "Agent Status"
create_directory "$TASK_POOL_DIR" "Task Pool"
create_directory "$DEPENDENCIES_DIR" "Dependencies"
create_directory "$MISSING_TASKS_DIR" "Missing Tasks"
create_directory "$PROMOTION_QUEUE_DIR" "Promotion Queue"

# Create secondary directories
echo -e "\nCreating secondary directories..."
create_directory "$TEMPLATES_DIR" "Templates"
create_directory "$ARCHIVE_DIR" "Archive"
create_directory "$MASTERLOG_ARCHIVE_DIR" "Masterlog Archive"
create_directory "$EMERGENCY_BACKUP_DIR" "Emergency Backups"
create_directory "$CLOUD_SYNC_DIR" "Cloud Sync"
create_directory "$SIMULATION_DIR" "Simulation"
create_directory "$REMOTE_CACHE_DIR" "Remote Cache"

# Create system files
echo -e "\nCreating system files..."
create_file "$MAIN_RULESET" "Main Ruleset"
create_file "$SYSTEM_DOCUMENTATION" "System Documentation"
create_file "$PATH_REGISTRY" "Path Registry"
create_file "$TIDY_LOG" "Tidy Log"
create_file "$ORGANIZE_LOG" "Organize Log"
create_file "$SYSTEM_STATUS" "System Status"
create_file "$ANOMALY_LOG" "Anomaly Log"
create_file "$SUPERVISOR_ALERTS" "Supervisor Alerts"
create_file "$AGENT_REGISTRY" "Agent Registry"
create_file "$MISSING_TASKS_LOG" "Missing Tasks Log"
create_file "$OBJECTIVE_PROMOTION_LOG" "Objective Promotion Log"
create_file "$AGENT_TIMEOUT_LOG" "Agent Timeout Log"
create_file "$TASK_REASSIGNMENT_LOG" "Task Reassignment Log"
create_file "$HEARTBEAT_MONITOR" "Heartbeat Monitor"

echo -e "\n=== Setup Complete ==="
echo "To verify the installation, run:"
echo "ls -la \$SYSTEM_DIR"
echo
echo "To start using the system, ensure your environment is configured by running:"
echo "source $(dirname "$0")/config/environment.sh"
