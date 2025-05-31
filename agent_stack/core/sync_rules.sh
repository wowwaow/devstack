#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source environment configuration
source "$SCRIPT_DIR/config/environment.sh"

# Function to sync devstack with rules
sync_devstack() {
    echo -e "${BLUE}Syncing devstack with rules directory...${NC}"
    
    # Create temporary directory for git operations
    TEMP_DIR=$(mktemp -d)
    
    # Clone or update devstack repository
    if [ -d "$WARP_RULES_DIR/.git" ]; then
        echo "Updating existing devstack repository..."
        cd "$WARP_RULES_DIR"
        git pull origin main
    else
        echo "Cloning devstack repository..."
        git clone https://github.com/wowwaow/devstack.git "$TEMP_DIR"
        
        # Ensure rules directory exists
        mkdir -p "$WARP_RULES_DIR"
        
        # Copy rules and configuration
        cp -r "$TEMP_DIR/agent_stack/core/rules/"* "$WARP_RULES_DIR/"
        cp -r "$TEMP_DIR/agent_stack/core/config" "$WARP_RULES_DIR/"
        
        # Initialize git in rules directory
        cd "$WARP_RULES_DIR"
        git init
        git remote add origin https://github.com/wowwaow/devstack.git
        git fetch
        git checkout main
    fi
    
    # Clean up temporary directory
    rm -rf "$TEMP_DIR"
    
    echo -e "${GREEN}Sync completed!${NC}"
}

# Function to rebuild system from rules
rebuild_system() {
    echo -e "${BLUE}Rebuilding system from rules...${NC}"
    
    # Source updated environment configuration
    source "$WARP_RULES_DIR/config/environment.sh"
    
    # Run initialization script
    "$SCRIPT_DIR/initialize.sh"
    
    echo -e "${GREEN}System rebuild completed!${NC}"
}

# Main execution
echo -e "${BLUE}=== Warp System Auto-Sync ====${NC}"

# Check if WARP_RULES_DIR is set
if [ -z "$WARP_RULES_DIR" ]; then
    echo -e "${RED}Error: WARP_RULES_DIR not set${NC}"
    exit 1
fi

# Sync devstack
sync_devstack

# Rebuild system
rebuild_system

# Set up automatic sync (via cron)
setup_auto_sync() {
    # Create sync script in user's home directory
    SYNC_SCRIPT="$HOME/warp_sync.sh"
    
    echo '#!/bin/bash' > "$SYNC_SCRIPT"
    echo "export WARP_HOST_DIR=\"$WARP_HOST_DIR\"" >> "$SYNC_SCRIPT"
    echo "export WARP_SYSTEM_DIR=\"$WARP_SYSTEM_DIR\"" >> "$SYNC_SCRIPT"
    echo "$SCRIPT_DIR/sync_rules.sh" >> "$SYNC_SCRIPT"
    
    chmod +x "$SYNC_SCRIPT"
    
    # Add to crontab if not already present
    if ! crontab -l | grep -q "warp_sync.sh"; then
        (crontab -l 2>/dev/null; echo "0 * * * * $SYNC_SCRIPT") | crontab -
        echo -e "${GREEN}Automatic hourly sync configured${NC}"
    fi
}

# Setup automatic sync
setup_auto_sync

echo -e "\n${GREEN}System is ready and will automatically sync with devstack repository${NC}"
echo "Manual sync can be triggered by running: $0"
