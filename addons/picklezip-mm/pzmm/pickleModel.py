# Copyright (c) 2020, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0


# %%
<<<<<<< HEAD
from pathlib import Path
=======
import os
>>>>>>> 7f7206d (initial commit of omm repo)

import pickle

# %%
class PickleModel():
    
<<<<<<< HEAD
    def pickleTrainedModel(trainedModel, modelPrefix, pPath=Path.cwd()):
        '''
        Writes the trained model to a binary pickle file.
=======
    def pickleTrainedModel(trainedModel, modelPrefix, pPath=os.getcwd()):
        '''
        Write trained model to a binary pickle file. 
>>>>>>> 7f7206d (initial commit of omm repo)
        
        Parameters
        ---------------
        trainedModel
            User-defined trained model.
        modelPrefix : string
<<<<<<< HEAD
            The variable name for the model to be displayed in SAS Open Model Manager or SAS Model Manager
=======
            Variable name for the model to be displayed in SAS Open Model Manager 
>>>>>>> 7f7206d (initial commit of omm repo)
            (i.e. hmeqClassTree + [Score.py || .pickle]).
        pPath : string, optional
            File location for the output pickle file. Default is the current
            working directory.
			
		Yields
		---------------
		'*.pickle'
<<<<<<< HEAD
			The binary pickle file that contains the trained model.
        '''
        
        with open(pPath / (modelPrefix + '.pickle'), 'wb') as pFile:
=======
			Binary pickle file containing a trained model.
        '''
        
        with open(os.path.join(pPath, modelPrefix + '.pickle'), 'wb') as pFile:
>>>>>>> 7f7206d (initial commit of omm repo)
            pickle.dump(trainedModel, pFile)