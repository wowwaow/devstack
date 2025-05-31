#!/bin/bash

verify_file_access() {
    local file_path="$1"
    if [[ ! -r "$file_path" ]] || [[ ! -w "$file_path" ]]; then
        log_error "Access verification failed for: $file_path"
        return 1
    fi
    return 0
}

verify_directory_access() {
    local dir_path="$1"
    if [[ ! -r "$dir_path" ]] || [[ ! -w "$dir_path" ]] || [[ ! -x "$dir_path" ]]; then
        log_error "Directory access verification failed for: $dir_path"
        return 1
    fi
    return 0
}

ensure_file_permissions() {
    local file_path="$1"
    local permissions="${2:-644}"
    
    if [[ -f "$file_path" ]]; then
        sudo chown "$WARP_USER:$WARP_GROUP" "$file_path"
        sudo chmod "$permissions" "$file_path"
        log_permission_action "FILE" "$file_path" "permissions_set_$permissions"
    else
        log_warn "File does not exist: $file_path"
        return 1
    fi
    
    verify_file_access "$file_path"
}

ensure_directory_permissions() {
    local dir_path="$1"
    local permissions="${2:-755}"
    
    if [[ -d "$dir_path" ]]; then
        sudo chown "$WARP_USER:$WARP_GROUP" "$dir_path"
        sudo chmod "$permissions" "$dir_path"
        log_permission_action "DIRECTORY" "$dir_path" "permissions_set_$permissions"
    else
        sudo mkdir -p "$dir_path"
        sudo chown "$WARP_USER:$WARP_GROUP" "$dir_path"
        sudo chmod "$permissions" "$dir_path"
        log_permission_action "DIRECTORY" "$dir_path" "created_with_permissions_$permissions"
    fi
    
    verify_directory_access "$dir_path"
}

ensure_file_exists() {
    local file_path="$1"
    local default_content="${2:-}"
    
    if [[ ! -f "$file_path" ]]; then
        ensure_directory_permissions "$(dirname "$file_path")"
        echo "$default_content" > "$file_path"
        ensure_file_permissions "$file_path"
        log_info "Created file: $file_path"
    fi
}

