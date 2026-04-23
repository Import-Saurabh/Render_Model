
# Crop Disease Prediction API `v1.0.0`
> **FastAPI-based ML Inference Service for Agricultural Disease Detection**

The Crop Disease Prediction API is a production-ready service that predicts disease probabilities for crops using environmental stress scores, growth stage data, and Growing Degree Days (GDD). It enables early disease risk identification to support precision agriculture decisions.

## 🚀 Key Benefits
* **Early Disease Detection:** Predicts disease probability before visible symptoms appear.
* **Multi-Disease Output:** Returns probability scores for 7 diseases per crop in a single API call.
* **Stress-Aware Predictions:** Combines vegetation, water, and soil stress with GDD for high-accuracy inference.
* **Production-Ready:** Lambda-compatible via Mangum, CORS-enabled, and schema-validated with Pydantic.
* **Model Caching:** Models loaded once at startup for low-latency responses.

---

## 📍 API Reference

**Base URL:** `http://127.0.0.1:8000`  
**Version Prefix:** `/api/v1/`

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Health check — returns `{ "status": "ok" }` |
| `POST` | `/api/v1/wheat/predict-diseases` | Predict disease probabilities for **Wheat** |
| `POST` | `/api/v1/cotton/predict-diseases` | Predict disease probabilities for **Cotton** |

---

## 🛠 Input Schema & Validation

All prediction endpoints accept a JSON object with the following fields:

### 1. Stress Score Ranges
| Field | Valid Range | Notes |
| :--- | :--- | :--- |
| `vegetation_stress_score` | `0 to 1` | 0 = no stress, 1 = maximum stress |
| `water_stress_score` | `0 to 1` | 0 = no stress, 1 = maximum stress |
| `soil_stress_score` | `0 to 1` | 0 = no stress, 1 = maximum stress |
| `final_stress_percent` | `0 to 1` | Aggregate score (e.g., `0.36` for 36%) |
| `gdd_min` / `gdd_max` | `>= 0` | Growing degree days |

### 2. Growth Stages (Strict Matching)
The `growth_stage` field must exactly match the strings below (no abbreviations).

* **Wheat Stages:** `Germination`, `Emergence`, `Tillering`, `Stem Elongation & Jointing`, `Booting`, `Heading`, `Flowering`, `Grain Filling`, `Ripening`, `Maturity`, `Harvest`, `Seed Treatment & Sowing`.
* **Cotton Stages:** `Seed Treatment & Sowing`, `Germination & Emergence`, `Seedling Establishment`, `Square Formation`, `Boll Formation`, `Flowering`, `Boll Development`, `Maturity`.

---

## 📝 Usage Example

### Request (Wheat)
```json
POST /api/v1/wheat/predict-diseases
{
  "crop": "wheat",
  "growth_stage": "Tillering",
  "vegetation_stress_score": 0.5,
  "water_stress_score": 0.2,
  "soil_stress_score": 0.5,
  "final_stress_percent": 0.36,
  "gdd_min": 300,
  "gdd_max": 600
}
```

### Response
```json
{
  "crop": "wheat",
  "growth_stage": "Tillering",
  "disease_probabilities": {
    "yellow_rust": 0.12,
    "brown_rust": 0.08,
    "fusarium_head_blight": 0.03,
    "powdery_mildew": 0.05,
    "leaf_blight": 0.09,
    "root_rot": 0.02,
    "smut": 0.01
  }
}
```

---

## 📁 Project Structure
```text
FastAPI Deployment/
├── main.py              # Entry point & Mangum handler
├── core/                # Config & Logging
├── api/v1/              # Endpoint definitions
├── schemas/             # Pydantic models
├── services/            # Business & ML logic
└── models/              # Saved .pkl or .joblib models
```

---

## ⚠️ Known Issues & Setup
**Scikit-learn Version Mismatch:** If you encounter an `InconsistentVersionWarning`, ensure your environment matches the training version:
```bash
pip install scikit-learn==1.6.1
```

**Run Locally:**
```bash
python -m uvicorn main:app --reload
```
Access the interactive Swagger UI at: `http://127.0.0.1:8000/docs`
