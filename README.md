# Docker setup

## Introduction

This system is a bundle created to provide very usefull services in order
to work from a remote place to job, the provided services are:

### Jitsi meeting

A great tool for video meetings with a lot of configurations and uses.

You can find more information in
[Jitsi web page](https://jitsi.org/jitsi-meet/) and also on
[jitsi github](https://github.com/jitsi).

### Wireguard

A VPN service that allows you to create new users really fast and share
their credentials and provides clients for most platforms.

You can find more information over on
[wireguard web page](https://www.wireguard.com/) and also on
[wireguard github](https://github.com/WireGuard)
(Here you can also find the code for the clients).

### Traefik

Reverse proxy and loader balancer.

You can find more information in
[traefik web page](https://traefik.io/) and also on 
[traefik github](https://github.com/traefik/traefik).

## Quick start

This instalation guide asumes you have a correct instalation of docker and
docker-compose, if not check 
[how to install docker and docker-compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-getting-started).

There are 2 main scripts:
- start.sh: Creates all the required files, networks and containers.
- stop.sh: Removes the networks and containers from the host.

The main configuration parameters will be request by the start.sh script,
but jitsi parameters have to be configured by the user on the jitsi/.env file


Fist of all run start.sh:
```
./start.sh
```
Then change the configuration files and configuration files that you want to
(at least jitsi/.env). Finally run up.sh:
```
./up.sh
```

If you want to take down the system or if something whent wrong during the
start just use down.sh:
```
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


