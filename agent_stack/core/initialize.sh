#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Warp Agent System Initialization ===${NC}"
echo

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function to check if environment variables are set
check_environment() {
    # Set HOME if not already set
    if [[ -z "$HOME" ]]; then
        export HOME="$(getent passwd $(whoami) | cut -d: -f6)"
        echo "Setting HOME directory: $HOME"
    fi

    # Set up devstack directory
    if [[ -z "$DEVSTACK_DIR" ]]; then
        export DEVSTACK_DIR="$HOME/devstack"
        echo "Setting DEVSTACK_DIR: $DEVSTACK_DIR"
    fi

    # Set up Warp directories
    if [[ -z "$WARP_HOST_DIR" ]]; then
        export WARP_HOST_DIR="/mnt/host"
        echo "Using default WARP_HOST_DIR: $WARP_HOST_DIR"
    fi

    if [[ -z "$WARP_SYSTEM_DIR" ]]; then
        export WARP_SYSTEM_DIR="$WARP_HOST_DIR/WARP_CURRENT"
        echo "Using default WARP_SYSTEM_DIR: $WARP_SYSTEM_DIR"
    fi

    # Ensure devstack directory exists
    if [[ ! -d "$DEVSTACK_DIR" ]]; then
        echo "Creating devstack directory structure..."
        mkdir -p "$DEVSTACK_DIR/agent_stack/core/rules"
        # Clone or copy necessary files
        if [[ -d "$SCRIPT_DIR" && "$SCRIPT_DIR" != "$DEVSTACK_DIR/agent_stack/core" ]]; then
            cp -r "$SCRIPT_DIR"/* "$DEVSTACK_DIR/agent_stack/core/"
        fi
    fi
}

# Initialize environment
check_environment

# Source environment configuration
echo "Sourcing environment configuration..."
source "$SCRIPT_DIR/config/environment.sh"

# Sync with devstack repository
echo -e "\n${BLUE}Syncing with devstack repository...${NC}"
"$SCRIPT_DIR/sync_rules.sh"

# Run setup script
echo -e "\n${BLUE}Running system setup...${NC}"
"$SCRIPT_DIR/setup.sh"

# Run validation
echo -e "\n${BLUE}Validating system configuration...${NC}"
"$SCRIPT_DIR/config/validate.sh"

# Setup auto-sync reminder
echo -e "\n${YELLOW}Important: Auto-sync has been configured${NC}"
echo "The system will automatically:"
echo "- Sync with devstack repository hourly"
echo "- Rebuild system as needed"
echo "- Maintain configuration across updates"

echo -e "\n${GREEN}Initialization complete!${NC}"
echo
echo "To use the system, ensure your environment is configured by running:"
echo "source $SCRIPT_DIR/config/environment.sh"
echo
echo "To manually sync with devstack at any time, run:"
echo "$SCRIPT_DIR/sync_rules.sh"
echo
echo "To validate the system at any time, run:"
echo "$SCRIPT_DIR/config/validate.sh"
