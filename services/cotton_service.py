import numpy as np
from fastapi import HTTPException
from utils.model_loader import load_cotton_models

disease_labels = [
    "damping_off",
    "root_rot",
    "bacterial_blight",
    "alternaria_leaf_spot",
    "fusarium_wilt",
    "verticillium_wilt",
    "boll_rot"
]

def predict_cotton(data):
    scaler, crop_encoder, stage_encoder, model = load_cotton_models()

    try:
        # Normalize input (CRITICAL)
        crop = data.crop.strip().lower()
        stage = data.growth_stage.strip()

        stage_encoded = stage_encoder.transform([stage])[0]
        crop_encoded = crop_encoder.transform([crop])[0]

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Encoding error: {str(e)}"
        )

    # Feature order MUST match training
    X = np.array([[ 
        data.vegetation_stress_score,
        data.water_stress_score,
        data.soil_stress_score,
        data.final_stress_percent,
        data.gdd_min,
        data.gdd_max,
        stage_encoded,
        crop_encoded
    ]])

    try:
        X_scaled = scaler.transform(X)
        preds = model.predict(X_scaled)[0]

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Model inference failed: {str(e)}"
        )

    return {
        disease_labels[i]: round(float(preds[i]), 4)
        for i in range(len(disease_labels))
    }