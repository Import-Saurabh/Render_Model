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

def softmax(x):
    """Numerically stable softmax"""
    x = np.array(x)
    exp_x = np.exp(x - np.max(x))  # stability trick
    return exp_x / exp_x.sum()

def predict_cotton(data):
    scaler, crop_encoder, stage_encoder, model = load_cotton_models()

    try:
        # Normalize input
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

    # -------------------------------
    # POST-PROCESSING LOGIC
    # -------------------------------

    # Step 1: Raw predictions → dict
    raw_preds = {
        disease_labels[i]: float(preds[i])
        for i in range(len(disease_labels))
    }

    # Step 2: Remove negative values
    filtered = {k: max(v, 0) for k, v in raw_preds.items()}

    # Step 3: Apply threshold (0.1)
    filtered = {k: v for k, v in filtered.items() if v >= 0.1}

    # Step 4: Edge case — if all removed
    if not filtered:
        top_disease = max(raw_preds, key=raw_preds.get)
        return {top_disease: 1.0}

    # Step 5: Softmax normalization
    values = list(filtered.values())
    keys = list(filtered.keys())

    softmax_values = softmax(values)

    # Step 6: Final output
    normalized = {
        keys[i]: round(float(softmax_values[i]), 4)
        for i in range(len(keys))
    }

    return normalized