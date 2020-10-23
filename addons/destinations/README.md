# Configuring Publishing Destinations

This directory contains examples of Jupyter notebooks that you can use to create container publishing destinations for Amazon Web Services (AWS), Azure, CAS, and Private Docker. 
The [viya35](./viya35) directory contains the examples for configuration publishing destinations for SAS Model Manager 15.3 on SAS Viya 3.5 and SAS Open Model Manager 1.2.

You can use the example Jupyter notebooks or Python scripts to create new publishing destinations for the following destination types: CAS, Amazon Web Services (AWS), Azure and Private Docker.

_**Note:** Creating a publishing destination for Azure is only supported for SAS Viya 4._

## SAS Viya 4

**Content in progress...**

### Prerequisites for Creating a Publishing Destination for SAS Viya 4

* Make sure that you have Python 3 with the requests package installed on the machine where you are going to run the Jupyter notebooks or scripts.

**_Question: Where should Python be installed to run the Jupyter notebooks?_**

### Enable Publishing Validation on Azure

1. Create and integrate an Azure Active Directory Application with an Azure Kubernetes Service cluster.
   
   Use the following modifications when performing the steps in the [Azure Active Directory Integration](https://docs.microsoft.com/en-us/azure/aks/azure-ad-integration) documentation: 
    
      1. To associate a virtual machine (VM) with each node in the cluster, modify the 'az aks create' command to include two additional options, when creating the cluster:
         ```
	        --vm-set-type AvailabilitySet
	        --load-balancer-sku basic
         ```
      2. You must add a static public IP address to each VM, and provide at least one of these IP addresses when creating a publishing destination.

2. Add an inbound port rule to each VM with these values:
   ```
   Source: IP Addresses
   Source IP Address: <customer IP range>
   Source port ranges: *
   Destination: Any
   Destination port ranges: 30000-32767
   Protocol: TCP
   Action: Allow
   Priority: 100
   ```

3. Add a contributor role to the Azure Active Directory application.

   1. From the Azure portal, select **Subscriptions**.
   2. Select the subscription where the cluster was created.
   3. Select access control (IAM).
   4. Click **Add** and select **Add role assignment**.
   5. Select the following values from the drop-down lists:
       
          Role: Contributor
          Assign access to: Azure AD user, group, service principal
          Select: Search for your AAD server application
          
   6. Click **Save**.
   
### Create Publishing Destinations

Run the Jupyter notebook or Python script for a specific destination type to create a publishing destination:

* [CreateAWSDestination.ipynb](./CreateAWSDestination.ipynb)
* [CreateAzureDestinatin.ipynb](./CreateAzureDestination.ipynb)
* [CreatePrivateDockerDestination.ipynb](./CreatePrivateDockerDestination.ipynb)
* [create_cas_destination.py](./create_cas_destination.py)


## SAS Viya 3.5

Here are the prerequisites for creating a new publishing destination for SAS Viya 3.5:

* Make sure that you have Python 3 with the requests package installed on the machine where you are going to run the scripts.

  Here is an example of using yum to install Python 3 on a machine:
  ```
   sudo yum install -y python3
   sudo pip3 install requests
   ```

* If your destination type is AWS, you must create a credential domain in SAS Credentials service and store the AWS access key information in the credentials. Please modify the host URL (viya_host and port), SAS account, and AWS access key information in the script, and then enter the domain name in the create_aws_destination.py file.
  ```
   python create_aws_credential_domain.py
  ```

* Make sure that you modify the host URL (viya_host and port), SAS account, Domain name, or private docker information in the script before you run them.

* If Python 3 executable file name is 'python3', then update the following commands to use 'python3', instead of 'python'.
  ```
   python create_cas_destination.py
   python create_aws_destination.py
   python create_privatedocker_destination.py
  ```
