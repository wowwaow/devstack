#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Warp Agent System Initialization ===${NC}"
echo

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source environment configuration
echo "Sourcing environment configuration..."
source "$SCRIPT_DIR/config/environment.sh"

# Function to check if environment variables are set
check_environment() {
    if [[ -z "$WARP_HOST_DIR" ]]; then
        export WARP_HOST_DIR="/mnt/host"
        echo "Using default WARP_HOST_DIR: $WARP_HOST_DIR"
    else
        echo "Using WARP_HOST_DIR: $WARP_HOST_DIR"
    fi

    if [[ -z "$WARP_SYSTEM_DIR" ]]; then
        export WARP_SYSTEM_DIR="$WARP_HOST_DIR/WARP_CURRENT"
        echo "Using default WARP_SYSTEM_DIR: $WARP_SYSTEM_DIR"
    else
        echo "Using WARP_SYSTEM_DIR: $WARP_SYSTEM_DIR"
    fi
}

# Initialize environment
check_environment

# Run setup script
echo -e "\n${BLUE}Running system setup...${NC}"
"$SCRIPT_DIR/setup.sh"

# Run validation
echo -e "\n${BLUE}Validating system configuration...${NC}"
"$SCRIPT_DIR/config/validate.sh"

echo -e "\n${GREEN}Initialization complete!${NC}"
echo
echo "To use the system, ensure your environment is configured by running:"
echo "source $SCRIPT_DIR/config/environment.sh"
echo
echo "To validate the system at any time, run:"
echo "$SCRIPT_DIR/config/validate.sh"
