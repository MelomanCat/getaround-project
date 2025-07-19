import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from mlflow.models.signature import infer_signature
import pandas as pd
import numpy as np



# read dataset
path = "https://fullstackds-projects-bucket.s3.eu-west-3.amazonaws.com/data/Getaround/get_around_pricing_project.csv"
df_pricing = pd.read_csv(path, index_col=0)
df_pricing['mileage'] = df_pricing['mileage'].astype(float)
df_pricing['engine_power'] = df_pricing['engine_power'].astype(float)

# Divide target from features
y = df_pricing["rental_price_per_day"]
X = df_pricing.drop("rental_price_per_day", axis=1)

# categorize features
cat_cols = ["model_key", "fuel", "paint_color", "car_type"]
num_cols = ["mileage", "engine_power"]
bool_cols = [col for col in X.columns if col not in cat_cols + num_cols]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Define preprocessing
preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols) # to enable API handle new categories from input
], remainder="passthrough") # leave boolean without encoding - RandomForest can deal with such data

# Wrap preprocessing and model in Pipeline
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", RandomForestRegressor(random_state=42))
])

# Model logging

# Setting up MLflow server address
mlflow.set_tracking_uri("https://jedha0padavan-mlflow-server-final-project.hf.space")

# Set a separate experiment for this model
mlflow.set_experiment("getaround-pricing")

with mlflow.start_run() as run:
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    mlflow.log_metric("mae", mae)
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("r2", r2)

    # Use signature to save info about input/output
    signature = infer_signature(X_test, pipeline.predict(X_test))

    # Input example
    input_example = X_test.iloc[:1]

    mlflow.sklearn.log_model(
        sk_model=pipeline,
        artifact_path="model",
        input_example=input_example,
        signature=signature
)

run_id = run.info.run_id
model_uri = f"runs:/{run_id}/model"

mlflow.register_model(model_uri, "getaround-pricing")
  