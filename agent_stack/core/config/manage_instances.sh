#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function to create new instance
create_instance() {
    local instance_name="$1"
    local base_dir="${2:-/mnt/host}"
    
    export WARP_HOST_DIR="$base_dir"
    export WARP_SYSTEM_DIR="$base_dir/$instance_name"
    
    echo -e "${BLUE}Creating new instance: $instance_name${NC}"
    echo "Base directory: $WARP_HOST_DIR"
    echo "System directory: $WARP_SYSTEM_DIR"
    
    source "$SCRIPT_DIR/environment.sh"
    "$SCRIPT_DIR/../initialize.sh"
}

# Function to list instances
list_instances() {
    local base_dir="${1:-/mnt/host}"
    
    echo -e "${BLUE}Available Instances in $base_dir:${NC}"
    echo
    
    for dir in "$base_dir"/*/; do
        if [ -d "$dir" ]; then
            instance_name=$(basename "$dir")
            if [ -f "$dir/System Commands/README.md" ]; then
                echo -e "${GREEN}✓${NC} $instance_name (Valid Warp Instance)"
            else
                echo -e "${YELLOW}?${NC} $instance_name (Unverified)"
            fi
        fi
    done
}

# Function to switch instance
switch_instance() {
    local instance_name="$1"
    local base_dir="${2:-/mnt/host}"
    
    local instance_dir="$base_dir/$instance_name"
    
    if [ ! -d "$instance_dir" ]; then
        echo -e "${RED}Error: Instance $instance_name not found${NC}"
        return 1
    fi
    
    export WARP_HOST_DIR="$base_dir"
    export WARP_SYSTEM_DIR="$instance_dir"
    
    echo -e "${BLUE}Switching to instance: $instance_name${NC}"
    source "$SCRIPT_DIR/environment.sh"
    "$SCRIPT_DIR/validate.sh"
}

# Function to delete instance
delete_instance() {
    local instance_name="$1"
    local base_dir="${2:-/mnt/host}"
    
    local instance_dir="$base_dir/$instance_name"
    
    if [ ! -d "$instance_dir" ]; then
        echo -e "${RED}Error: Instance $instance_name not found${NC}"
        return 1
    fi
    
    echo -e "${YELLOW}Warning: This will delete instance $instance_name${NC}"
    echo -e "${YELLOW}Directory to be deleted: $instance_dir${NC}"
    read -p "Are you sure? (y/N) " confirm
    
    if [[ $confirm =~ ^[Yy]$ ]]; then
        rm -rf "$instance_dir"
        echo -e "${GREEN}Instance $instance_name deleted${NC}"
    else
        echo "Operation cancelled"
    fi
}

# Show usage if no arguments provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <command> [options]"
    echo
    echo "Commands:"
    echo "  create <instance_name> [base_dir]  Create new instance"
    echo "  list [base_dir]                    List available instances"
    echo "  switch <instance_name> [base_dir]  Switch to instance"
    echo "  delete <instance_name> [base_dir]  Delete instance"
    echo
    echo "Examples:"
    echo "  $0 create dev_instance"
    echo "  $0 list"
    echo "  $0 switch prod_instance"
    echo "  $0 delete old_instance"
    exit 1
fi

# Parse commands
command="$1"
shift

case "$command" in
    create)
        if [ -z "$1" ]; then
            echo -e "${RED}Error: Instance name required${NC}"
            exit 1
        fi
        create_instance "$1" "$2"
        ;;
    list)
        list_instances "$1"
        ;;
    switch)
        if [ -z "$1" ]; then
            echo -e "${RED}Error: Instance name required${NC}"
            exit 1
        fi
        switch_instance "$1" "$2"
        ;;
    delete)
        if [ -z "$1" ]; then
            echo -e "${RED}Error: Instance name required${NC}"
            exit 1
        fi
        delete_instance "$1" "$2"
        ;;
    *)
        echo -e "${RED}Error: Unknown command $command${NC}"
        exit 1
        ;;
esac
