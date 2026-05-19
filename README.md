# 🚗 Getaround — Pricing Optimization & Delay Impact Analysis

End-to-end data project combining product analytics, interactive visualization, and machine learning deployment for a car-sharing platform.

The project focuses on analyzing the impact of introducing a minimum buffer time between rentals in order to reduce operational issues caused by late vehicle returns.

## 📊 Key Findings

- Most delays are under 1 hour, meaning short buffers can resolve a large share of problematic bookings
- The optimal strategy was a 30-minute buffer applied only to Connect vehicles
- This scenario resolved ~49.5% of at-risk rentals while minimizing revenue loss (~€14K)

## 🚀 Project Components

### 📈 Interactive Dashboard
Built with Streamlit and deployed on Hugging Face Spaces.

The dashboard allows users to:
- compare Connect vs Non-Connect vehicles
- visualize delay frequency and operational impact
- simulate multiple buffer scenarios
- evaluate revenue vs operational trade-offs

🔗 Dashboard demo: https://huggingface.co/spaces/jedha0padavan/getaround-dashboard

---

### 🤖 Price Prediction API
FastAPI endpoint predicting daily rental prices based on vehicle characteristics.

- Model: Random Forest Regressor
- Experiment tracking with MLflow
- JSON input/output format

🔗 API demo: https://huggingface.co/spaces/jedha0padavan/fast-api

---

### 📦 MLflow Experiment Tracking
Training experiments and model tracking performed using MLflow.

🔗 MLflow server: https://huggingface.co/spaces/jedha0padavan/mlflow-server-final-project

---

## 🛠️ Tech Stack

Python · Pandas · Scikit-learn · Streamlit · FastAPI · MLflow · Hugging Face Spaces

---

## 📁 Repository Structure

### `Streamlit_dashboard/`
Interactive dashboard source code.

### `MLflow/`
Training scripts and MLflow experiment tracking.

### `API/`
FastAPI `/predict` endpoint implementation.
