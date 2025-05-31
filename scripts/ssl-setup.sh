#!/bin/bash

# Generate SSL certificates for local development
SSL_DIR="./services/nginx/ssl"
DAYS_VALID=365
COUNTRY="US"
STATE="CA"
LOCALITY="San Francisco"
ORGANIZATION="DevStack Development"
ORGANIZATIONAL_UNIT="Development Team"
COMMON_NAME="localhost"

# Create SSL directory if it doesn't exist
mkdir -p "$SSL_DIR"

# Generate SSL certificate and key
openssl req -x509 \
    -nodes \
    -days "$DAYS_VALID" \
    -newkey rsa:2048 \
    -keyout "$SSL_DIR/devstack.key" \
    -out "$SSL_DIR/devstack.crt" \
    -subj "/C=$COUNTRY/ST=$STATE/L=$LOCALITY/O=$ORGANIZATION/OU=$ORGANIZATIONAL_UNIT/CN=$COMMON_NAME"

# Set proper permissions
chmod 644 "$SSL_DIR/devstack.crt"
chmod 600 "$SSL_DIR/devstack.key"

echo "SSL certificate generated successfully at $SSL_DIR"

