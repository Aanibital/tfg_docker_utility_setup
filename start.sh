#!/bin/bash

# Destroying previous containers
echo Trying to remove previous containers...
docker-compose -f traefik/docker-compose.yml down
docker-compose -f jitsi/docker-compose.yml down
docker-compose -f wg/docker-compose.yml down  
echo Done.

# Creation of certificates folder for traefik
mkdir -p traefik/letsencrypt


# Creation of traefik enviromental variables
echo Traefik configuration:
echo -n "Please enter an email for the traefik certificates: "
read adminEmail
echo -n "Please enter host domain for Traefik: "
read domainTraefik

cat > traefik/.env << EOF1
ADMIN_EMAIL=$adminEmail
DOMAIN_TRAEFIK=$domainTraefik
EOF1

# Creation of wireguard database folder
mkdir -p wg/wg-access-server-data

# Creation of wireguard config file
echo Wireguard configuration:
echo -n "Please enter your host ip: "
read hostIp
echo -n "Please enter host domain for VPN admin page:"
read domainVpn
echo -n "Please enter an admin user for VPN admin page:"
read adminUser
echo -n "Please enter an admin password for VPN admin page:"
read adminPassword

cat > wg/config.yaml << EOF2
loglevel: info
wireguard:
  externalHost: "$hostIp"
  adminPassword: "$adminPassword"
EOF2

cat > wg/.env << EOF3
HOST_IP=$hostIp
DOMAIN_VPN=$domainVpn
ADMIN_USER=$adminUser
ADMIN_PASSWORD=$adminPassword
EOF3

# Creation of jitsi environmental variables
echo Generating jitsi configuration..
cp jitsi/env.example jitsi/.env
chmod +x jitsi/gen-passwords.sh
./jitsi/gen-passwords.sh

sed -i s/DOCKER_HOST_ADDRESS=/DOCKER_HOST_ADDRESS=$hostIp/g jitsi/.env

echo -n "Please enter host domain for Jitsi:"
read domainJitsi
sed -i s/PUBLIC_URL=/PUBLIC_URL=$domainJitsi/g jitsi/.env



# Creation of jitsi passwords and required folders

mkdir -p ~/.jitsi-meet-cfg/{web/crontabs,web/letsencrypt,transcripts,prosody/config,prosody/prosody-plugins-custom,jicofo,jvb,jigasi,jibri}
echo Done.

