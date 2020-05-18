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

import os

import numpy as np

# %%
class ScoreCode():
    
    def writeScoreCode(self, inputDF, targetDF, modelPrefix,
                       predictMethod, pickleName,
                       metrics=['EM_EVENTPROBABILITY', 'EM_CLASSIFICATION'],
                       pyPath=os.getcwd(), threshPrediction=None,
                       otherVariable=False):
        '''
        Write python score code for model manager based on training data used
        to generate the model pickle file. The python file will be included in 
        the zip file to be imported into model manager.
        
        The score code generated is designed to be a working template for any 
        Python model to be used in SAS Open Model Manager, but is not guaranteed 
        to work out of the box for scoring and publishing/validating.
        
        Note that for categorical variables, the variable is split into all of
        the possible categorical values of the variable and by default does NOT
        include a catch-all [catVar]_Other variable to include any missing 
        values or any values not found in the training dataset. If you have 
        missing values or values not included in your training dataset, you
        will need to set the OtherVariable option to true.
        
        Parameters
        ---------------
        inputDF : dataframe
            Dataframe containing training data, including only the predictor
            columns. This function currently only supports int(64), float(64),
            and str data types for scoring.
        targetDF : dataframe
            Dataframe containing training data of the target variable.
        modelPrefix : string
            Variable name for the model to be displayed in model manager 
            (i.e. hmeqClassTree + [Score.py || .pickle]).      
        predictMethod : string
            User-defined prediction method for score testing. This should be
            in a form such that the model and data input can be added using 
            the format() command. 
            For example: '{}.predict_proba({})'.
        pickleName : string
            Name of pickle file containing the model.
        metrics : string list, optional
            Scoring metrics for model manager. The default is a set of two
            metrics: EM_EVENTPROBABILITY and EM_CLASSIFICATION.
        pyPath : string, optional
            Local path of the score code file. The default is the current 
            working directory.
        threshPrediction : float, optional
            Prediction theshold for probability metrics. For classification,
            below this threshold is a 0 and above is a 1.
        otherVariable : boolean, optional
            Option for having a categorical other value for catching missing 
            values or values not found in the training dataset. The default
            is set to False.
    			
    		Yields
    		---------------
        '*Score.py'
            Python score code file for model manager.
        '''       
        
        inputVarList = list(inputDF.columns)
        newVarList = list(inputVarList)
        inputDtypesList = list(inputDF.dtypes)        
    
        pyPath = os.path.join(pyPath, modelPrefix + 'Score.py')
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
            
            for i, dTypes in enumerate(inputDtypesList):
                dTypes = dTypes.name
                if 'int' in dTypes or 'float' in dTypes:
                    if self.checkIfBinary(inputDF[inputVarList[i]]):
                        self.pyFile.write(f'''\n
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
    
        # insert the model into the provided predictMethod call
            predictMethod = predictMethod.format('_thisModelFit', 'inputArray')
            self.pyFile.write(f'''\n
    prediction = {predictMethod}''')
            
            self.pyFile.write(f'''\n
    {metrics[0]} = float(prediction)''')
            if threshPrediction is None:
                threshPrediction = np.mean(targetDF)
                self.pyFile.write(f'''\n
    if ({metrics[0]} >= {threshPrediction}):
        {metrics[1]} = '1'
    else:
        {metrics[1]} = '0' ''')
            
            self.pyFile.write(f'''\n
    return({metrics[0]}, {metrics[1]})''')
            
    def splitStringColumn(self, inputSeries, otherVariable):
        '''
        Split a column of string values into a number of new variables equal
        to the number of unique values in the original column (excluding None
        values). Then write to file new statements that tokenize the newly
        defined variables.
        
        As an example: given a series named strCol with values ['A', 'B', 'C',
        None, 'A', 'B', 'A', 'D'], designate the following new variables: 
        strCol_A, strCol_B, strCol_D. Then write the following to file:
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
        Check a pandas series to determine if the values are binary or nominal.
        
        Parameters
        ---------------
        inputSeries : float or int series
            Series with numeric values.
        
        Returns
        ---------------
        isBinary : boolean
            True if the series values are binary. False if the series values
            are nominal.
        '''
        
        isBinary = False
        binaryFloat = [float(1), float(0)]
        
        if inputSeries.value_counts().size == 2:
            if (binaryFloat[0] in inputSeries.astype('float') and 
                binaryFloat[1] in inputSeries.astype('float')):
                isBinary = False
            else:
                isBinary = True
                
        return isBinary
        