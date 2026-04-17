Wheat Multi-Disease Prediction Model (ANN + FastAPI)

This project implements an Artificial Neural Network (ANN) to predict multiple wheat disease probabilities using rule-based stress scores and GDD-based growth stage context.
The trained model is deployed using FastAPI with Swagger UI for easy testing.

"" Key Design Principles

ANN only learns relationships (no agronomy logic inside ML)

Stress is rule-based, not learned

No DAS used (only GDD)

Growth stage is pre-mapped, not predicted

Multi-output regression (7 disease probabilities)

"""" Model Inputs

The model expects already calculated stress scores and stage context.

Field	Description
vegetation_stress_score	Normalized (0–1)
water_stress_score	Normalized (0–1)
soil_stress_score	Normalized (0–1)
final_stress_percent	0–100
gdd_min	Stage lower GDD
gdd_max	Stage upper GDD
crop	Encoded (e.g., Wheat)
growth_stage	Encoded (Tillering, Flowering, etc.)
"""" Model Outputs

The ANN predicts 7 independent disease probabilities:

yellow_rust

brown_rust

fusarium_head_blight

powdery_mildew

leaf_blight

root_rot

smut

A dominant disease is derived after prediction (post-processing).

📁 Project Structure (Simple)
Wheat_Master_Model/
│
├── main.py                             # FastAPI inference
├── train_ann_multi_disease.py          # Training script
├── wheat_with_mapped_disease1row.xlsx  # Training dataset
│
├── disease_probability_ann_multi.pkl   # Trained ANN model
├── stress_scaler.pkl                   # StandardScaler
├── crop_encoder.pkl                    # Crop encoder
├── stage_encoder.pkl                   # Stage encoder
│
├── requirements.txt
└── README.md

:: Environment Setup
1️ Create & activate virtual environment
python -m venv venv
venv\Scripts\activate

2️ Install dependencies
pip install -r requirements.txt


Recommended requirements.txt:

fastapi
uvicorn
numpy
scikit-learn==1.6.1
pydantic

""" Model Training
Run training script
python train_ann_multi_disease.py

Training Output

Trains ANN (MLPRegressor)

Saves:

disease_probability_ann_multi.pkl

stress_scaler.pkl

crop_encoder.pkl

stage_encoder.pkl

Example console output:

Mean Absolute Error (MAE): 0.1248
Training complete. Multi-disease ANN model saved.

"""" Run FastAPI Inference Server
Start server on custom port (recommended)
python -m uvicorn main:app --port 8001

"""" Swagger UI (API Testing)

Open in browser:

http://127.0.0.1:8001/docs

""" API Endpoint
POST /predict-disease
Sample Request
{
  "crop": "Wheat",
  "growth_stage": "Tillering",
  "vegetation_stress_score": 0.26,
  "water_stress_score": 0.58,
  "soil_stress_score": 0.62,
  "final_stress_percent": 58,
  "gdd_min": 300,
  "gdd_max": 600
}

Sample Response
{
  "disease_probabilities": {
    "yellow_rust": 0.03,
    "brown_rust": 0.02,
    "fusarium_head_blight": 0.41,
    "powdery_mildew": 0.05,
    "leaf_blight": 0.62,
    "root_rot": 0.21,
    "smut": 0.02
  },
  "dominant_disease": "leaf_blight"
}

*** Common Issues & Fixes
Port already in use
python -m uvicorn main:app --port 8001

sklearn version warning

Ensure training and inference use the same version:

pip install scikit-learn==1.6.1

**** Summary

ANN model with multi-disease outputs

Clean separation of rules vs ML

Simple FastAPI deployment

Swagger UI for testing

(Ready for local use or AWS EC2 deployment)
