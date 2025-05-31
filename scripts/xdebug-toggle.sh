#!/bin/bash

# Toggle Xdebug extension in PHP container
CONTAINER_NAME="devstack-php"
XDEBUG_INI="/usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini"
XDEBUG_INI_DISABLED="/usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini.disabled"

if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    if docker exec $CONTAINER_NAME test -f $XDEBUG_INI; then
        # Disable Xdebug
        docker exec $CONTAINER_NAME mv $XDEBUG_INI $XDEBUG_INI_DISABLED
        echo "Xdebug disabled"
    else
        # Enable Xdebug
        docker exec $CONTAINER_NAME mv $XDEBUG_INI_DISABLED $XDEBUG_INI
        echo "Xdebug enabled"
    fi
    
    # Restart PHP container
    docker restart $CONTAINER_NAME
else
    echo "PHP container is not running"
    exit 1
fi

