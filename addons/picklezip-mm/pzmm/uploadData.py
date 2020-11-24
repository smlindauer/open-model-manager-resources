# Copyright (c) 2020, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0


# %%
import os
import platform

import requests
import pysftp
import getpass
import json

# %%

class ModelImport():
    
    def __init__(self, host):
        '''
        Initializes the  ModelImport class with host location, user name, and password.
        
        Parameters
        ---------------
        host : string
            Name of the host server with a SAS Open Model Manager installation.
        '''
        
        if host[:7] == 'http://':
            host = host[7:]
        self.host = host
        self.server = 'http://' + host
        
    def getAccessToken(self):
        '''
        Retrieves the access token from the host server for further API requests.
        Requires user input for user name and password, but does not keep
        password in memory.
        
        Returns
        ---------------
        authToken : string
            Access token from JSON file from the API post request. Used for 
            further API requests to the host server.
        '''
        
        authURI = '/SASLogon/oauth/token'
        headersAuth = {
                'accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Basic c2FzLmVjOg=='
                }
        authToken = ''
        username = ''
        password = ''
        notAuthenticated = True
        
        while notAuthenticated: 
            username = input('Enter username:')
            password = getpass.getpass('Enter password for %s:' % username)
            authBody = ('grant_type=password&username=' + username +
                        '&password=' + password)
            authReturn = requests.post(self.server + authURI,
                                       data=authBody,
                                       headers=headersAuth)
            if authReturn.status_code == requests.codes.ok:
                authToken = authReturn.json()['access_token']
                notAuthenticated = False
            else:
                print('Please enter correct user id and password.')
        
        password = ''
        
        return f'Bearer {authToken}'
    
    def findProjectID(self, projectName, authToken):
        '''
        Given a project name, makes an API request to Model Repository API to find the 
        project ID. If project ID is not found, creates a new project and returns
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
        Determines the Public repository folder ID, and then creates a new project 
        in the common model repository to store the models.
        
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
                    projectName=None, zPath=os.getcwd()):
        '''
        Imports the zipped pickle file and corresponding Python and JSON files into
        the common model repository using the 'import model' API request. 
        
        If the project ID is not known, provide the project name and an API
        request searches for the project ID. If a project does not already exist, and you
        do not provide either the project name or ID, the function  
        creates a new project via an API request.
        
        Parameters
        ---------------
        modelPrefix : string
            Variable name for the model to be displayed in SAS Open Model Manager
            (i.e. hmeqClassTree + [Score.py || .pickle]).
        projectID : string, optional
            Universally unique identifier string project identifier. The default value is None.
        projectName : string, optional
            Project name for retrieving the project ID. The default value is None.
        zPath : string, optional
            Location for the archive ZIP file. The default value is the current
            working directory.
        '''
        authToken = self.getAccessToken()
        
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
        
    def uploadPickle(pLocalPath, pRemotePath,
                     host, username, password=None, privateKey=None):
        #TODO: Remove password from memory as in self.getAccessToken() 
        #TODO: Obsoleted after 19w47 builds of model manager
        '''
        Uploads a local pickle file to a SAS Open Model Manager server via sftp. Set the
        permission of the pickle file on the server to 777 to allow the score
        code to use the pickle file.
        
        Parameters
        ---------------
        pLocalPath : string
            Local path of the pickle file.
        pRemotePath : string
            Remote path on the server for the pickle file's location.
        host : string
            Name of the host server to send the pickle file.
        username : string
            Server login credential username.
        password : string, optional
            Password for SFTP connection attempt. Default is None, in case
            user is using an RSA/DSA key pairing.
        privateKey : string, optional
            Private key location for RSA/DSA key pairing logins. Default is 
            None.
        '''
        
        # convert windows path format to linux path format
        if platform.system() == 'Windows':
            pRemotePath = ('/' + 
                           os.path.normpath(pRemotePath).replace('\\', '/'))
        
        with pysftp.Connection(host, username=username, password=password,
                               private_key=privateKey) as sftp:
            sftp.put(pLocalPath, remotepath=pRemotePath)
            sftp.chmod(pRemotePath, mode=777)