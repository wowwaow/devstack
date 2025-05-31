# Warp Agent Stack

A flexible, environment-based AI agent coordination system designed for portability and multi-instance deployment.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/wowwaow/devstack.git
cd devstack/agent_stack

# Install Python dependencies
pip install -r requirements.txt

# Optional: Configure custom paths
export WARP_HOST_DIR=/custom/path     # Default: /mnt/host
export WARP_SYSTEM_DIR=/custom/system  # Default: $WARP_HOST_DIR/WARP_CURRENT

# Initialize the environment
./core/initialize.sh
```

## Environment Configuration

The system uses environment variables for configuration, enabling flexible deployment and easy migration between systems.

### Base Configuration
```bash
# Default paths
WARP_HOST_DIR="/mnt/host"
WARP_SYSTEM_DIR="$WARP_HOST_DIR/WARP_CURRENT"

# Source configuration
source core/config/environment.sh
```

### Custom Deployment
```bash
# Example: Custom paths
export WARP_HOST_DIR=/path/to/host
export WARP_SYSTEM_DIR=/path/to/system
source core/config/environment.sh

# Example: Multiple instances
export WARP_SYSTEM_DIR=/path/instance1
source core/config/environment.sh
```

## Directory Structure

```
agent_stack/
├── core/
│   ├── agents/      # Agent management system
│   ├── config/      # Environment configuration
│   │   ├── environment.sh  # Environment variable definitions
│   │   └── validate.sh     # Configuration validation
│   ├── events/      # Event handling system
│   ├── logging/     # Logging infrastructure
│   ├── monitoring/  # System monitoring
│   ├── tasks/       # Task management
│   ├── tests/       # Test suite
│   ├── initialize.sh # System initialization
│   └── setup.sh     # Directory setup
└── docs/
    ├── COMMANDS.md              # Available commands
    ├── INSTALLATION.md          # Installation guide
    ├── PROTOCOLS.md             # System protocols
    ├── SYSTEM_ARCHITECTURE.md   # System design
    └── USAGE.md                 # Usage instructions
```

## Testing

### Running Tests
```bash
# Run all environment tests
./core/tests/run_tests.sh

# Run specific test
python -m pytest core/tests/test_environment.py
```

### Test Coverage
```bash
# Generate test coverage report
python -m pytest --cov=core tests/
```

## System Validation

### Configuration Validation
```bash
# Validate environment setup
./core/config/validate.sh
```

### Directory Structure Validation
The system automatically validates the directory structure during initialization and provides detailed status:
- Directory existence and permissions
- File access and permissions
- Environment variable configuration

## Dependencies

### Python Dependencies
Install required Python packages:
```bash
pip install -r requirements.txt
```

### System Dependencies
- Python 3.8+
- Bash shell
- Git

## Documentation

- [Installation Guide](docs/INSTALLATION.md) - Detailed setup instructions
- [System Architecture](docs/SYSTEM_ARCHITECTURE.md) - System design and components
- [Usage Guide](docs/USAGE.md) - How to use the system
- [Command Reference](docs/COMMANDS.md) - Available commands
- [System Protocols](docs/PROTOCOLS.md) - System protocols and standards

## Development

### Setting Up Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt

# Initialize development instance
export WARP_SYSTEM_DIR=/path/to/dev/instance
./core/initialize.sh
```

### Running Tests During Development
```bash
# Run tests with detailed output
python -m pytest -v core/tests/

# Run tests with coverage
python -m pytest --cov=core --cov-report=html core/tests/
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Install development dependencies
4. Run tests to ensure everything works
5. Commit your changes
6. Push to your branch
7. Create a Pull Request

## License

[License details to be added]

## Support

For issues and questions, please:
1. Check the documentation
2. Run the validation script
3. Check the test results
4. Create an issue if the problem persists


## Instance Management

The system supports running multiple instances with different configurations. Use the instance management utility to create and manage instances:

### Creating New Instance
```bash
# Create a new instance
./core/config/manage_instances.sh create dev_instance

# Create instance in custom location
./core/config/manage_instances.sh create prod_instance /custom/base/path
```

### Listing Instances
```bash
# List all instances
./core/config/manage_instances.sh list

# List instances in custom location
./core/config/manage_instances.sh list /custom/base/path
```

### Switching Between Instances
```bash
# Switch to different instance
./core/config/manage_instances.sh switch dev_instance

# Switch to instance in custom location
./core/config/manage_instances.sh switch prod_instance /custom/base/path
```

### Deleting Instances
```bash
# Delete an instance (will prompt for confirmation)
./core/config/manage_instances.sh delete old_instance
```

### Instance Directory Structure
Each instance maintains its own isolated environment with:
- Separate configuration
- Independent logs
- Isolated agent status
- Dedicated task pools
- Instance-specific objectives

This allows you to run multiple configurations (e.g., development, testing, production) without interference.

### Best Practices
1. Use descriptive instance names
2. Keep development and production instances separate
3. Regular backup of production instances
4. Validate configuration after switching instances
5. Use consistent base directories for related instances

