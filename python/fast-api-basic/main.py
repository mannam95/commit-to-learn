from io import StringIO
from typing_extensions import Annotated
from fastapi import FastAPI, File, UploadFile
from src.train import model_train_test_by_given_files
import pandas as pd

# Create an instance of FastAPI
app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian", "defaultModelsExpandDepth": -1})

# Define a base route
@app.get("/")
def api_index():
   return {"message": "Not Implemented Yet"}


@app.post("/model-train")
def api_model_train_test_by_given_files(trainFile: UploadFile = File(...), testFile: UploadFile = None):
   try:
      # check whether the files are uploaded or not
      if not (trainFile):
         return {"error": "Please upload both train file"}
              
      # check if the files are in csv format or not
      if trainFile.filename.split(".")[-1] != "csv" or (testFile and testFile.filename.split(".")[-1] != "csv"):
         return {"error": "Please upload csv files only"}
            
      # if the files are uploaded and in csv format, then call the model_train_test_by_given_files function
      # Call the model_train_test_by_given_files function
      return model_train_test_by_given_files(trainFile, testFile)
   except Exception as e:
         return {"error at api_model_train_test_by_given_files:": str(e)}