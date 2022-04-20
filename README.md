# Docker setup

## Introduction

This system is a bundle created to provide very usefull for remote working,
the provided services are:

### Jitsi meeting

A great tool for video meetings with a lot of configurations and uses.

You can find more information in
[Jitsi web page](https://jitsi.org/jitsi-meet/) and also on
[jitsi github](https://github.com/jitsi).

### Wireguard

A VPN service that allows you to create new users really fast and share
their credentials and provides clients for most platforms.

You can find more information over on
[Wireguard web page](https://www.wireguard.com/) and also on
[Wireguard github](https://github.com/WireGuard)
(Here you can also find the code for the clients).

### Traefik

Reverse proxy and loader balancer.

You can find more information in
[Traefik web page](https://traefik.io/) and also on 
[Traefik github](https://github.com/traefik/traefik).

## Quick start

This instalation guide asumes you have a correct instalation of docker and
docker-compose, if not check 
[how to install docker and docker-compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-getting-started).

There are 3 main scripts:
- start.sh: Creates all the required files and folders.
- up.sh: Creates the networks and containers.
- down.sh: Removes the networks and containers from the host.

The main configuration parameters will be request by the start.sh script,
but jitsi parameters have to be configured by the user on the jitsi/.env file


Fist of all run start.sh:
```s
./start.sh
```
Then change the configuration files that you want to.
Finally run up.sh:
```s
./up.sh
```

If you want to take down the system or if something whent wrong during the
start just use down.sh:
```s
./down.sh
```

Note that the script has the same permmissions as the user who runs it, so if
you need to make use of sudo to run docker commands, you will need to make use
of sudo run the script

SSL certificates are requested to [Lets Encrypt](https://letsencrypt.org/), if
you request more than a certain quantity in an hour you will be banned. Thats
why traefik is configured to request the certificates to a demo Lets Encrypt
server that doesnt block user but doesnt produce the final certificates.
Once all is in place just go to traefik/docker-compose.yml and remove the line:
``` yml
- "--certificatesresolvers.myhttpchallenge.acme.caserver=https://acme-staging-v02.api.letsencrypt.org/directory"
```
## System requirements

- Unix system
- Docker and docker-compose installed
- 4 domains to:
    - Vpn web ui
    - Traefik dashboard
    - Jitsi meet
    - Calendar
- Server with open ports on firewall (at least 80,443,1000 and 51820)
- Administrator email

## System diagram

![](docs/systemDiagram.png)

## FAQ

1. The first time I use the start.sh script it throws a bunch of warnings:
This is fine, it is trying to take down services with a configuration that
is not done at the moment

2. The scripts doesnt create the services, just throws a buch of warnings:
If you run the scripts in the following order:
```s
./start.sh
./up.sh
```
And the warnings persist you should probably check your docker-compose version
and update to v. 1.28+. To check your docker version use:
```s
docker-compose --version
```
To update your docker compose make sure you uninstall it and the use:
```s
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
# If that doesnt work check that the path is right
#To fix the issue you can create symbolic links in the right path
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```
3. I have commented the alternative certificates in traefik docker-compose and
I am not getting recognised certificates: This could be cause because your
traefik/letsencrypt/acme.json fila has a valid certificate already (the
unrecognised one). In order to ask for a new certificate you shoul remove
this file and restart the system using:
```s
./down.sh
rm traefik/letsencrypt/acme.json
./up.sh
```
