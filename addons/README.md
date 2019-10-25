# Overview

This directory contains the instructions to perform various jobs in Open Model Manager container:
* install extra Python packages into the Open MM container;
* change PyMAS configuration in the container;
* turn on logging debug for specific service using sas-admin util;
* create container base images for Python2, Python3 and R models with Python script;
* create AWS and/or private docker publish destinations with Python script;

## Extra Python packages
When container instance is up, Python 3 has been installed under sas user. User could also install extra Python packages if needed.

Login into container instance as sas user
```
docker exec -it openmm bash
```
Use pip3 to install Python packages, such as
```
pip3 install --user numpy
pip3 install --user h2o
```

## PyMAS Configuration
In order to use a PyMAS Package. We need configure Compute Server and/or CAS Server. 
Please refer to SAS Micro Analytic Service 5.3: Programming and Administration Guide for more information.

Login into container instance as sas user
```
docker exec -it openmm bash
```

Create (if not exists) and edit the following files:
* /opt/sas/viya/config/etc/sysconfig/microanalyticservice.conf
* /opt/sas/viya/config/etc/sysconfig/compsrv/default/sas-compsrv
* /opt/sas/viya/config/etc/cas/default/cas_usermods.settings

Add the following lines in the files:
```
MAS_M2PATH=/opt/sas/viya/home/SASFoundation/misc/embscoreeng/mas2py.py
export MAS_M2PATH
 
MAS_PYPATH=/usr/bin/python3
export MAS_PYPATH
```

## Turn on logging debug with sas-admin util
Occasionally user would like to get more debug information from log file when troubleshoot certain situation. 
The SAS Administration (sas-admin) Command Line Interface (CLI) could easily set logging level for specific SAS services in CLI.
User can download it at [download site at SAS Support](https://support.sas.com/downloads/package.htm?pid=2133).
The following steps illustrate how to turn on DEBUG level on SAS Model Publish service.
* Download and extract sas-admin;
* Create a json file (such as modelpublish_debug.json) in the same directory as:
```
{
    "name": "modelpublish logging level",
    "items": [{
        "metadata": {
            "mediaType": "application/vnd.sas.configuration.config.logging.level+json;version=1",
             "services": ["modelPublish", "modelRepository"]
        },
        "name": "com.sas.modelmanager",
        "level": "DEBUG"
    }]
}
``` 
* Get auth token with your user name, password
```
./sas-admin prof set-endpoint http://localhost:8080
./sas-admin auth login -u <username> -p <password>
```
* Create configuration settings for logging
```
./sas-admin plugins enable-default-repo
./sas-admin plugins install --repo SAS configuration
./sas-admin configuration configurations create --file modelpublish_debug.json
```

## Model containerization
Since SAS Viya 15.3, we start supporting model containerization for Python and R models. 
Two more things to be done before user is able to publish Python or R model to model container image.


### Create publish destinations
Three Python scripts could help user to create new destinations for types of cas, aws and privateDocker.

<b>Make sure that you modify the SAS account, AWS access key information or private docker information in the script before execution. </b>
```
python create_cas_destination.py
python create_aws_destination.py
python create_privatedocker_destination.py
```


### Create base images
Here are the types of model base images that are currently supported:
* Python 2 base image is used for scoring Python 2 models
* Python 3 base image is used for scoring Python 3 models
* R base image is used for scoring R models

<b>Before running the scripts, make sure that you modify the script and fill in proper user name, password and specify the destination name.</b> 
#### Create Python 3 base image
In the script we use synchronous publish mode to generate Python base images. Please wait until it returns result.
```
python create_python3_destination.py
```
#### Create Python 2 base image
```
python create_python2_destination.py
```
#### Create Python R base image
It may take longer to create R base image, so in the script we use asynchronous publish.
```
python create_r_destination.py
```

