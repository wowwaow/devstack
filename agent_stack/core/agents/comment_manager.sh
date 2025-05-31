#!/bin/bash

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Import environment
source "$SCRIPT_DIR/../config/environment.sh"

# Function to add a comment
add_comment() {
    local agent_id="$1"
    local file_path="$2"
    local comment="$3"
    local line_number="$4"

    python3 - <<EOF
from agents.comments import AgentCommentSystem
acs = AgentCommentSystem()
acs.add_comment("$agent_id", "$file_path", "$comment", ${line_number:-None})
EOF
}

# Function to get comments for a file
get_file_comments() {
    local file_path="$1"

    python3 - <<EOF
from agents.comments import AgentCommentSystem
acs = AgentCommentSystem()
comments = acs.get_file_comments("$file_path")
import json
print(json.dumps(comments, indent=2))
EOF
}

# Function to get all comments from an agent
get_agent_comments() {
    local agent_id="$1"

    python3 - <<EOF
from agents.comments import AgentCommentSystem
acs = AgentCommentSystem()
comments = acs.get_agent_comments("$agent_id")
import json
print(json.dumps(comments, indent=2))
EOF
}

# If this script is run directly, show usage
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "Usage:"
    echo "  source ${BASH_SOURCE[0]}"
    echo "  add_comment <agent_id> <file_path> <comment> [line_number]"
    echo "  get_file_comments <file_path>"
    echo "  get_agent_comments <agent_id>"
fi

