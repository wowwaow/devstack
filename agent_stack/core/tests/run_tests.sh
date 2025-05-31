#!/bin/bash

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Warp Environment Tests ===${NC}"

# Source environment configuration
echo "Sourcing environment configuration..."
source "$SCRIPT_DIR/../config/environment.sh"

# Run Python tests
echo -e "\nRunning environment tests..."
"$SCRIPT_DIR/test_environment.py"

