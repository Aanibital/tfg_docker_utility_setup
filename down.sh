#!/bin/bash

# this Script take down the servers, it does not stop the servers.

echo Trying to remove previous containers...
docker-compose -f traefik/docker-compose.yml down
docker-compose -f jitsi/docker-compose.yml down
docker-compose -f wg/docker-compose.yml down  
echo Done.
echo Removing networks...
docker network rm traefiknet
echo Done.