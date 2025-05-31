#!/bin/bash

# Initialize DevStack development environment

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
mkdir -p www
mkdir -p services/nginx/ssl
mkdir -p services/nginx/conf.d
mkdir -p services/php/conf.d
mkdir -p services/mysql/conf.d

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file from example"
fi

# Generate SSL certificates
./scripts/ssl-setup.sh

# Set execute permissions on scripts
chmod +x scripts/*.sh

# Create basic index.php file if www is empty
if [ ! "$(ls -A www)" ]; then
    echo '<?php phpinfo();' > www/index.php
    echo "Created example index.php file"
fi

# Build and start containers
docker compose build
docker compose up -d

echo "DevStack initialization complete!"
echo "Access your development environment at https://localhost"

