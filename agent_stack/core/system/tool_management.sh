#!/bin/bash

install_tool() {
    local tool_name="$1"
    local method="${2:-auto}"
    local justification="${3:-required_for_operation}"
    
    ensure_directory_permissions "$INSTALLED_TOOLS_DIR"
    ensure_file_exists "$TOOL_INSTALLATION_LOG" "# Tool Installation Log

| Timestamp | Tool | Method | Status | Justification |
|-----------|------|--------|--------|---------------|"
    
    log_info "Installing tool: $tool_name via $method"
    
    local install_success=false
    local error_message=""
    
    case $method in
        apt)
            if sudo apt update && sudo apt install -y "$tool_name"; then
                install_success=true
            else
                error_message="APT installation failed"
            fi
            ;;
        pip)
            if pip install "$tool_name" --user; then
                install_success=true
            else
                error_message="PIP installation failed"
            fi
            ;;
        npm)
            if npm install -g "$tool_name"; then
                install_success=true
            else
                error_message="NPM installation failed"
            fi
            ;;
        auto)
            # Try different methods automatically
            if command -v apt &> /dev/null && sudo apt update && sudo apt install -y "$tool_name"; then
                install_success=true
                method="apt"
            elif command -v pip &> /dev/null && pip install "$tool_name" --user; then
                install_success=true
                method="pip"
            elif command -v npm &> /dev/null && npm install -g "$tool_name"; then
                install_success=true
                method="npm"
            else
                error_message="All installation methods failed"
            fi
            ;;
        *)
            error_message="Unknown installation method: $method"
            ;;
    esac
    
    local status="FAILED"
    if $install_success; then
        status="SUCCESS"
        log_success "Tool $tool_name installed successfully via $method"
        
        # Update tools registry
        if command -v jq &> /dev/null; then
            jq --arg tool "$tool_name" --arg method "$method" --arg time "$(date -Iseconds)" \
               '.installed_tools[$tool] = {
                   "method": $method,
                   "installed_at": $time,
                   "status": "active"
               } | .last_updated = $time | .installation_count += 1' \
               "$TOOLS_REGISTRY" > "${TOOLS_REGISTRY}.tmp" && \
               mv "${TOOLS_REGISTRY}.tmp" "$TOOLS_REGISTRY"
        fi
    else
        log_error "Tool installation failed: $tool_name - $error_message"
    fi
    
    # Log installation attempt
    echo "| $(date) | $tool_name | $method | $status | $justification |" >> "$TOOL_INSTALLATION_LOG"
    
    return $($install_success && echo 0 || echo 1)
}

