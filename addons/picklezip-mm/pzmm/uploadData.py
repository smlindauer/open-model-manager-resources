# Copyright SAS Institute
#
#  Licensed under the Apache License, Version 2.0 (the License);
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# %%
import os

import requests
import getpass
import json

# %%

def getAccessToken(server, username=None, password=None):
    '''
    Retrieve access token from the host server for further API requests. There
    are two options for retrieving an access token:
        1. Only provide the host server in the arguments. The user will be 
        prompted to input their username and password (the password will not
        be displayed in the prompt, nor kept in memory). Five attempts are
        allowed before the program exits.
        2. Provide the username, password, and host server in the arguments.
        After the authentication attempt, the password will be removed from
        the memory.
        
    Parameters
    ---------------
    server : string
        Name of the host server with a model manager installation. Includes 
        the protocol specification (i.e. http://).
    username : string
        Username used for authentication to the server.
    password : string
        Password used for authentication to the server.
    
    Returns
    ---------------
    authToken : string
        Access token from json file from the API post request. Used for 
        further API requests to the host server.
    '''
    
    authURI = '/SASLogon/oauth/token'
    headersAuth = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic c2FzLmVjOg=='
            }
    authToken = ''
    
    if (username is not None) and (password is not None):
        authBody = ('grant_type=password&username=' + username +
                    '&password=' + password)
        authReturn = requests.post(server + authURI,
                                   data=authBody,
                                   headers=headersAuth)
        if authReturn.status_code == 200:
            authToken = authReturn.json()['access_token']        
            notAuthenticated = False
        else:
            notAuthenticated = True
            print('The provided username and password combination failed to' + 
                  ' authenticate. Please enter correct a username and' + 
                  ' password combination.')
    else:
        notAuthenticated = True
    
    loginAttempts = 0
    while (notAuthenticated and loginAttempts < 5): 
        username = input('Enter username:')
        password = getpass.getpass('Enter password for %s:' % username)
        authBody = ('grant_type=password&username=' + username +
                    '&password=' + password)
        authReturn = requests.post(server + authURI,
                                   data=authBody,
                                   headers=headersAuth)
        if authReturn.status_code == 200:
            authToken = authReturn.json()['access_token']
            notAuthenticated = False
        else:
            print('Please enter correct username and password.')
            loginAttempts += 1
    
    password = ''
    
    return f'Bearer {authToken}'


class ModelImport():
    
    def __init__(self, host):
        '''
        Initialize ModelImport class with host location and username/password.
        
        Parameters
        ---------------
        host : string
            Name of the host server with a model manager installation.
        '''
        
        if host[:7] == 'http://':
            host = host[7:]
        self.host = host
        self.server = 'http://' + host
            
    def findProjectID(self, projectName, authToken):
        '''
        Given a project name, make an API request to model manager to find the 
        project ID. If project ID is not found, create a new project and return
        its project ID.
        
        Parameters
        ---------------
        projectName : string
            Project name for retrieving the project ID.
        authToken : string
            Access token used for API requests.
        
        Returns
        ---------------
        projectID : string
            Universally unique identifier string project identifier.
        '''
        
        headers = {
                'Origin': self.server,
                'Authorization': authToken}
        projectFilter = f'?filter=eq(name, \'{projectName}\')'
        requestUrl = f'{self.server}/modelRepository/projects{projectFilter}'
        projectRequest = requests.get(requestUrl, headers=headers)
        
        try:
            projectID = projectRequest.json()['items'][0]['id']
        except IndexError:
            print(f'No project named {projectName} could be found.')
            print(f'Creating a new project named {projectName}.')
            projectID = self.createNewProject(projectName, authToken)
            return projectID
            
        return projectID

    def createNewProject(self, projectName, authToken):
        '''
        Determine the public repository folder ID. Then create a new project 
        on model manager to store models in.
        
        Parameters
        ---------------
        projectName : string
            Project name for retrieving the project ID.
        authToken : string
            Access token used for API requests.      
        
        Returns
        ---------------
        projectID : string
            Universally unique identifier string project identifier.
        '''
        
        repositoryHeaders = {'Authorization': authToken}
        requestUrl = (f'{self.server}/modelRepository/repositories' +
                      "?filter=eq(name,'Public')")
        repositoryList = requests.get(requestUrl, headers=repositoryHeaders)
        repositoryID = repositoryList.json()['items'][0]['id']
        repositoryFolderID = repositoryList.json()['items'][0]['folderId']
        
        headers = {'Content-Type': 'application/vnd.sas.models.project+json',
                   'Authorization': authToken}
        body = {'name': projectName,
                'repositoryId': repositoryID,
                'folderId': repositoryFolderID}
        url = f'{self.server}/modelRepository/projects'
        newProject = requests.post(url, data=json.dumps(body), headers=headers)
        
        return newProject.json()['id']
    
    def importModel(self, modelPrefix, projectID=None,
                    projectName=None, zPath=os.getcwd(),
                    username=None, password=None):
        '''
        Import zipped pickle file and corresponding python and json files into
        model manager using the 'import model' API. 
        
        If the project ID is not known, provide the project name and an API
        request will search for the project ID. If no project already exists, 
        do not provide either the project name or ID and the function will 
        create a new project via an API request.
        
        Parameters
        ---------------
        modelPrefix : string
            Variable name for the model to be displayed in model manager 
            (i.e. hmeqClassTree + [Score.py || .pickle]).
        projectID : string, optional
            Universally unique identifier string project identifier. Default is None.
        projectName : string, optional
            Project name for retrieving the project ID. Default is None.
        zPath : string, optional
            File location for the zipped archive. Default is the current
            working directory.
        username : string
            Username used for authentication to the server.
        password : string
            Password used for authentication to the server.            
        '''
        authToken = getAccessToken(self.server, username, password)
        
        if projectID is None and projectName is not None:
            projectID = self.findProjectID(projectName, authToken)
        elif projectID is None and projectName is None:
            projectName = input('Please specify a new project name:')
            projectID = self.createNewProject(projectName, authToken)
        
        with open(zPath, 'rb') as zFile:
            
            body = {'name': modelPrefix,
                    'type': 'zip',
                    'projectId': projectID,
                    'versionOption': 'LATEST'}

            files = {'file': (f'{modelPrefix}.zip',
                              zFile,
                              'multipart/form-data')}

            headers = {'Origin': f'{self.server}',
                       'Authorization': authToken}

            url = f'{self.server}/modelRepository/models'
            modelRequest = requests.post(url,
                                         headers=headers,
                                         files=files,
                                         data=body)
        
        try:
            modelRequest.raise_for_status()
        except requests.exceptions.HTTPError:
            print('Model import failed: ' +
                  f'A model named {modelPrefix} already exists.')
            print('Please adjust the zip file name appropriately.')
# DEPRECIATED       
#    def uploadPickle(pLocalPath, pRemotePath,
#                     host, username, password=None, privateKey=None):
#        #TODO: Remove password from memory as in self.getAccessToken() 
#        #TODO: Obsoleted after 19w47 builds of model manager
#        '''
#        Upload a local pickle file to a model manager server via sftp. Set the
#        permission of the pickle file on the server to 777 to allow the score
#        code to use the pickle file.
#        
#        Parameters
#        ---------------
#        pLocalPath : string
#            Local path of the pickle file.
#        pRemotePath : string
#            Remote path on the server for the pickle file's location.
#        host : string
#            Name of the host server to send the pickle file.
#        username : string
#            Server login credential username.
#        password : string, optional
#            Password for SFTP connection attempt. Default is None, in case
#            user is using an RSA/DSA key pairing.
#        privateKey : string, optional
#            Private key location for RSA/DSA key pairing logins. Default is 
#            None.
#        '''
#        
#        # convert windows path format to linux path format
#        if platform.system() == 'Windows':
#            pRemotePath = ('/' + 
#                           os.path.normpath(pRemotePath).replace('\\', '/'))
#        
#        with pysftp.Connection(host, username=username, password=password,
#                               private_key=privateKey) as sftp:
#            sftp.put(pLocalPath, remotepath=pRemotePath)
#            sftp.chmod(pRemotePath, mode=777)