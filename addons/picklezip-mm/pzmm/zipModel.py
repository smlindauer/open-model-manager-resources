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
from pathlib import Path
import zipfile

# %%

class ZipModel():
    
    def zipFiles(fileDir, modelPrefix):
        '''
        Combines all JSON files with the model pickle file and associated score code file
        into a single archive ZIP file.
        
        Parameters
        ---------------
        fileDir : string
            Location of *.json, *.pickle, and *Score.py files.
        modelPrefix : string
            Variable name for the model to be displayed in SAS Open Model Manager 
            (i.e. hmeqClassTree + [Score.py || .pickle]).
            
        Yields
        ---------------
        '*.zip'
            Archived ZIP file for importing into SAS Open Model Manager. In this form,
            the ZIP file can be imported into SAS Open Model Manager.
        '''
        
        fileNames = []
        fileNames.extend(sorted(Path(fileDir).glob('*.json')))
        fileNames.extend(sorted(Path(fileDir).glob('*Score.py')))
        fileNames.extend(sorted(Path(fileDir).glob('*.pickle')))
        
        with zipfile.ZipFile(Path(fileDir) / (modelPrefix + '.zip'), mode='w') as zFile:
            for name in fileNames:
                zFile.write(Path(fileDir) / name, arcname=name)