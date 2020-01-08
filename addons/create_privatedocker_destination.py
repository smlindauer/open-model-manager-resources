#
# Copyright (c) 2019, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import mmAuthorization
import requests
import json

viya_host = "localhost"
port = ":8080"
host_url="http://" + viya_host + port
destination_url = host_url + "/modelPublish/destinations/"

mm_auth = mmAuthorization.mmAuthorization("myAuth")

# admin user id and password
admin_userId = "SAS_USER_ADMIN_ID"
user_passwd = "SAS_USER_PASSWD"

# destination name
dest_name = "MY_PRIVATE_DOCKER_DEST_NAME"

# docker repository base url
BASE_REPO_URL = "xx.xx.xx.xx"   # or "xx.xx.xx.xx/xxx"

# docker daemon socket url
DOCKER_HOST_URL = "" # using unix socket on default

# uncomment the line below if the docker daemon is running on tcp socket
# DOCKER_HOST_URL = "tcp://yy.yy.yy.yy:2375"

if admin_userId == "SAS_USER_ADMIN_ID":
    print("Please replace the values in the script with real ones before executing the script!")
    exit(1)

admin_auth_token = mm_auth.get_auth_token(host_url, admin_userId, user_passwd)

destination_privatedocker_headers = {
    "If-Match":"false",
    "Content-Type":"application/vnd.sas.models.publishing.destination.privatedocker+json",
    mmAuthorization.AUTHORIZATION_HEADER: mmAuthorization.AUTHORIZATION_TOKEN + admin_auth_token
}

# create new destination, expecting 201
print("Creating " + dest_name + " destination...")

props = [{"name": "baseRepoUrl", "value": BASE_REPO_URL}]
if DOCKER_HOST_URL != "":
    props.append({"name": "dockerHost", "value": DOCKER_HOST_URL})

destination_attrs = {
    "name":dest_name,
    "destinationType":"privateDocker",
     "properties": props
}

destination = requests.post(destination_url, 
                       data=json.dumps(destination_attrs), headers=destination_privatedocker_headers)

print(destination)

