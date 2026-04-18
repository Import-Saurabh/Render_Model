import pandas as pd

# Load data
df = pd.read_excel("models/cotton/Cotton_Master_Dataset_CORRECTED.xlsx", sheet_name="Master data")

# Corrected stage‑disease mapping
stage_disease_map = {
    "Seed Treatment & Sowing": ["damping_off", "root_rot"],
    "Germination & Emergence": ["damping_off", "root_rot"],
    "Seedling Establishment": ["damping_off", "root_rot", "bacterial_blight", "fusarium_wilt"],
    "Square Formation": ["bacterial_blight", "fusarium_wilt", "verticillium_wilt", "alternaria_leaf_spot"],
    "Flowering": ["bacterial_blight", "fusarium_wilt", "verticillium_wilt", "alternaria_leaf_spot"],
    "Boll Formation": ["boll_rot", "bacterial_blight", "fusarium_wilt", "verticillium_wilt", "alternaria_leaf_spot"],
    "Boll Development": ["boll_rot", "fusarium_wilt", "verticillium_wilt", "alternaria_leaf_spot", "bacterial_blight"],
    "Maturity": ["boll_rot", "alternaria_leaf_spot"]
}
disease_cols = ["damping_off", "root_rot", "bacterial_blight", "alternaria_leaf_spot",
                "fusarium_wilt", "verticillium_wilt", "boll_rot"]

def compute_weights(v, w, s):
    """Return dict of raw weights for each disease based on stress scores."""
    return {
        "damping_off": (1 - w) * 0.6 + (1 - s) * 0.4,
        "root_rot": (1 - s) * 0.7 + (1 - w) * 0.3,
        "bacterial_blight": (1 - w) * 0.5 + v * 0.5,
        "fusarium_wilt": v * 0.8 + s * 0.2,
        "verticillium_wilt": v * 0.5 + (1 - w) * 0.3 + s * 0.2,
        "alternaria_leaf_spot": v * 0.9 + s * 0.1,
        "boll_rot": (1 - w) * 0.6 + v * 0.4
    }

for idx, row in df.iterrows():
    stage = row["growth_stage"]
    allowed = stage_disease_map.get(stage, [])
    
    v = row["vegetation_stress_score"]
    w = row["water_stress_score"]
    s = row["soil_stress_score"]
    
    weights_all = compute_weights(v, w, s)
    weights = {d: weights_all[d] for d in allowed}
    total_weight = sum(weights.values())
    
    # Target sum: scale final_stress_percent to a realistic probability range (0–0.8)
    target_sum = (row["final_stress_percent"] / 100) * 0.8
    
    if total_weight > 0:
        for disease in allowed:
            df.at[idx, disease] = (weights[disease] / total_weight) * target_sum
    else:
        for disease in allowed:
            df.at[idx, disease] = 0.0
            
    # Zero out disallowed diseases
    for col in disease_cols:
        if col not in allowed:
            df.at[idx, col] = 0.0

df.to_excel("Cotton_Master_Dataset_FIXED.xlsx", index=False)