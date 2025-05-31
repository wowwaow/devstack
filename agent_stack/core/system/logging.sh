#!/bin/bash

log_message() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" | tee -a "$SYSTEM_LOGS_DIR/system.log"
}

log_info() { log_message "INFO" "$1"; }
log_warn() { log_message "WARN" "$1"; }
log_error() { log_message "ERROR" "$1"; }
log_success() { log_message "SUCCESS" "$1"; }

log_permission_action() {
    local type="$1"
    local path="$2"
    local action="$3"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    ensure_file_exists "$PERMISSION_AUDIT_LOG"
    echo "| $timestamp | $type | $path | $action |" >> "$PERMISSION_AUDIT_LOG"
}

