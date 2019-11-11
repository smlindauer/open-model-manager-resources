# Overview

This directory contains the scripts to launch and debug the SAS Open Model Manager container. 

# Files

* sitedefault_sample.yml - Sample file for sitedefault.yml which loads defaults into Consul.
* sssd_sample.conf - Sample for sssd.conf which is used for authenticating users in the container.
* run_docker_container - Script that will launch the container with the correct settings for the `docker run` command

# Deploying the Container


1.  Retrieve the files for this project in the manner you prefer. Place all the files in the same directory location.

2.  Create sssd.conf and sitedefault.yml files according to the comments in the sample files. Save the files in the same location as the run_docker_container script.

3.  If you have a sssd.cert associated with the sssd.conf file, place it in the same location as the run_docker_container script.

4.  Copy the files in the licenses directory from the uncompressed Software Order Email (SOE) zip file to the same location as the run_docker_container script.

5.  If you plan to run in TLS mode, copy the signed CA certificate and name it casigned.crt. Then copy the public key and name it servertls.key. Save both files in the same location as the run_docker_container script.

6.  Change the permissions of the run_docker_container file:
```
chmod +x run_docker_container
```

7.  Run the run_docker_container script using the appropriate values for the variables.

```
cd <the directory where you saved the run_docker_container file>
./run_docker_container --container-name openmodelmanager --image <registry URL>/<namespace>/<image>:<tag> --order <SAS order> --http-port <port> --https-port <port> [--debug, --tls]

```

The command starts the container in detached mode. After the container is started, you can perform the following tasks.



*  Look at logs:

```
docker logs openmodelmanager
```

*  Log into the container:

```
docker exec -it openmodelmanager bash

```
*  Stop and delete the container instance:

```
docker stop openmodelmanager
docker rm openmodelmanager
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
After the container is running, return to [SAS Open Model Manager 1.2 for Containers: Deployment Guide](http://documentation.sas.com/?docsetId=dplymdlmgmt0phy0dkr&docsetTarget=titlepage.htm&docsetVersion=1.2&locale=en) for information required to complete your initial deployment.
