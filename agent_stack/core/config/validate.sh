#!/bin/bash

# Source environment configuration
source "$(dirname "$0")/environment.sh"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check directory
check_directory() {
    local dir_path="$1"
    local dir_name="$2"
    
    printf "Checking %-30s" "$dir_name..."
    
    if [[ ! -d "$dir_path" ]]; then
        echo -e "${RED}MISSING${NC}"
        return 1
    elif [[ ! -w "$dir_path" ]]; then
        echo -e "${YELLOW}NOT WRITABLE${NC}"
        return 2
    else
        echo -e "${GREEN}OK${NC}"
        return 0
    fi
}

# Function to check file
check_file() {
    local file_path="$1"
    local file_name="$2"
    
    printf "Checking %-30s" "$file_name..."
    
    if [[ ! -f "$file_path" ]]; then
        echo -e "${RED}MISSING${NC}"
        return 1
    elif [[ ! -r "$file_path" ]]; then
        echo -e "${YELLOW}NOT READABLE${NC}"
        return 2
    else
        echo -e "${GREEN}OK${NC}"
        return 0
    fi
}

# Function to check environment variable
check_env_var() {
    local var_name="$1"
    
    printf "Checking %-30s" "$var_name..."
    
    if [[ -z "${!var_name}" ]]; then
        echo -e "${RED}NOT SET${NC}"
        return 1
    else
        echo -e "${GREEN}SET${NC} (${!var_name})"
        return 0
    fi
}

echo "=== Warp Agent System Configuration Validation ==="
echo

echo "Environment Variables:"
check_env_var "WARP_HOST_DIR"
check_env_var "WARP_SYSTEM_DIR"
check_env_var "SYSTEM_DIR"

echo -e "\nPrimary Directories:"
check_directory "$SYSTEM_COMMANDS_DIR" "System Commands"
check_directory "$WORK_LOGS_DIR" "Work Logs"
check_directory "$SYSTEM_LOGS_DIR" "System Logs"
check_directory "$WARP_RULES_DIR" "Warp Rules"
check_directory "$CURRENT_OBJECTIVE_DIR" "Current Objective"
check_directory "$FUTURE_OBJECTIVES_DIR" "Future Objectives"
check_directory "$PAST_OBJECTIVES_DIR" "Past Objectives"
check_directory "$AGENT_STATUS_DIR" "Agent Status"
check_directory "$TASK_POOL_DIR" "Task Pool"
check_directory "$DEPENDENCIES_DIR" "Dependencies"
check_directory "$MISSING_TASKS_DIR" "Missing Tasks"
check_directory "$PROMOTION_QUEUE_DIR" "Promotion Queue"

echo -e "\nSecondary Directories:"
check_directory "$TEMPLATES_DIR" "Templates"
check_directory "$ARCHIVE_DIR" "Archive"
check_directory "$MASTERLOG_ARCHIVE_DIR" "Masterlog Archive"
check_directory "$EMERGENCY_BACKUP_DIR" "Emergency Backups"
check_directory "$CLOUD_SYNC_DIR" "Cloud Sync"
check_directory "$SIMULATION_DIR" "Simulation"
check_directory "$REMOTE_CACHE_DIR" "Remote Cache"

echo -e "\nCritical System Files:"
check_file "$MAIN_RULESET" "Main Ruleset"
check_file "$SYSTEM_DOCUMENTATION" "System Documentation"
check_file "$PATH_REGISTRY" "Path Registry"
check_file "$TIDY_LOG" "Tidy Log"
check_file "$ORGANIZE_LOG" "Organize Log"
check_file "$SYSTEM_STATUS" "System Status"
check_file "$ANOMALY_LOG" "Anomaly Log"
check_file "$SUPERVISOR_ALERTS" "Supervisor Alerts"
check_file "$AGENT_REGISTRY" "Agent Registry"
check_file "$MISSING_TASKS_LOG" "Missing Tasks Log"
check_file "$OBJECTIVE_PROMOTION_LOG" "Objective Promotion Log"
check_file "$AGENT_TIMEOUT_LOG" "Agent Timeout Log"
check_file "$TASK_REASSIGNMENT_LOG" "Task Reassignment Log"
check_file "$HEARTBEAT_MONITOR" "Heartbeat Monitor"

echo -e "\nPermissions Summary:"
echo "Directory permissions should be: 755 (drwxr-xr-x)"
echo "File permissions should be: 644 (rw-r--r--)"

echo -e "\nTo fix any permission issues, run:"
echo "chmod -R 755 \$SYSTEM_DIR"
echo "find \$SYSTEM_DIR -type f -exec chmod 644 {} \;"

echo -e "\nValidation complete. Address any issues marked in ${RED}RED${NC} or ${YELLOW}YELLOW${NC}."
