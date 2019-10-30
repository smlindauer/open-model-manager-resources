# Overview

This directory contains the scripts to launch and debug the SAS Open Model Manager container. 

# Files

* sitedefault_sample.yml - Sample file for sitedefault.yml which loads defaults into Consul.
* sssd_sample.conf - Sample for sssd.conf which is used for authenticating users in the container.
* run_docker_container - Script that will launch the container with the correct settings for the `docker run` command

# Deploying the Container


1.  Create sssd.conf and sitedefault.yml files according to the comments in the sample files.

2.  Copy the license file from the zip file attached to your Software Order Email.

3.  If you plan to run in TLS mode, prepare the certificates. Upload the signed CA certificate and name it casigned.crt. Then upload the public key and name itservertls.key. 

4.  Run the run_docker_container script. Use the image URL, the SAS order ID, and the port mapped to the http port in place of the variables in the command below.

```
cd deployment
./run_deployment --container-name openmodelmanager --image <registry url>/<namespace>/<image>:<tag> --order <SAS order> --http-port <port> [--debug, --tls]

```

The command starts the image in detached mode. When the image is started, you can perform the following tasks:

```
# Look at logs
docker logs openmodelmanager

# Exec into the container
docker exec -it openmodelmanager bash

# Delete the container instance
docker container rm openmodelmanager
```

Also, a set of volumes will be created for you:

```
$ docker volume ls
DRIVER              VOLUME NAME
local               casdata-openmodelmanager
local               caspermstore-openmodelmanager
local               consul-openmodelmanager
local               postgres-openmodelmanager
local               sasmmastore-openmodelmanager
local               sasmmsresources-openmodelmanager
```
After the container is running, return to [SAS Open Model Manager 1.2 for Containers: Deployment Guide](http://documentation.sas.com/?docsetId=dplymdlmgmt0phy0dkr&docsetTarget=titlepage.htm&docsetVersion=1.2&locale=en) for post-installation tasks.
