import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from typing import List
import mlflow.pyfunc
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

### 
# Define configurations 
###
description = '''

## Cette API permet de prédire le prix de location d'un véhicule sur la plateforme Getaround à partir des données fournies.

## Endpoints disponibles :

- `/predict` (POST) : reçoit un JSON contenant les caractéristiques du véhicule et renvoie le prix prédit.

    Exemple de requête :
    ```json
    {
      "input": [
        {
          "model_key": "Citroën",
          "fuel": "gasoline",
          "paint_color": "red",
          "car_type": "sedan",
          "private_parking_available": true,
          "has_gps": false,
          "has_air_conditioning": true,
          "automatic_car": false,
          "has_getaround_connect": true,
          "has_speed_regulator": false,
          "winter_tires": true,
          "mileage": 12345.0,
          "engine_power": 150.0
        }
      ]
    }
    ```

    Exemple de réponse :
    ```json
    {
      "prediction": [123.45]
    }
    ```




'''

# URI of the tracking server (Hugging Face Space)
mlflow.set_tracking_uri("https://jedha0padavan-mlflow-server-final-project.hf.space")



# Initiate FastAPI
app = FastAPI(
    title = "API de Prédiction des Prix Getaround",
    description=description,
    version = "0.1"
    
)
# Root endpoint - landing page
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root():
    return """
    <html>
        <head>
            <title>🚗 Getaround Price Prediction API</title>
        </head>
        <body>
            <h2>✅ L'API de prédiction de prix est en ligne !</h2>
            </br>
            <h3>Consultez la <a href="/docs" target="_blank">documentation interactive</a> pour tester l'API.</h3>
        </body>
    </html>
    """

# Describe input format
class Item(BaseModel):
    model_key: str
    fuel: str
    paint_color: str
    car_type: str
    private_parking_available: bool
    has_gps: bool
    has_air_conditioning: bool
    automatic_car: bool
    has_getaround_connect: bool
    has_speed_regulator: bool
    winter_tires: bool
    mileage: float
    engine_power: float


class PredictionInput(BaseModel):
    input: List[Item]


###
# Define enpoints 
###
@app.post("/predict", tags=["Prediction"], operation_id="predict")
async def predict(data: PredictionInput):
    # Load model from run
    #logged_model = "runs:/4948312f56e14719bdefb9f9c14c202b/model"

    # Load model as a PyFuncModel.
    #loaded_model = mlflow.pyfunc.load_model(logged_model)
    # load model locally
    #model_path = "model"
    #
    #loaded_model = mlflow.pyfunc.load_model(model_path)

    #load model directly from S3 artifacts
    model_uri = "runs:/9a0814e20c0b482d9d5a66587c258ee1/model"
    loaded_model = mlflow.pyfunc.load_model(model_uri)

    try:
        df = pd.DataFrame([item.model_dump() for item in data.input])
        prediction = loaded_model.predict(df)
        return {"prediction": prediction.tolist()}
    except Exception as e:
        return {"error": str(e)}



if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)