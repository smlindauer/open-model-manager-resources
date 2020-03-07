# Overview

This directory contains examples of Jupyter notebooks and Python code that can be used to perform the following SAS Open Model Manager tasks:
* Calculate fit statistics, ROC, and lift, and then generate JSON files for a Python model
* Get the number of published models
* Build and import a trained Python model
* Fit a scoring script for Python model containerization
* Fit a scoring script for R model containerization


## Calculate Fit Statistics, ROC, and Lift, and then Generate JSON Files

When you compare models, the model comparison output includes model properties, user-defined properties, and variables. The model comparison output 
might also include fit statistics, and lift and ROC plots for the models if the required model files are available. The fit statistics, as well as 
plots for lift and ROC, can be produced using Python packages that then generate JSON files. These JSON files are used to show the fit statistics
and plots when comparing models in SAS Open Model Manager.


## Get the Number of Published Models

You can return the number of projects with published models and the total number of published models by destination type. Before you can return a count for published models,
you must perform the following steps:

1. Specify the URL for your host server.
2. Specify the user ID and password for either an administrator or a non-adminstrator user.
3. Get an authentification token.


## Build and Import a Trained Python Model

A Python model can be built and trained before importing the model in SAS Open Model Manager as a ZIP file. The ZIP file contains model files that are associated
with a specific model and stored within the ZIP file. The ZIP file can contain model folders at the same level or in a hierarchical folder structure. 
Each model folder within the ZIP file is imported as a separate model object that contains the contents of the model folder. 
When you import models from a ZIP file into a project version, the hierarchical folder structure is ignored. To build and import a trained Python model, you must
perform the following steps:

1. Build and train a model.
2. Serialize the model into a pickle file and deploy the pickle file into SAS Open Model Manager.
3. Write JSON files associated with the trained model and write the score code .py file.
4. Zip the pickle, JSON, and score code files into an archive.
5. Import the ZIP archive file to Open Model Manager via an API call.


## Fit a Scoring Script for Python Model Containerization

The web services in the container store the input CSV file and pass the input file name to your scoring script. Web services will search for the first script whose file 
name ends with 'score.py' for a Python model. The scoring script reads the input data from an input CSV file and then stores the output data in the CSV file.
The scoring script must follow the below pattern:

* The pickle file must be specified in the command-line arguments to be read by the script
* Input variables must be in the inputVar.json file, and the output variables in the outputVar.json file 


## Fit a Scoring Script for R Model Containerization

The web services in the container store the input CSV file and pass the input file name to your scoring script. Web services will search for the first script whose file
name ends with 'score.R' for an R model. The scoring script must follow the below pattern:

* Default R score code that helps score the R model with a RDA model file
* The RDA model file must be specified in the command-line arguments to be read by the script


This project is licensed under the [Apache 2.0 License](../LICENSE).
