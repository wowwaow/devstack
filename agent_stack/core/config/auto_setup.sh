#!/bin/bash

# Auto-setup script for new installations
# This script handles automatic recreation of the devstack structure

# Get the user's home directory
USER_HOME="$(getent passwd $(whoami) | cut -d: -f6)"
DEVSTACK_DIR="$USER_HOME/devstack"

# Create directory structure
mkdir -p "$DEVSTACK_DIR/agent_stack/core/rules"

# Initialize git repository if not exists
if [[ ! -d "$DEVSTACK_DIR/.git" ]]; then
    cd "$DEVSTACK_DIR"
    git init
    git remote add origin https://github.com/user/devstack.git  # Replace with actual repo URL
fi

# Copy core files if they exist in the current location
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -d "$CURRENT_DIR/../.." ]]; then
    cp -r "$CURRENT_DIR/../../"* "$DEVSTACK_DIR/agent_stack/"
fi

# Set up environment variables
echo "export DEVSTACK_DIR=$DEVSTACK_DIR" >> "$USER_HOME/.bashrc"
echo "source $DEVSTACK_DIR/agent_stack/core/config/environment.sh" >> "$USER_HOME/.bashrc"

# Initialize the system
"$DEVSTACK_DIR/agent_stack/core/initialize.sh"

