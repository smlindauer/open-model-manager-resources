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
dest_name = "MY_CAS_DEST_NAME"

if admin_userId == "SAS_USER_ADMIN_ID":
    print("Please replace the values in the script with real ones before executing the script!")
    exit(1)

admin_auth_token = mm_auth.get_auth_token(host_url, admin_userId, user_passwd)

destination_cas_headers = {
    "If-Match":"false",
    "Content-Type":"application/vnd.sas.models.publishing.destination.cas+json",
    mmAuthorization.AUTHORIZATION_HEADER: mmAuthorization.AUTHORIZATION_TOKEN + admin_auth_token
}

# create new destination, expecting 201
print("Creating " + dest_name + " destination...")

destination_attrs = {
    "name":dest_name,
    "destinationType":"cas",
    "casServerName":"cas-shared-default",
    "casLibrary" : "public",
    "destinationTable" : "SAS_MODEL_TABLE"
}

destination = requests.post(destination_url, 
                       data=json.dumps(destination_attrs), headers=destination_cas_headers)

print(destination)


