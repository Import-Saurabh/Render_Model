import pickle
import os

MODEL_CACHE = {}

def _load_pickle(path):
    with open(path, "rb") as f:
        return pickle.load(f)

# =========================
# WHEAT
# =========================
# model_loader.py — corrected file names

def load_wheat_models():
    if "wheat" in MODEL_CACHE:
        return MODEL_CACHE["wheat"]

    base = os.getenv("MODEL_PATH_WHEAT", "models/wheat/")

    scaler        = _load_pickle(base + "stress_scaler.pkl")
    crop_encoder  = _load_pickle(base + "crop_encoder.pkl")
    stage_encoder = _load_pickle(base + "stage_encoder.pkl")
    model         = _load_pickle(base + "disease_probability_ann_multi.pkl")

    MODEL_CACHE["wheat"] = (scaler, crop_encoder, stage_encoder, model)
    return MODEL_CACHE["wheat"]


def load_cotton_models():
    if "cotton" in MODEL_CACHE:
        return MODEL_CACHE["cotton"]

    base = os.getenv("MODEL_PATH_COTTON", "models/cotton/")

    scaler        = _load_pickle(base + "scaler.pkl")               # ← was stress_scaler.pkl
    crop_encoder  = _load_pickle(base + "crop_encoder.pkl")
    stage_encoder = _load_pickle(base + "stage_encode.pkl")         # ← was stage_encoder.pkl
    model         = _load_pickle(base + "cotton_ann_model.pkl")     # ← was disease_probability_ann_multi.pkl

    MODEL_CACHE["cotton"] = (scaler, crop_encoder, stage_encoder, model)
    return MODEL_CACHE["cotton"]

# =========================
# GENERIC ACCESS
# =========================
def load_models(crop: str):
    crop = crop.lower()

    if crop == "wheat":
        return load_wheat_models()
    elif crop == "cotton":
        return load_cotton_models()
    else:
        raise ValueError(f"Unsupported crop: {crop}")