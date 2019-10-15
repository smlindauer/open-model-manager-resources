# Overview

This directory contains the scripts to launch, debug the Open Model Manager container. 

# Files

* sitedefault_sample.yml - Sample file for sitedefault.yml which is used to load defaults into Consul.
* sssd_sample.conf - Sample  for sssd.conf which is used for authenticating users in the container.
* run_docker_container - Script that will launch the container with the correct settings for the `docker run` command

# Running

Create sssd.conf and sitedefault.yml files according to sample files;

Copy the license file from software order zip file;

Prepare the certificates if running in TLS mode. Upload signed CA certificate and named as casigned.crt, 
upload public key and named as servertls.key. 

Run the run_docker_container, pass in the container name, the image URL, SAS order ID and the port to map to the http port

```
cd deployment
./run_deployment --container-name openmm --image <registry url>/<namespace>/<image>:<tag> --order <SAS order> --http-port <port> [--debug, --tls]

```

That will start the image in detached mode. Once that is done you can do

```
# Look at logs
docker logs openmm

# Exec into the container
docker exec -it openmm bash

# Delete the container instance
docker container rm openmm
```

Also, a set of volumes will be created for you

```
$ docker volume ls
DRIVER              VOLUME NAME
local               casdata-openmm
local               caspermstore-openmm
local               consul-openmm
local               postgres-openmm
local               sasmmastore-openmm
local               sasmmsresources-openmm
```

