# Copyright (c) 2020, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

<<<<<<< HEAD
from pathlib import Path

=======

import os
import platform

import pandas as pd
>>>>>>> 7f7206d (initial commit of omm repo)
import numpy as np

# %%
class ScoreCode():
    
    def writeScoreCode(self, inputDF, targetDF, modelPrefix,
<<<<<<< HEAD
                       predictMethod, pickleName,
                       metrics=['EM_EVENTPROBABILITY', 'EM_CLASSIFICATION'],
                       pyPath=Path.cwd(), threshPrediction=None,
                       otherVariable=False):
        '''
        Writes a Python score code file based on training data used to generate the model pickle file. The Python file is included in
        the ZIP file that is imported or registered into the common model repository. The model can then be used by SAS applications, such as SAS Open Model Manager.
        
        The score code that is generated is designed to be a working template for any
        Python model, but is not guaranteed to work out of the box for scoring, publishing, or validating the model.
        
        Note that for categorical variables, the variable is split into
        the possible categorical values of the variable. Also, by default it does NOT
        include a catch-all [catVar]_Other variable to store any missing
        values or any values not found in the training data set. If you have
        missing values or values not included in your training data set, you
        must set the OtherVariable option to True.
        
        Parameters
        ---------------
        inputDF : DataFrame
            The `DataFrame` object contains the training data, and includes only the predictor
            columns. The writeScoreCode function currently only supports int(64), float(64),
            and str data types for scoring.
        targetDF : DataFrame
            The `DataFrame` object contains the training data for the target variable.
        modelPrefix : string
            The variable for the model name that is used when naming model files.
=======
                       predictMethod, pRemotePath,
                       metrics=['EM_EVENTPROBABILITY', 'EM_CLASSIFICATION'],
                       pyPath=os.getcwd(), threshPrediction=None):
#TODO: Support additional metrics
        '''
        Writes Python score code for SAS Open Model Manager based on training data that is used
        to generate the model pickle file. The Python file is included in 
        the ZIP file that is imported into SAS Open Model Manager.
        
        Parameters
        ---------------
        inputDF : dataframe
            Dataframe containing training data, including only the predictor
            columns. This function currently only supports int(64), float(64),
            and str data types for scoring.
        targetDF : dataframe
            Dataframe containing training data of the target variable.
        modelPrefix : string
            Variable name for the model to be displayed in SAS Open Model Manager
>>>>>>> 7f7206d (initial commit of omm repo)
            (i.e. hmeqClassTree + [Score.py || .pickle]).      
        predictMethod : string
            User-defined prediction method for score testing. This should be
            in a form such that the model and data input can be added using 
            the format() command. 
<<<<<<< HEAD
            For example: '{}.predict_proba({})'.
        pickleName : string
            Name of the pickle file that contains the model.
        metrics : string list, optional
            The scoring metrics for the model. The default is a set of two
            metrics: EM_EVENTPROBABILITY and EM_CLASSIFICATION.
        pyPath : string, optional
            The local path of the score code file. The default is the current
            working directory.
        threshPrediction : float, optional
            The prediction threshold for probability metrics. For classification,
            below this threshold is a 0 and above is a 1.
        otherVariable : boolean, optional
            The option for having a categorical other value for catching missing
            values or values not found in the training data set. The default setting
            is False.
    			
    		Yields
    		---------------
        '*Score.py'
            The Python score code file for the model.
        '''       
        
        inputVarList = list(inputDF.columns)
        newVarList = list(inputVarList)
        inputDtypesList = list(inputDF.dtypes)        
    
        pyPath = Path(pyPath) / (modelPrefix + 'Score.py')
        with open(pyPath, 'w') as self.pyFile:
        
            self.pyFile.write('''\
import math
import pickle
import pandas as pd
import numpy as np
import settings''')
            
            self.pyFile.write(f'''\n
def score{modelPrefix}({', '.join(inputVarList)}):
    "Output: {', '.join(metrics)}"''')
            
            self.pyFile.write(f'''\n
    try:
        _thisModelFit
    except NameError:
        with open(settings.pickle_path + '{pickleName}', 'rb') as _pFile:
            _thisModelFit = pickle.load(_pFile)''')
=======
            For example: '{}.predict_proba({}).format(model, input)'.
        pRemotePath : string
            Remote path on the server for the pickle file's location.
        metrics : string list, optional
            Scoring metrics for model manager. The default is a set of two
            metrics: EM_EVENTPROBABILITY and EM_CLASSIFICATION.
        pyPath : string, optional
            Local path of the score code file. The default is the current 
            working directory.
        threshPrediction : float, optional
            Prediction theshold for probability metrics. For classification,
            below this threshold is a 0 and above is a 1.
			
		Yields
		---------------
        '*Score.py'
            Python score code file for SAS Open Model Manager.
        '''        
        
        inputVarList = list(inputDF.columns)
        newVarList = inputVarList
        inputDtypesList = list(inputDF.dtypes)
        
        if platform.system() == 'Windows':
            pRemotePath = ('/' + 
                           os.path.normpath(pRemotePath).replace('\\', '/'))        
        
        pyPath = os.path.join(pyPath, modelPrefix + 'Score.py')
        with open(pyPath, 'w') as self.pyFile:
            
            self.pyFile.write('''\
import pickle
import pandas as pd
import numpy as np''')
            
            self.pyFile.write(f'''
def score{modelPrefix}({', '.join(inputVarList)}):
    "Output: {', '.join(metrics)}"''')
            
            self.pyFile.write('''\n
    arguments = locals()''')
            
            self.pyFile.write(f'''\n
    with open('{pRemotePath}') as pFile:
        model = pickle.load(pFile)''')
>>>>>>> 7f7206d (initial commit of omm repo)
            
            for i, dTypes in enumerate(inputDtypesList):
                dTypes = dTypes.name
                if 'int' in dTypes or 'float' in dTypes:
                    if self.checkIfBinary(inputDF[inputVarList[i]]):
                        self.pyFile.write(f'''\n
<<<<<<< HEAD
    try:
        if math.isnan({inputVarList[i]}):
            {inputVarList[i]} = {float(list(inputDF[inputVarList[i]].mode())[0])}
    except TypeError:
        {inputVarList[i]} = {float(list(inputDF[inputVarList[i]].mode())[0])}''')
                    else:
                        self.pyFile.write(f'''\n
    try:
        if math.isnan({inputVarList[i]}):
            {inputVarList[i]} = {float(inputDF[inputVarList[i]].mean(axis=0, skipna=True))}
    except TypeError:
        {inputVarList[i]} = {float(inputDF[inputVarList[i]].mean(axis=0, skipna=True))}''')
                elif 'str' in dTypes or 'object' in dTypes:
                    self.pyFile.write(f'''\n
    try:
        categoryStr = {inputVarList[i]}.strip()
    except AttributeError:
        categoryStr = 'Other'\n''')
                    tempVar = self.splitStringColumn(inputDF[inputVarList[i]],
                                                     otherVariable)
                    newVarList.remove(inputVarList[i])
                    newVarList.extend(tempVar)
    
            self.pyFile.write(f'''\n
    inputArray = pd.DataFrame([[1.0, {', '.join(newVarList)}]],
                              columns = ['const', {', '.join(f"'{x}'" for x in newVarList)}],
                              dtype = float)''')
    
        # Insert the model into the provided predictMethod call.
            predictMethod = predictMethod.format('_thisModelFit', 'inputArray')
=======
    if math.isnan({inputVarList[i]}):
        {inputVarList[i]} = {float(list(inputDF[inputVarList[i]].mode())[0])}''')
                    else:
                        self.pyFile.write(f'''\n
    if math.isnan({inputVarList[i]}):
        {inputVarList[i]} = {float(inputDF[inputVarList[i]].mean(axis=0, skipna=True))}''')
                elif 'str' in dTypes or 'object' in dTypes:
                    self.pyFile.write(f'''\n
    if {inputVarList[i]} is None:
        categoryStr = 'Other'
    else:
        categoryStr = {inputVarList[i]}.strip()\n''')
                    tempVar = self.splitStringColumn(inputDF[inputVarList[i]])
                    newVarList.remove(inputVarList[i])
                    newVarList.append(tempVar)
                    self.pyFile.write('''\n''')
            
            self.pyFile.write('''\n
    scoringDF = pd.DataFrame(, columns=[], dtype=float)''')
            # insert the model into the provided predictMethod call
            predictMethod = predictMethod.format('model')
>>>>>>> 7f7206d (initial commit of omm repo)
            self.pyFile.write(f'''\n
    prediction = {predictMethod}''')
            
            self.pyFile.write(f'''\n
    {metrics[0]} = float(prediction)''')
            if threshPrediction is None:
                threshPrediction = np.mean(targetDF)
<<<<<<< HEAD
                self.pyFile.write(f'''\n
=======
            self.pyFile.write(f'''\n
>>>>>>> 7f7206d (initial commit of omm repo)
    if ({metrics[0]} >= {threshPrediction}):
        {metrics[1]} = '1'
    else:
        {metrics[1]} = '0' ''')
            
            self.pyFile.write(f'''\n
    return({metrics[0]}, {metrics[1]})''')
            
<<<<<<< HEAD
    def splitStringColumn(self, inputSeries, otherVariable):
        '''
        Splits a column of string values into a number of new variables equal
        to the number of unique values in the original column (excluding None
        values). It then writes to a file the statements that tokenize the newly
        defined variables.
        
        Here is an example: Given a series named strCol with values ['A', 'B', 'C',
        None, 'A', 'B', 'A', 'D'], designates the following new variables:
        strCol_A, strCol_B, strCol_D. It then writes the following to the file:
=======
    def splitStringColumn(self, inputSeries):
        '''
        Split a column of string values into a number of new variables equal
        to the number of unique values in the original column (excluding None
        values). Then write to file new statements that tokenize the newly
        defined variables.
        
        As an example: given a series named strCol with values ['A', 'B', 'C',
        None, 'A', 'B', 'A', 'D'], designate the following new variables: 
        strCol_A, strCol_B, strCol_D. Then write the following to file:
>>>>>>> 7f7206d (initial commit of omm repo)
            strCol_A = np.where(val == 'A', 1.0, 0.0)
            strCol_B = np.where(val == 'B', 1.0, 0.0)
            strCol_D = np.where(val == 'D', 1.0, 0.0)
                    
        Parameters
        ---------------
        inputSeries : string series
            Series with the string dtype.
        self.pyFile : file (class variable)
            Open python file to write into.
            
        Returns
        ---------------
        newVarList : string list
            List of all new variable names split from unique values.
        '''
        
        uniqueValues = inputSeries.unique()
        uniqueValues = list(filter(None, uniqueValues))
<<<<<<< HEAD
        uniqueValues = [x for x in uniqueValues if str(x) != 'nan']
        newVarList = []
        for i, uniq in enumerate(uniqueValues):
            uniq = uniq.strip()
            newVarList.append(f'{inputSeries.name}_{uniq}')
            self.pyFile.write(f'''
    {newVarList[i]} = np.where(categoryStr == '{uniq}', 1.0, 0.0)''')
                
        if ('Other' not in uniqueValues) and otherVariable:
            newVarList.append(f'{inputSeries.name}_Other')
            self.pyFile.write(f'''
    {inputSeries.name}_Other = np.where(categoryStr == 'Other', 1.0, 0.0)''')
            
        return newVarList
    
    def checkIfBinary(self, inputSeries):
        '''
        Checks a pandas series to determine if the values are binary or nominal.
=======
        newVarList = []
        for i, uniq in enumerate(uniqueValues):
            uniq = uniq.strip()
            newVarList.append('{}_{}'.format(inputSeries.name, uniq))
            self.pyFile.write('''
    {} = np.where(categoryStr == '{}', 1.0, 0.0)'''.format(newVarList[i],
                                                           uniq))
            
        if 'Other' not in uniqueValues:
            self.pyFile.write(f'''
    {inputSeries.name}_Other = np.where(categoryStr == 'Other', 1.0, 0.0)''')
        
        return newVarList
    
    def checkIfBinary(inputSeries):
        '''
        Check a pandas series to determine if the values are binary or nominal.
>>>>>>> 7f7206d (initial commit of omm repo)
        
        Parameters
        ---------------
        inputSeries : float or int series
<<<<<<< HEAD
            A series with numeric values.
=======
            Series with numeric values.
>>>>>>> 7f7206d (initial commit of omm repo)
        
        Returns
        ---------------
        isBinary : boolean
<<<<<<< HEAD
            The returned value is True if the series values are binary, and False if the series values
=======
            True if the series values are binary. False if the series values
>>>>>>> 7f7206d (initial commit of omm repo)
            are nominal.
        '''
        
        isBinary = False
        binaryFloat = [float(1), float(0)]
        
        if inputSeries.value_counts().size == 2:
            if (binaryFloat[0] in inputSeries.astype('float') and 
                binaryFloat[1] in inputSeries.astype('float')):
<<<<<<< HEAD
                isBinary = False
            else:
=======
>>>>>>> 7f7206d (initial commit of omm repo)
                isBinary = True
                
        return isBinary
        