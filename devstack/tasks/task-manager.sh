#!/bin/bash

TASK_FILE="$(dirname $0)/tasks.json"

list_tasks() {
    echo "GLFS Build Tasks Status:"
    echo "======================="
    jq -r '.tasks[] | "\(.id): \(.title) [\(.status | ascii_upcase)]"' "$TASK_FILE" | while read line; do
        if [[ $line == *"[COMPLETED]"* ]]; then
            echo "✅ $line"
        else
            echo "⏳ $line"
        fi
    done
}

mark_done() {
    local id="$1"
    local date=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    jq --arg id "$id" --arg date "$date" \
       '.tasks = [.tasks[] | if .id == $id then .status = "completed" | .completion_date = $date else . end]' \
       "$TASK_FILE" > "$TASK_FILE.tmp" && mv "$TASK_FILE.tmp" "$TASK_FILE"
    echo "✅ Marked task $id as completed"
}

add_task() {
    local id="$1"
    local title="$2"
    jq --arg id "$id" --arg title "$title" \
       '.tasks += [{"id": $id, "title": $title, "status": "pending", "completion_date": null}]' \
       "$TASK_FILE" > "$TASK_FILE.tmp" && mv "$TASK_FILE.tmp" "$TASK_FILE"
    echo "⏳ Added new task: $id - $title"
}

case "$1" in
    "list") list_tasks ;;
    "done") mark_done "$2" ;;
    "add") add_task "$2" "$3" ;;
    *) echo "Usage: $0 {list|done <task-id>|add <task-id> <title>}" ;;
esac
