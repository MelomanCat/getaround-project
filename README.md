# Getaround Project – Dashboard, MLflow, and Prediction API

This repository contains the files related to my **Getaround student project**, developed as part of a Data Science curriculum. 
The goal was to analyze the impact of introducing a minimum buffer time between car rentals, and to provide tools to support decision-making and price optimization.

###  Repository structure:

- **Streamlit_dashboard/**  
  Contains the code for the interactive dashboard built with Streamlit and deployed on Hugging Face Spaces (https://huggingface.co/spaces/jedha0padavan/getaround-dashboard)
  This subfolder includes its own README with details about the dashboard sections and usage.

- **MLflow/**  
  Contains the training script (`train.py`) used to train a regression model and track the experiment using MLflow.
  Experiment getaround-pricing here : https://huggingface.co/spaces/jedha0padavan/mlflow-server-final-project
  
- **API/**  
  Contains the code for a `/predict` API endpoint created with FastAPI.  
  The API takes input data in JSON format and returns a predicted rental price. It is deployed on Hugging Face Spaces (https://huggingface.co/spaces/jedha0padavan/fast-api).



> Both the dashboard and the API are publicly available online via Hugging Face.  
> This project combines data analysis, model deployment, and interactive visualization in a real-world scenario.

