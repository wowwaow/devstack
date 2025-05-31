#!/bin/bash

# Dynamic Multi-Agent AI System (WARP) Implementation
# Enhanced with environment variables for flexibility and portability

set -euo pipefail

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source the core system configuration
source "$SCRIPT_DIR/config/environment.sh"

# Source the component modules
source "$SCRIPT_DIR/system/permissions.sh"
source "$SCRIPT_DIR/system/logging.sh"
source "$SCRIPT_DIR/system/agent_management.sh"
source "$SCRIPT_DIR/system/task_management.sh"
source "$SCRIPT_DIR/system/tool_management.sh"
source "$SCRIPT_DIR/system/monitoring.sh"
source "$SCRIPT_DIR/system/backup.sh"
source "$SCRIPT_DIR/system/operations.sh"

# Main command dispatcher
main() {
    case "${1:-help}" in
        start)
            start_system
            ;;
        stop)
            stop_system
            ;;
        status)
            if [[ -f "$SYSTEM_STATUS" ]]; then
                cat "$SYSTEM_STATUS"
            else
                log_error "System not initialized. Run '$0 start' first."
            fi
            ;;
        health)
            system_health_check
            ;;
        register_agent)
            if [[ $# -lt 2 ]]; then
                log_error "Usage: $0 register_agent <agent_id> [status]"
                exit 1
            fi
            register_agent "$2" "${3:-inactive}"
            ;;
        agent_status)
            if [[ $# -lt 2 ]]; then
                log_error "Usage: $0 agent_status <agent_id>"
                exit 1
            fi
            status=$(get_agent_status "$2")
            echo "Agent $2 status: $status"
            ;;
        heartbeat)
            if [[ $# -lt 2 ]]; then
                log_error "Usage: $0 heartbeat <agent_id>"
                exit 1
            fi
            update_agent_heartbeat "$2"
            ;;
        create_task)
            if [[ $# -lt 3 ]]; then
                log_error "Usage: $0 create_task <task_id> <description> [agent] [priority]"
                exit 1
            fi
            create_task "$2" "$3" "${4:-unassigned}" "${5:-medium}"
            ;;
        assign_task)
            if [[ $# -lt 3 ]]; then
                log_error "Usage: $0 assign_task <agent_id> <task_id>"
                exit 1
            fi
            assign_task_to_agent "$2" "$3"
            ;;
        install_tool)
            if [[ $# -lt 2 ]]; then
                log_error "Usage: $0 install_tool <tool_name> [method]"
                exit 1
            fi
            install_tool "$2" "${3:-auto}"
            ;;
        backup)
            create_system_backup "${2:-backup_$(date +%Y%m%d_%H%M%S)}"
            ;;
        help|--help|-h)
            cat << EOF
WARP Multi-Agent AI System - Dynamic Implementation

USAGE:
    $0 <command> [arguments]

COMMANDS:
    start                           - Initialize and start the WARP system
    stop                            - Gracefully stop the WARP system
    status                          - Show system status
    health                          - Perform health check
    
    register_agent <id> [status]    - Register a new agent
    agent_status <id>               - Get agent status
    heartbeat <id>                  - Update agent heartbeat
    
    create_task <id> <desc> [agent] - Create a new task
    assign_task <agent> <task>      - Assign task to agent
    
    install_tool <name> [method]    - Install a tool
    backup [name]                   - Create system backup
    
    help                            - Show this help message

ENVIRONMENT VARIABLES:
    WARP_HOST_DIR      - Base host directory (default: /mnt/host)
    WARP_SYSTEM_DIR    - System directory (default: \$WARP_HOST_DIR/WARP_CURRENT)
    WARP_USER          - System user (default: ubuntu)
    WARP_GROUP         - System group (default: ubuntu)

For more information, see the documentation in the Warp_Rules directory.
