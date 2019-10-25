import mmAuthorization
import requests
import json

public_ip = "localhost"
host_url="http://" + public_ip + ":8080"
destination_url = host_url + "/modelPublish/destinations/"

mm_auth = mmAuthorization.mmAuthorization("myAuth")

admin_userId = "SAS_USER_ADMIN_ID"
user_passwd = "SAS_USER_PASSWD"

admin_auth_token = mm_auth.get_auth_token(host_url, admin_userId, user_passwd)

destination_admin_headers = {
    mmAuthorization.AUTHORIZATION_HEADER: mmAuthorization.AUTHORIZATION_TOKEN + admin_auth_token
}

destination_aws_headers = {
    "If-Match":"false",
    "Content-Type":"application/vnd.sas.models.publishing.destination.aws+json",
    mmAuthorization.AUTHORIZATION_HEADER: mmAuthorization.AUTHORIZATION_TOKEN + admin_auth_token
}

# create new destination, expecting 201
dest_name = "AWS"
print("Creating " + dest_name + " destination...")

destination_attrs = {
    "name":dest_name,
    "destinationType":"aws",
     "properties": [{"name": "accessKeyId",                
                 "value": "MY_AWS_KEY_ID"},
                {"name": "secretAccessKey",                 
                 "value": "MY_AWS_ACCESS_KEY"},
                {"name": "region",                 
                 "value": "us-east-1"},
                {"name": "kubernetesCluster",                 
                 "value": "MY_EKS_NAME"}
                   ]
}

destination = requests.post(destination_url, 
                       data=json.dumps(destination_attrs), headers=destination_aws_headers)

print(destination)

