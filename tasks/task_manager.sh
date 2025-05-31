#!/bin/bash

# Task Management Utility Script
# Provides command-line functionality for managing tasks in the devstack system

set -e

TASK_ROOT="/home/ubuntu/devstack/tasks"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

usage() {
    echo "Task Management Utility"
    echo
    echo "Usage: $0 <command> [options]"
    echo
    echo "Commands:"
    echo "  status <task-id>                     Show task status and details"
    echo "  update-status <task-id> <status>     Update task status"
    echo "  dependencies <task-id>               Show task dependencies"
    echo "  blocked-by <task-id>                 Show tasks blocking this task"
    echo "  blocks <task-id>                     Show tasks blocked by this task"
    echo "  validate <task-id>                   Show validation requirements"
    echo "  ready <task-id>                      Check if task is ready to start"
    echo "  progress <task-id> <percentage>      Update task progress"
    echo "  assign <task-id> <username>          Assign task to user"
    echo "  list-phase <phase>                   List tasks in specific phase"
    echo "  list-status <status>                 List tasks with specific status"
    echo "  dependency-chain <task-id>           Show full dependency chain for task"
    echo "  critical-path                        Show critical paths through tasks"
    echo "  progress-summary                     Show overall project progress"
    echo
    echo "Statuses: PENDING, IN_PROGRESS, BLOCKED, FAILED, COMPLETED"
    echo "Phases: INITIALIZATION, BUILD, SYSTEM, QA, CORE"
}

validate_status_transition() {
    local current_status=$1
    local new_status=$2
    
    case $current_status in
        PENDING)
            case $new_status in
                IN_PROGRESS|BLOCKED) return 0;;
                *) return 1;;
            esac
            ;;
        IN_PROGRESS)
            case $new_status in
                COMPLETED|BLOCKED|FAILED) return 0;;
                *) return 1;;
            esac
            ;;
        BLOCKED)
            case $new_status in
                IN_PROGRESS|FAILED) return 0;;
                *) return 1;;
            esac
            ;;
        FAILED)
            case $new_status in
                IN_PROGRESS) return 0;;
                *) return 1;;
            esac
            ;;
        COMPLETED)
            case $new_status in
                IN_PROGRESS) return 0;;
                *) return 1;;
            esac
            ;;
        *)
            return 1
            ;;
    esac
}

find_task_file() {
    local task_id=$1
    local file=""
    case $task_id in
        TASK-[1-3]*)
            phase_num=${task_id#TASK-}
            phase_num=${phase_num%%.*}
            file=$(find "$TASK_ROOT/lfs_builder/phase${phase_num}_environment" \
                       "$TASK_ROOT/lfs_builder/phase${phase_num}_temp_tools" \
                       "$TASK_ROOT/lfs_builder/phase${phase_num}_system" \
                       2>/dev/null | grep -i "${task_id##*-}")
            ;;
        TASK-QA*)
            file=$(find "$TASK_ROOT/lfs_builder/qa" -type f | grep -i "${task_id##*-}")
            ;;
        TASK-RM*)
            file=$(find "$TASK_ROOT/core_implementation/resource_management" -type f | grep -i "${task_id##*-}")
            ;;
        TASK-EH*)
            file=$(find "$TASK_ROOT/core_implementation/error_handling" -type f | grep -i "${task_id##*-}")
            ;;
        TASK-TI*)
            file=$(find "$TASK_ROOT/core_implementation/testing" -type f | grep -i "${task_id##*-}")
            ;;
        TASK-MT*)
            file=$(find "$TASK_ROOT/core_implementation/monitoring" -type f | grep -i "${task_id##*-}")
            ;;
        TASK-DOC*)
            file=$(find "$TASK_ROOT/core_implementation/documentation" -type f | grep -i "${task_id##*-}")
            ;;
    esac

    if [ -z "$file" ]; then
        file=$(find "$TASK_ROOT" -type f -name "*.yml" -exec grep -l "task_id: \"$task_id\"" {} \;)
    fi

    echo "$file"
}

show_progress_summary() {
    echo -e "${BLUE}Project Progress Summary:${NC}"
    echo "----------------------------------------"
    
    local total_tasks=0
    local completed_tasks=0
    local in_progress_tasks=0
    local blocked_tasks=0
    local pending_tasks=0
    local failed_tasks=0
    
    while read -r file; do
        ((total_tasks++))
        local status=$(grep "status:" "$file" | cut -d'"' -f2)
        case $status in
            COMPLETED) ((completed_tasks++));;
            IN_PROGRESS) ((in_progress_tasks++));;
            BLOCKED) ((blocked_tasks++));;
            PENDING) ((pending_tasks++));;
            FAILED) ((failed_tasks++));;
        esac
    done < <(find "$TASK_ROOT" -type f -name "*.yml" -exec grep -l "task_id:" {} \;)
    
    local completed_pct=$(( completed_tasks * 100 / total_tasks ))
    local in_progress_pct=$(( in_progress_tasks * 100 / total_tasks ))
    local blocked_pct=$(( blocked_tasks * 100 / total_tasks ))
    local pending_pct=$(( pending_tasks * 100 / total_tasks ))
    local failed_pct=$(( failed_tasks * 100 / total_tasks ))
    
    echo "Total Tasks: $total_tasks"
    echo -e "${GREEN}Completed: $completed_tasks ($completed_pct%)${NC}"
    echo -e "${BLUE}In Progress: $in_progress_tasks ($in_progress_pct%)${NC}"
    echo -e "${YELLOW}Blocked: $blocked_tasks ($blocked_pct%)${NC}"
    echo -e "${BLUE}Pending: $pending_tasks ($pending_pct%)${NC}"
    echo -e "${RED}Failed: $failed_tasks ($failed_pct%)${NC}"
    
    echo -e "\nProgress by Phase:"
    for phase in INITIALIZATION BUILD SYSTEM QA CORE; do
        local phase_total=0
        local phase_completed=0
        while read -r file; do
            ((phase_total++))
            local status=$(grep "status:" "$file" | cut -d'"' -f2)
            if [ "$status" = "COMPLETED" ]; then
                ((phase_completed++))
            fi
        done < <(find "$TASK_ROOT" -type f -name "*.yml" -exec grep -l "phase: \"$phase\"" {} \;)
        
        if [ $phase_total -gt 0 ]; then
            local phase_pct=$(( phase_completed * 100 / phase_total ))
            echo "$phase: $phase_completed/$phase_total ($phase_pct%)"
        fi
    done
}

show_status() {
    local task_id=$1
    local file=$(find_task_file "$task_id")
    
    if [ -z "$file" ]; then
        echo -e "${RED}Task $task_id not found${NC}"
        return 1
    fi

    echo -e "${BLUE}Task Details for $task_id:${NC}"
    echo "----------------------------------------"
    grep -A 1 "name:" "$file"
    grep -A 1 "status:" "$file"
    grep -A 1 "priority:" "$file"
    grep -A 1 "phase:" "$file"
    echo "----------------------------------------"
    grep -A 2 "metadata:" "$file"
}

update_status() {
    local task_id=$1
    local new_status=$2
    local file=$(find_task_file "$task_id")
    
    if [ -z "$file" ]; then
        echo -e "${RED}Task $task_id not found${NC}"
        return 1
    fi

    local current_status=$(grep "status:" "$file" | cut -d'"' -f2)

    if ! validate_status_transition "$current_status" "$new_status"; then
        echo -e "${RED}Invalid status transition: $current_status -> $new_status${NC}"
        echo "Valid transitions from $current_status:"
        case $current_status in
            PENDING) echo "  -> IN_PROGRESS, BLOCKED";;
            IN_PROGRESS) echo "  -> COMPLETED, BLOCKED, FAILED";;
            BLOCKED) echo "  -> IN_PROGRESS, FAILED";;
            FAILED) echo "  -> IN_PROGRESS";;
            COMPLETED) echo "  -> IN_PROGRESS";;
        esac
        return 1
    fi

    sed -i "s/status: .*/status: \"$new_status\"/" "$file"
    sed -i "s/last_updated: .*/last_updated: \"$TIMESTAMP\"/" "$file"
    echo -e "${GREEN}Updated status of $task_id from $current_status to $new_status${NC}"
}

show_dependencies() {
    local task_id=$1
    local file=$(find_task_file "$task_id")
    
    if [ -z "$file" ]; then
        echo -e "${RED}Task $task_id not found${NC}"
        return 1
    fi

    echo -e "${BLUE}Dependencies for $task_id:${NC}"
    echo "----------------------------------------"
    grep -A 5 "dependencies:" "$file"
}

show_blocked_by() {
    local task_id=$1
    echo -e "${BLUE}Tasks blocking $task_id:${NC}"
    echo "----------------------------------------"
    find "$TASK_ROOT" -type f -name "*.yml" -exec grep -l "blocks.*$task_id" {} \;
}

show_blocks() {
    local task_id=$1
    local file=$(find_task_file "$task_id")
    
    if [ -z "$file" ]; then
        echo -e "${RED}Task $task_id not found${NC}"
        return 1
    fi

    echo -e "${BLUE}Tasks blocked by $task_id:${NC}"
    echo "----------------------------------------"
    grep -A 5 "blocks:" "$file"
}

show_validation() {
    local task_id=$1
    local file=$(find_task_file "$task_id")
    
    if [ -z "$file" ]; then
        echo -e "${RED}Task $task_id not found${NC}"
        return 1
    fi

    echo -e "${BLUE}Validation requirements for $task_id:${NC}"
    echo "----------------------------------------"
    grep -A 5 "validation_requirements:" "$file"
}

check_ready() {
    local task_id=$1
    local file=$(find_task_file "$task_id")
    
    if [ -z "$file" ]; then
        echo -e "${RED}Task $task_id not found${NC}"
        return 1
    fi

    local deps=$(grep -A 5 "dependencies:" "$file")
    if [ -z "$deps" ] || [ "$deps" == "dependencies: []" ]; then
        echo -e "${GREEN}Task $task_id has no dependencies and is ready to start${NC}"
        return 0
    fi

    echo -e "${YELLOW}Checking dependencies for $task_id...${NC}"
    while read -r dep; do
        if [[ $dep =~ task_id:.[A-Z]+-[0-9]+.* ]]; then
            local dep_id=$(echo "$dep" | grep -o '"[A-Z]\+-[0-9]\+[^"]*"' | tr -d '"')
            local dep_file=$(find_task_file "$dep_id")
            local dep_status=$(grep "status:" "$dep_file" | cut -d'"' -f2)
            if [ "$dep_status" != "COMPLETED" ]; then
                echo -e "${RED}Dependency $dep_id is not completed (status: $dep_status)${NC}"
                return 1
            fi
        fi
    done <<< "$deps"

    echo -e "${GREEN}All dependencies are satisfied. Task $task_id is ready to start${NC}"
}

update_progress() {
    local task_id=$1
    local progress=$2
    local file=$(find_task_file "$task_id")
    
    if [ -z "$file" ]; then
        echo -e "${RED}Task $task_id not found${NC}"
        return 1
    fi

    if ! [[ $progress =~ ^[0-9]+$ ]] || [ "$progress" -lt 0 ] || [ "$progress" -gt 100 ]; then
        echo -e "${RED}Invalid progress percentage. Must be between 0 and 100${NC}"
        return 1
    fi

    sed -i "s/progress_percentage: .*/progress_percentage: $progress/" "$file"
    sed -i "s/last_updated: .*/last_updated: \"$TIMESTAMP\"/" "$file"
    echo -e "${GREEN}Updated progress of $task_id to $progress%${NC}"
}

assign_task() {
    local task_id=$1
    local username=$2
    local file=$(find_task_file "$task_id")
    
    if [ -z "$file" ]; then
        echo -e "${RED}Task $task_id not found${NC}"
        return 1
    fi

    sed -i "s/assigned_to: .*/assigned_to: \"$username\"/" "$file"
    sed -i "s/last_updated: .*/last_updated: \"$TIMESTAMP\"/" "$file"
    echo -e "${GREEN}Assigned $task_id to $username${NC}"
}

list_phase_tasks() {
    local phase=$1
    echo -e "${BLUE}Tasks in phase $phase:${NC}"
    echo "----------------------------------------"
    find "$TASK_ROOT" -type f -name "*.yml" -exec grep -l "phase: \"$phase\"" {} \; | while read -r file; do
        echo -n "$(basename "$file"): "
        task_id=$(grep "task_id:" "$file" | cut -d'"' -f2)
        echo "$task_id"
        deps=$(grep -A 3 "dependencies:" "$file" | grep "task_id:")
        if [ ! -z "$deps" ]; then
            echo "  Dependencies:"
            echo "$deps" | while read -r dep; do
                echo "    $dep"
            done
        fi
        blocks=$(grep -A 3 "blocks:" "$file" | grep "task_id:")
        if [ ! -z "$blocks" ]; then
            echo "  Blocks:"
            echo "$blocks" | while read -r block; do
                echo "    $block"
            done
        fi
        echo
    done
}

list_status_tasks() {
    local status=$1
    echo -e "${BLUE}Tasks with status $status:${NC}"
    echo "----------------------------------------"
    find "$TASK_ROOT" -type f -name "*.yml" -exec grep -l "status: \"$status\"" {} \; | while read -r file; do
        echo -n "$(basename "$file"): "
        task_id=$(grep "task_id:" "$file" | cut -d'"' -f2)
        echo "$task_id"
        deps=$(grep -A 3 "dependencies:" "$file" | grep "task_id:")
        if [ ! -z "$deps" ]; then
            echo "  Dependencies:"
            echo "$deps" | while read -r dep; do
                echo "    $dep"
            done
        fi
        blocks=$(grep -A 3 "blocks:" "$file" | grep "task_id:")
        if [ ! -z "$blocks" ]; then
            echo "  Blocks:"
            echo "$blocks" | while read -r block; do
                echo "    $block"
            done
        fi
        echo
    done
}

show_dependency_chain() {
    local task_id=$1
    local indent=${2:-0}
    local visited=${3:-""}
    local file=$(find_task_file "$task_id")
    
    if [ -z "$file" ]; then
        echo -e "${RED}Task $task_id not found${NC}"
        return 1
    fi

    if [[ $visited == *"$task_id"* ]]; then
        echo "$(printf '%*s' $indent '')${YELLOW}$task_id (circular dependency)${NC}"
        return 0
    fi

    visited="$visited $task_id"
    local status=$(grep "status:" "$file" | cut -d'"' -f2)
    echo "$(printf '%*s' $indent '')${BLUE}$task_id${NC} (Status: $status)"

    local deps=$(grep -A 5 "dependencies:" "$file" | grep "task_id:" | cut -d'"' -f2)
    if [ ! -z "$deps" ]; then
        echo "$(printf '%*s' $((indent+2)) '')Dependencies:"
        echo "$deps" | while read -r dep; do
            show_dependency_chain "$dep" $((indent+4)) "$visited"
        done
    fi
}

# Main command processing
case $1 in
    status)
        show_status "$2"
        ;;
    update-status)
        update_status "$2" "$3"
        ;;
    dependencies)
        show_dependencies "$2"
        ;;
    blocked-by)
        show_blocked_by "$2"
        ;;
    blocks)
        show_blocks "$2"
        ;;
    validate)
        show_validation "$2"
        ;;
    ready)
        check_ready "$2"
        ;;
    progress)
        update_progress "$2" "$3"
        ;;
    assign)
        assign_task "$2" "$3"
        ;;
    list-phase)
        list_phase_tasks "$2"
        ;;
    list-status)
        list_status_tasks "$2"
        ;;
    dependency-chain)
        show_dependency_chain "$2"
        ;;
    progress-summary)
        show_progress_summary
        ;;
    *)
        usage
        exit 1
        ;;
esac
