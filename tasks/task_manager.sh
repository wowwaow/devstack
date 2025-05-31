#!/bin/bash
# Simple task viewer
set -e

help() {
    echo "Task Manager"
    echo "Usage: $0 <command> [args]"
    echo
    echo "Commands:"
    echo "  phase <phase>    List tasks in phase"
    echo "  info <task-id>   Show task info"
}

get_field() {
    local file=$1
    local field=$2
    sed -n "s/^[ ]*$field: \"\([^\"]*\)\".*/\1/p" "$file"
}

phase() {
    [ -z "$1" ] && { echo "Error: Phase required"; return 1; }
    echo "Tasks in phase $1:"
    echo "-------------------"
    find . -type f -name "*.yml" -exec grep -l "phase: \"$1\"" {} \; | sort | while read -r file; do
        echo "Task: $(get_field "$file" "task_id")"
        echo "Name: $(get_field "$file" "name")"
        echo "Status: $(get_field "$file" "status")"
        if grep -q "^[ ]*dependencies:" "$file"; then
            echo "Dependencies:"
            deps=$(sed -n '/^[ ]*dependencies:/,/^[^ ]/p' "$file" | grep "task_id:" | sed 's/.*"\([^"]*\)".*/  \1/')
            [ -n "$deps" ] && echo "$deps"
        fi
        echo
    done
}

info() {
    [ -z "$1" ] && { echo "Error: Task ID required"; return 1; }
    file=$(find . -type f -name "*.yml" -exec grep -l "task_id: \"$1\"" {} \; | head -n 1)
    [ -z "$file" ] && { echo "Error: Task not found"; return 1; }
    
    echo "Task Details:"
    echo "-------------------"
    echo "ID: $1"
    echo "Name: $(get_field "$file" "name")"
    echo "Status: $(get_field "$file" "status")"
    echo "Phase: $(get_field "$file" "phase")"
    echo "Priority: $(get_field "$file" "priority")"
    
    if grep -q "^[ ]*dependencies:" "$file"; then
        echo "Dependencies:"
        deps=$(sed -n '/^[ ]*dependencies:/,/^[^ ]/p' "$file" | grep "task_id:" | sed 's/.*"\([^"]*\)".*/  \1/')
        [ -n "$deps" ] && echo "$deps"
    fi
}

case $1 in
    phase) phase "$2" ;;
    info) info "$2" ;;
    *) help ;;
esac
