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
import io
import os
from setuptools import setup, find_packages

# %% 
def getFile(fName):
    with io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              fName), encoding='utf8') as inFile:
        return inFile.read()
    
setup(
      name='picklezip-mm',
      version='0.1-dev',
      description='',
      long_description=getFile('README.md'),
      long_description_content_type='text/markdown',
      author='SAS',
      author_email='support@sas.com',
      url='./picklezip-mm',
      license='',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
              'pysftp >= v0.2.9',
              'pandas >= v0.25.3'
              ],
      classifiers=[
              'Development Status :: 1 - Planning Copy',
              'Environment :: Console',
              'Intended Audience :: Science/Research',
              'Programming Language :: Python',
              'Topic :: Scientific/Engineering'
              ]
      )