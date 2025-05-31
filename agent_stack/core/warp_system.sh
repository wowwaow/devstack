#!/bin/bash
# Dynamic Multi-Agent AI System (WARP) Implementation
# Enhanced with environment variables for flexibility and portability

set -euo pipefail

# Source the core system configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config/environment.sh"

# Source the component modules
source "$SCRIPT_DIR/system/permissions.sh"
source "$SCRIPT_DIR/system/logging.sh"
source "$SCRIPT_DIR/system/agent_management.sh"
source "$SCRIPT_DIR/system/task_management.sh"
source "$SCRIPT_DIR/system/tool_management.sh"
source "$SCRIPT_DIR/system/monitoring.sh"
source "$SCRIPT_DIR/system/backup.sh"

# Import the main system operations
source "$SCRIPT_DIR/system/operations.sh"

# Execute the CLI interface
source "$SCRIPT_DIR/system/cli.sh"

# Run the main function with all arguments
main "$@"

