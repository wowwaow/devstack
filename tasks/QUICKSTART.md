# Task System Quick Start Guide

## Getting Started

### 1. Initial Setup
```bash
cd /home/ubuntu/devstack/tasks
# Review the current task structure
ls -R
# Check the task summary
cat TASK_SUMMARY.md
```

### 2. Understanding Task Types
1. **LFS Builder Tasks** (`/lfs_builder/`)
   - Sequential build process
   - Phase-based execution
   - Clear dependency chain

2. **Core Implementation Tasks** (`/core_implementation/`)
   - Component-based structure
   - Parallel execution possible
   - Cross-component dependencies

## Common Operations

### 1. Starting a New Task
1. Check task dependencies:
```bash
# Example for TASK-2.1
grep -r "TASK-2.1" .
```

2. Verify prerequisite completion:
```bash
# Check status of dependencies
cat lfs_builder/phase1_environment/*.yml | grep "status:"
```

3. Update task status:
```bash
# Edit the task's YAML file
# Change status: "PENDING" to status: "IN_PROGRESS"
```

### 2. Task Execution Flow

#### LFS Builder Example
1. Start with Phase 1:
   ```bash
   # Begin with environment validation
   vim lfs_builder/phase1_environment/environment_validation.yml
   # Follow the dependency chain: 1.1 -> 1.2 -> 1.3 -> 1.4
   ```

2. Progress through phases:
   ```bash
   # Move to Phase 2 after Phase 1 completion
   # Check Phase 1 completion status
   grep -r "status:" lfs_builder/phase1_environment/
   ```

#### Core Implementation Example
1. Independent component start:
   ```bash
   # Start Resource Management tasks
   cd core_implementation/resource_management/
   # Begin with TASK-RM001 (no dependencies)
   ```

2. Parallel task execution:
   ```bash
   # Check for tasks without dependencies
   grep -r "dependencies: []" core_implementation/
   ```

### 3. Status Updates

#### Updating Task Status
```yaml
# Edit task YAML file
metadata:
  last_updated: "YYYY-MM-DDThh:mm:ssZ"
  assigned_to: "username"
  estimated_completion: "YYYY-MM-DDThh:mm:ssZ"
  progress_percentage: 50
```

#### Tracking Dependencies
```bash
# Check blocking tasks
grep -r "blocks:" .
# Check required tasks
grep -r "requires:" .
```

### 4. Validation

#### Pre-execution Validation
```bash
# Check validation requirements
grep -A 5 "validation_requirements:" task_file.yml
```

#### Implementation Verification
```bash
# Review implementation details
grep -A 10 "implementation_details:" task_file.yml
```

## Best Practices

### 1. Task Selection
- Start with tasks having no dependencies
- Prioritize critical tasks
- Consider parallel execution opportunities

### 2. Status Management
- Keep status updated regularly
- Document blockers immediately
- Update progress percentage accurately

### 3. Dependency Handling
- Verify all prerequisites before starting
- Update blocking tasks when completing work
- Document any new dependencies discovered

### 4. Documentation
- Maintain implementation notes
- Update validation results
- Record any deviations from plan

## Common Patterns

### 1. Sequential Build (LFS Builder)
```
TASK-1.1 -> TASK-1.2 -> TASK-1.3 -> TASK-1.4
    |
    v
TASK-2.1 -> TASK-2.2 -> TASK-2.3
    |
    v
TASK-3.1 -> TASK-3.2 -> TASK-3.3
```

### 2. Parallel Component Work (Core Implementation)
```
Resource Management    Error Handling       Testing
TASK-RM001 -----> TASK-EH002          TASK-TI001
TASK-RM002 -----> TASK-MT003 <----- TASK-TI003
TASK-RM003 -----> TASK-MT001
```

## Troubleshooting

### 1. Dependency Issues
```bash
# Find all dependencies for a task
grep -r "TASK-XX" .
# Check status of blocking tasks
grep -r "blocks.*TASK-XX" .
```

### 2. Status Conflicts
```bash
# Find all tasks in specific status
grep -r "status: \"IN_PROGRESS\"" .
# Check last updated timestamp
grep -r "last_updated" .
```

### 3. Implementation Problems
- Check validation requirements
- Review implementation details
- Verify component dependencies
- Check for related tasks

## Getting Help
- Review TASK_SUMMARY.md for overview
- Check individual task YAML files for details
- Examine dependency_map.yml for relationships
- Consult implementation_phases.yml for phase guidelines

