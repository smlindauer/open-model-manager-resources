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
import json, os, pprint

viya_host = "localhost"
port = ":8080"
host_url="http://" + viya_host + port
publishmodel_url = host_url + "/modelPublish/models"

mm_auth = mmAuthorization.mmAuthorization("myAuth")

user_id = "SAS_USER_ID"
user_passwd = "SAS_USER_PASSWD"

dest_name = "MY_DEST_NAME"

auth_token = mm_auth.get_auth_token(host_url, user_id, user_passwd)

model_get_headers = {
    mmAuthorization.AUTHORIZATION_HEADER: mmAuthorization.AUTHORIZATION_TOKEN + auth_token
}

# synchronous
model_publishing_headers = {
    'Content-Type': 'application/vnd.sas.models.publishing.request+json',
    mmAuthorization.AUTHORIZATION_HEADER: mmAuthorization.AUTHORIZATION_TOKEN + auth_token
}
# asynchronous
model_publishing_async_headers = {
    'Content-Type': 'application/vnd.sas.models.publishing.request.asynchronous+json',
    mmAuthorization.AUTHORIZATION_HEADER: mmAuthorization.AUTHORIZATION_TOKEN + auth_token
}

# # Create and publish the BaseImages to specified destination
# #
# # Synchronous create python2 base-image
# # The API call will wait until baseImage is fully created and pushed
# # The 'imageUrl' property will be showed in the returned body
# #

# create python2 base-image (with synchronous request)
# three required fields: 
# - modelName: 'python'
# - modelId: must be 'base'
# - modelVersionid: '2'

python_model = {
    "name":"publish python2 baseimage",
    "modelContents":[
        {
            "modelName": "python",
            "modelId": "base",
            "modelVersionId": "2"
        }
    ],
    "destinationName": dest_name
}

published_model = requests.post(publishmodel_url, 
                             data=json.dumps(python_model), headers=model_publishing_headers)

print(published_model)
json_obj = published_model.json()

pprint.pprint(json_obj)

# inspect property value of 'imageUrl'
if "properties" in json_obj:
    props = json_obj["properties"]
    if "imageUrl" in props:
        print("imageUrl:", props["imageUrl"])

