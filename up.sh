#!/bin/bash

# Creation of traefik virtual network
echo Trying to create a new virtual network...
docker network rm traefiknet
docker network create traefiknet
echo Done.

# Running containers on background
echo Launching traefik...
docker-compose -f traefik/docker-compose.yml up -d
echo Done.
echo Launching jitsi meet...
docker-compose -f jitsi/docker-compose.yml up -d
echo Done.
echo Launching wireguard...
docker-compose -f wg/docker-compose.yml up -d
echo Done.