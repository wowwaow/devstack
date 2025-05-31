# AI Agent Stack Installation Guide

## System Requirements

### Minimum Requirements
- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended)
- 2 CPU cores minimum (4 cores recommended)
- 10GB available disk space
- Linux-based operating system (Ubuntu 20.04+ recommended)

### Python Dependencies
```
pip install -r requirements.txt
```

## Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/wowwaow/devstack.git
cd devstack/agent_stack
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
.\venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
1. Copy the example configuration:
```bash
cp config/example.env .env
```

2. Edit the `.env` file with your settings:
```env
AGENT_STACK_HOME=./
LOG_LEVEL=INFO
MAX_AGENTS=5
HEARTBEAT_INTERVAL=120
SOFT_TIMEOUT=300
HARD_TIMEOUT=600
CRITICAL_TIMEOUT=900
```

### 5. Initialize System Structure
```bash
python scripts/initialize_system.py
```

This will:
- Create required directories
- Initialize log files
- Set up agent registry
- Generate initial templates

### 6. Verify Installation
```bash
python scripts/system_check.py
```

The system check will verify:
- Directory structure
- File permissions
- Python dependencies
- Environment configuration
- System connectivity

## Post-Installation Setup

### 1. Configure Agent Profiles
1. Navigate to `core/agent_status/`
2. Copy the example profile:
```bash
cp AGENT_PROFILE_TEMPLATE.json my_agent_profile.json
```
3. Edit the profile with your agent's specifications

### 2. Setup Logging
1. Review logging configuration in `config/logging.yaml`
2. Adjust log rotation and retention policies as needed
3. Configure log paths if using custom locations

### 3. Initialize Task Pool
1. Navigate to `core/task_pool/`
2. Set up initial task templates
3. Configure task priority rules

### 4. Configure Monitoring
1. Review monitoring settings in `config/monitoring.yaml`
2. Set up alert thresholds
3. Configure notification endpoints

## Troubleshooting

### Common Issues

#### Permission Errors
```bash
# Fix directory permissions
chmod -R u+rw agent_stack/
```

#### Python Version Conflicts
- Ensure you're using Python 3.8+
- Check for conflicting packages
- Verify virtual environment activation

#### Log Directory Issues
```bash
# Create missing log directories
mkdir -p logs/system_logs logs/work_logs
```

### Health Check
Run the health check script to diagnose issues:
```bash
python scripts/health_check.py
```

## Security Considerations

### File Permissions
- Ensure proper file ownership
- Set restrictive permissions on configuration files
- Protect sensitive credentials

### Network Security
- Configure firewalls appropriately
- Use secure communication channels
- Implement proper authentication

## Maintenance

### Regular Tasks
1. Monitor log files
2. Check system health
3. Update dependencies
4. Backup configuration
5. Clean old logs

### Backup Procedures
1. Back up configuration files
2. Export agent registry
3. Archive important logs
4. Document system state

## Next Steps
- Review [Usage Guide](USAGE.md)
- Configure [Agent Protocols](PROTOCOLS.md)
- Set up [Monitoring](MONITORING.md)
- Plan [Backup Strategy](BACKUP.md)

## Support
For issues and support:
1. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Review [Known Issues](KNOWN_ISSUES.md)
3. Submit an issue on GitHub
4. Contact system administrators
